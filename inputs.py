from Machine import PWM, ADC, 

def read_knobs():
     """read the values from the potentiometers and convert them to x and y coordinates"""
     x_value = x_axis.read_u16()  #read the X potentiometer value (0-65535)
     y_value = y_axis.read_u16()  #read the Y potentiometer value (0-65535)
    
    
     return x_value, y_value

def translate(angle: float) -> int:
    pulse_width = 500 + (2500 - 500) * angle / 180  #Pulse width equation
    duty_cycle = pulse_width / 20000  #20000 microseconds 
    duty_u16_value = int(duty_cycle * 65535)#Scale to 16-bit range
    duty_u16_value = max(D_MIN, min(D_MAX, duty_u16_value))#clamp(limit it) to safe range
    return duty_u16_value

def pen_control():
     global pen_write, last_pen_button_state
     current_pen_button_state = pen_switch.value()
     if current_pen_button_state == 1 and last_pen_button_state == 0: #have it like this to actaully see its pressed!
            pen_write = not pen_write  #toggle the pen state
            print(f"Pen state changed: {'Ready!' if pen_write else 'Waiting!'}")
            pen_state = PEN_DOWN if pen_write else PEN_UP
            safe_duty(pen_pwm, pen_state)
    
     last_pen_button_state = current_pen_button_state


pen_switch = Pin(12, Pin.IN, Pin.PULL_DOWN)
pen_write = False # False = up, True = down
last_pen_button_state = 0