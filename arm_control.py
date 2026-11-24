import config, inputs, kinematics, time
from machine import PWM, ADC, Pin
def safe_duty(servo, duty):
#Make sure the angle is within the range of 0 to 180 degrees
    if config.D_MIN <= duty <= config.D_MAX:
         servo.duty_u16(duty)
    else:
        print(f"Duty cycle {duty} is out of range.")
        return
#Make sure angle set safe
def safe_angle(servo, angle):
    if 0 <= angle <= 180:
        duty = inputs.translate(angle)
        safe_duty(servo, duty)
L1 = 155
L2 = 155

def ITS_ALIVE():
    print("The robot arm is alive and ready to move!")
    #Gets the intial values of the knobs and converts them to x and y coordinates
    x_raw, y_raw = inputs.read_knobs()

    x_cord = ((x_raw / 65535) * config.PAPER_WIDTH) + config.PAPER_X_OFFSET
    y_cord = ((y_raw / 65535) * config.PAPER_HEIGHT) + config.PAPER_Y_OFFSET
   
    #Ugly math
    theta1, theta2 = kinematics.inverse_kinematics(x_cord, y_cord, L1, L2, min_angle_deg=-20, max_angle_deg=160)
    

    print(f"Initial position: x={x_cord:.2f}, y={y_cord:.2f}, theta1={theta1:.2f}, theta2={theta2:.2f}")
    safe_angle(config.shoulder_pwm, theta1)
    safe_angle(config.elbow_pwm, theta2)

    #PEN!
    inputs.pen_control()  # Set the initial pen state
def main():
    """Main entry point to run the robotic arm control."""
    print("Starting Arm Control...")
    while True:
        ITS_ALIVE()
        time.sleep(0.5)
