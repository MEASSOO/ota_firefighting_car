# code here
from machine import PWM, Pin,ADC
import time
import utime
from dcmotor import DCMotor
from servo import Servo
from ota import OTAUpdater

# initialize OTA
firmware_url = "https://raw.githubusercontent.com/MEASSOO/ota_firefighting_car/"





# Initialize Pins
testLed = Pin(2, Pin.OUT)


#water_level = ADC(Pin(25, Pin.IN))
m1_1 = Pin(4, Pin.OUT)
m1_2 = Pin(5, Pin.OUT)
m1_en = PWM(Pin(32), freq=1000)
m2_1 = Pin(22, Pin.OUT)
m2_2 = Pin(23, Pin.OUT)
m2_en = PWM(Pin(33), freq=1000)
r_motor = DCMotor(m1_1, m1_2, m1_en)
l_motor = DCMotor(m2_1, m2_2, m2_en)
pump = Pin(13, Pin.OUT) # 19 to 13
servo = Servo(pin=21)
l_sensor = ADC(Pin(25, Pin.IN))
c_sensor = ADC(Pin(14, Pin.IN)) ## change 
r_sensor = ADC(Pin(27, Pin.IN))

#l_sensor.atten(ADC.ATTN_11DB)
#c_sensor.atten(ADC.ATTN_11DB)
#r_sensor.atten(ADC.ATTN_11DB)

#l_sensor.width(ADC.WIDTH_12BIT)
#c_sensor.width(ADC.WIDTH_12BIT)
#r_sensor.width(ADC.WIDTH_12BIT)


#water_level.atten(ADC.ATTN_11DB)
#water_level.width(ADC.WIDTH_12BIT)

#servo.move(90)





def Feedback():
    valR = r_sensor.read()
    valL = l_sensor.read()
    valC = c_sensor.read()
    if (valC < valR and valC < valL):
        print("Center")
        TurnForward()
    elif (valR < valC and valR < valL):
        print("Right")
        TurnRight()
    elif (valL < valC and valL < valR):
        print("Left")
        TurnLeft()
    else:
        print("Stop")
        TurnStop()
        
    check_fire()



def CheckTank():
    
    val = water_level.read()
    
    if val < 1500:
        print("Fill The Tank!")
    

def MovementOfServo():
    
    servo.move(45)
    time.sleep(0.5)
    servo.move(135)
    time.sleep(0.5)
    
    

    

# functions

def TurnLeft():
    
    # Make Robot To Go To Left Drive
    r_motor.forward(100)
    l_motor.stop()
    
def TurnRight():
    # Make Robot To Go To Right Drive
    l_motor.forward(100)
    r_motor.stop()
    
def TurnForward():
    # Make Robot To Go To Forward
    l_motor.forward(100)
    r_motor.forward(100)

def TurnStop():
    # Make Robot To Stop From Motion
    l_motor.stop()
    r_motor.stop()

def StartPumpWater():
    # Make Robot Pump Water on Fire
    MovementOfServo()
    pass

def StopPumpWater():
    # Make Robot Stop Pump Water
    pass

def check_fire():
    
    #check from where fire -> which sensor that close to near fire to take command
    c_read = c_sensor.read()
    l_read = l_sensor.read()
    r_read = r_sensor.read()
    print(c_read)
    if (c_read < 2000 or l_read < 2000 or r_read < 2000):
        
        print("Fire near!!!!", c_read)
        TurnStop()
        StartPumpWater()
    else:
        pass




pump.on()


time.sleep(5)


pump.off()

time.sleep(5)
pump.on()

time.sleep(5)

pump.off()
#while True:
    
 #   Feedback()
  #time.sleep(0.25)
 
 
while True:

    ota_updater = OTAUpdater("Orange_AB2F", "6mE8R3iBhD4M", firmware_url, "boot.py")
    ota_updater.download_and_install_update_if_available()

    time.sleep(5)

    
 

