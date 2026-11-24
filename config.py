from machine import PWM, Pin, ADC
import math
import time
#CONVERTOR

#Arm length
L1 = 155
L2 = 155

#Set up the pins for the knobs to controll the arm
x_axis = ADC(Pin(26))  #X potentiometer on GPIO 26
y_axis = ADC(Pin(27))  #Y potentiometer on GPIO 27



#PWM for shoulder and elbow servos
shoulder_pwm = PWM(Pin(0))# Shoulder servo on GPIO 0
elbow_pwm = PWM(Pin(1)) #Elbow servo on GPIO 1


# Set PWM frequency for arm
shoulder_pwm.freq(50)  # Standard servo frequency 50 Hz
elbow_pwm.freq(50)


#Best guess at min and max duty cycles
D_MIN = 2300  # Minimum allowed duty cycle
D_MAX = 7500  # Maximum allowed duty cycle
PEN_UP = 2300    # Duty cycle for pen up
PEN_DOWN = 3000  # Duty cycle for pen down


pen_switch = Pin(12, Pin.IN, Pin.PULL_DOWN)
pen_pwm = PWM(Pin(2))
pen_pwm.freq(50)  # Standard servo frequency 50 Hz
pen_write = False # False = up, True = down
last_pen_button_state = 0

Maximum_coordinates_x, Maximum_coordinates_y = 200, 200
Minimum_coordinates_x, Minimum_coordinates_y = -200, 50