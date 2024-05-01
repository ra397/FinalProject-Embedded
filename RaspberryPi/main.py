from lcdlib import *
import utime
from machine import ADC, Pin, Timer
import urequests
from connect_to_wifi import *
from get_forecast import *


# Initialize the LCD
lcd = lcd(RS=15, RW=1, EN=14, D4=13, D5=12, D6=11, D7=10, COL=16, ROW=2)
lcd.init()
lcd.clrscr()

# Initialize the sensor
temp_sensor = ADC(Pin(28))  # ADC on GP28/ADC2

# Initialize the joystick
xAxis = ADC(Pin(27))
yAxis = ADC(Pin(26))
button = Pin(17,Pin.IN, Pin.PULL_UP)

displayMode = 0
oldDisplayMode = 0
timeCount = 0

# Connect pico w to internet
connect_to_internet('ala247', 'coolfinch947')

# Server url
url = 'http://192.168.0.101:8000/temperature'


# Function that reads temperature from LM35DZ IC
# Returns a tuple (Temp in Celcius, Temp in Fahrenheit)
def read_temperature(sensor):
    reading = sensor.read_u16()   # Read ADC value (0-65535)
    voltage = reading * 3.3 / 65535  # Convert ADC value to voltage
    c_temperature = voltage * 100  # Convert voltage to temperature in Celsius (10 mV per °C)
    f_temperature = (c_temperature * 9/5) + 32
    return c_temperature, f_temperature

forecast_data = get_weather_forecast(URL)
daily_forecast_data = process_forecast_data(forecast_data)
print(daily_forecast_data)


while True:
    # Get tempreture reading
    temp = read_temperature(temp_sensor)
    
    # Get Joystick reading
    xValue = xAxis.read_u16()
    yValue = yAxis.read_u16()
    buttonValue = button.value()

    # Update xStatus based on xValue
    if xValue <= 600:
        xStatus = "left"
    elif xValue >= 60000:
        xStatus = "right"
    else:
        xStatus = "middle"  

    # Update yStatus based on yValue
    if yValue <= 600:
        yStatus = "up"
    elif yValue >= 60000:
        yStatus = "down"
    else:
        yStatus = "middle"  

    # Update buttonStatus based on buttonValue
    if buttonValue == 0:
        buttonStatus = "pressed"
        if displayMode == 0:
            displayMode = 1
        else:
            displayMode = 0
    else:
        buttonStatus = "not pressed"
    
    # Dispaly to LCD
    print(displayMode)
    if displayMode == 0:
        if oldDisplayMode != displayMode: # clear screen if dispaly mode has changed
            lcd.clrscr()
        lcd.pos_puts(0, 0, "Temp: {:.2f} C".format(temp[0]))
        lcd.pos_puts(6, 1, "{:.2f} F".format(temp[1]))
    else:
        if oldDisplayMode != displayMode: # clear screen if dispaly mode has changed
            lcd.clrscr()
        lcd.pos_puts(0, 0, "Weather Forecast:")
        lcd.pos_puts(0, 1, "Scroll w Joystick")
    
    # Send data to server
    if timeCount == 100:
        lcd.clrscr()
        lcd.pos_puts(0, 0, "Sending data")
        lcd.pos_puts(0, 1, "to server ...")
        data = {
            'c_temperature': temp[0],
            'f_temperature': temp[1]
            }
        try:
            response = urequests.post(url, json=data)  # Send data as JSON
            print(response.text)
            response.close()
        except Exception as e:
            print("Failed to send data:", e)
        timeCount = 0
    
    oldDisplayMode = displayMode
    timeCount += 1
    utime.sleep(0.1)