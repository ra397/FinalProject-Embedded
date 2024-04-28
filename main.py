from lcdlib import *
import time
from machine import ADC, Pin, Timer
import urequests
from connect_to_wifi import *


# Initialize the LCD
lcd = lcd(RS=15, RW=1, EN=14, D4=13, D5=12, D6=11, D7=10, COL=16, ROW=2)
lcd.init()
lcd.clrscr()

# Initialize the sensor
temp_sensor = ADC(Pin(28))  # ADC on GP28/ADC2

# Connect pico w to internet
connect_to_internet()

# Server url
url = 'http://172.20.10.12:8000/temperature'


# Function that reads temperature from LM35DZ IC
# Returns a tuple (Temp in Celcius, Temp in Fahrenheit)
def read_temperature(sensor):
    reading = sensor.read_u16()   # Read ADC value (0-65535)
    voltage = reading * 3.3 / 65535  # Convert ADC value to voltage
    c_temperature = voltage * 100  # Convert voltage to temperature in Celsius (10 mV per °C)
    f_temperature = (c_temperature * 9/5) + 32
    return c_temperature, f_temperature


while True:
    # Get tempreture reading
    temp = read_temperature(temp_sensor)
    
    # Dispaly to LCD
    lcd.pos_puts(0, 0, "Temp: {:.2f} C".format(temp[0]))
    lcd.pos_puts(6, 1, "{:.2f} F".format(temp[1]))
    
    # Send data to server
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
    
    time.sleep(1)