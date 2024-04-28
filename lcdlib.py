######################################################################################
#Title   :  HD44780 LCD Library(4Bit) for Raspberry pi Pico
#Author  :  Bardia Alikhan Afshar <bardia.a.afshar@gmail.com>
#Language:  Python
#Hardware:  Raspberry pi pico
#Moficication : Changed pins on pi
#####################################################################################
from machine import Pin
import utime


class lcd():
    LCD_CLR=0x01        #Screen Clear Command Address               
    LCD_DISP_ON=0x0C    #Screen On Command Address                  
    LCD_DISP_OFF=0x08   #Screen Off Command Address                 
    LCD_BLINK_ON=0x0D   #Cursor Blink On Command Address              
    LCD_BLINK_OFF=0x0C  #Cursor Blink Off Command Address              
    LCD_CURSOR_ON=0x0E  #Cursor On Command Address           
    LCD_CURSOR_OFF=0x0C #Cursor Off Command Address           
    LCD_2LINE=0x08      #Address for More Than 2 Line LCDs (For Example 4*20)
    Xcurrent = 0        #Cursor X Position
    Ycurrent = 0        #Cursor Y Position

    def __init__(self, RS=15, RW=1, EN=14, D4=13, D5=12, D6=11, D7=10, COL=16, ROW=2):
        #LCD Default Pins
        self.RS = Pin(RS,Pin.OUT)
        self.RW = Pin(RW,Pin.OUT)
        self.EN = Pin(EN,Pin.OUT)
        self.D4 = Pin(D4,Pin.OUT)
        self.D5 = Pin(D5,Pin.OUT)
        self.D6 = Pin(D6,Pin.OUT)
        self.D7 = Pin(D7,Pin.OUT)
        self.COL = COL
        self.ROW = ROW
        self.delay=15
    # A pluse for EN Pin
    def E_Blink(self):
        self.EN.value(1)
        utime.sleep_us(self.delay)
        self.EN.value(0)
        utime.sleep_us(self.delay)
    # Command Data Transfer Function(4Bit Mode)
    def command4bit(self,cmd):
        self.D4.value((cmd & 0x01) >>0)
        self.D5.value((cmd & 0x02) >>1)
        self.D6.value((cmd & 0x04) >>2)
        self.D7.value((cmd & 0x08) >>3)
        self.E_Blink()
    #Command Data Transfer Function
    def command(self,cmd):
        self.RS.value(0)
        self.command4bit(cmd >> 4)
        self.command4bit(cmd & 0x0F)
        utime.sleep_ms(5)
    #Sends RAW DATA to LCD
    def write_data(self,data):
        self.RS.value(1)
        self.command4bit(data >> 4)
        self.command4bit(data & 0x0F)
        utime.sleep_ms(5)
    # Display On Function
    def DspOn(self):
        self.command(self.LCD_DISP_ON)
    # Display Off Function
    def DspOff(self):
        self.command(self.LCD_DISP_OFF)
    # Blink On Function
    def BlinkOn(self):
        self.command(self.LCD_BLINK_ON)
    # Blink Off Function
    def BlinkOff(self):
        self.command(self.LCD_BLINK_OFF)
    # Cursor On Function
    def CursorOn(self):
        self.command(self.LCD_CURSOR_ON)
    #Cursor Off Function
    def CursorOff(self):
        self.command(self.LCD_CURSOR_OFF)
    
    #Screen Clear Function
    def clrscr(self):
        self.command(self.LCD_CLR)
        utime.sleep_ms(1)
    # Cursor Position set Function
    def gotoxy(self,x,y):
        row_addr=[0x00, 0x40, 0x14, 0x54] 
        if (y >= self.ROW):
            y = 0
        Xcurrent = x
        Ycurrent = y
        self.command(0x80 | (x + row_addr[y]))
    #Initializing Function for LCD    
    def init(self):
        FuncCnTrL=0
        utime.sleep_ms(1)
        self.gotoxy(0,0)
        # Changing Address if --> LCD Rows>2 Line
        if (self.ROW > 1):
            FuncCnTrL|= self.LCD_2LINE
        #Starts Commands to set LCD in 4Bit Interface
        self.command4bit(0x03)                              
        utime.sleep_ms(5)
        self.command4bit(0x03)
        utime.sleep_ms(5)
        self.command4bit(0x03)
        utime.sleep_ms(5)
        self.command4bit(0x02)
        utime.sleep_ms(5)
        #Turns Displays on - No Cursor - No Blinking - Position 0,0 - Default Font
    	self.command(0x20 | FuncCnTrL)
        self.command(0x08 | 0x04)
        self.clrscr()
        self.command(0x04 | 0x02)
        utime.sleep_ms(5)
    
    #Puts String on LCD 
    def puts(self,string):
        
        for x in string:
            self.write_data(ord(x))
    
    #Puts String on X,Y Position
    def pos_puts(self,x,y,string):
        self.gotoxy(x,y)
        self.puts(string)