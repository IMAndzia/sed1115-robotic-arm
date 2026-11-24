def safe_duty(servo, duty):
#Make sure the angle is within the range of 0 to 180 degrees
    if D_MIN <= duty <= D_MAX:
         servo.duty_u16(duty)
    else:
        print(f"Duty cycle {duty} is out of range.")
        return
#Make sure angle set safe
def safe_angle(servo, angle):
    if 0 <= angle <= 180:
        duty = translate(angle)
        safe_duty(servo, duty)

def clamp_paper_position(x_cord, y_cord):
    half_width = PAPER_WIDTH / 2

    x_cord = max(PAPER_X_OFFSET - half_width,
                 min(PAPER_X_OFFSET + half_width, x_cord))
    y_cord = max(PAPER_Y_OFFSET,
                 min(PAPER_Y_OFFSET + PAPER_HEIGHT, y_cord))

    return x_cord, y_cord
def ITS_ALIVE():
    print("The robot arm is alive and ready to move!")
    #Gets the intial values of the knobs and converts them to x and y coordinates
    x_raw, y_raw = read_knobs()

    x_cord = (x_raw / 65535) * PAPER_WIDTH - (PAPER_WIDTH / 2) + PAPER_X_OFFSET
    y_cord = (y_raw / 65535) * PAPER_HEIGHT + PAPER_Y_OFFSET
    x_cord, y_cord = clamp_paper_position(x_cord, y_cord)

    #Ugly math
    theta1, theta2 = inverse_kinematics(x_cord, y_cord)
    if theta1 is None or theta2 is None:
        print("Initial position is out of reach. Please adjust the knobs.")
        return

    print(f"Initial position: x={x_cord:.2f}, y={y_cord:.2f}, theta1={theta1:.2f}, theta2={theta2:.2f}")
    safe_angle(shoulder_pwm, theta1)
    safe_angle(elbow_pwm, theta2)

    #PEN!
    pen_control()  # Set the initial pen state
def main():
    """Main entry point to run the robotic arm control."""
    print("Starting Arm Control...")
    while True:
        ITS_ALIVE()
        time.sleep(0.5)
if __name__ == "__main__": 
    main()