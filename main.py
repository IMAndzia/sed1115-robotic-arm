"""Entry point for the Raspberry Pi Pico robotic arm.

Copy this file and the project's config.py and kinematics.py to the Pico,
then run main.py with MicroPython. Check the pin assignments and servo
calibration in config.py before powering the servos.
"""

import time

from config import (
    D_MAX,
    D_MIN,
    L1,
    L2,
    PAPER_HEIGHT,
    PAPER_WIDTH,
    PAPER_X_OFFSET,
    PAPER_Y_OFFSET,
    PEN_UP,
    elbow_pwm,
    pen_pwm,
    pen_switch,
    shoulder_pwm,
    x_axis,
    y_axis,
)
from kinematics import inverse_kinematics

POLL_INTERVAL_S = 0.05


def angle_to_duty(angle):
    """Convert a 0..180 degree servo angle to a safe 16-bit PWM duty value."""
    pulse_us = 500 + (2000 * angle / 180)
    duty = int((pulse_us / 20_000) * 65_535)
    return max(D_MIN, min(D_MAX, duty))


def set_servo_angle(servo, angle):
    """Set a servo only when the requested angle is within its safe range."""
    if not 0 <= angle <= 180:
        return False
    servo.duty_u16(angle_to_duty(angle))
    return True


def knobs_to_position():
    """Map the two potentiometers to a point on the configured paper area."""
    x_raw = x_axis.read_u16()
    y_raw = y_axis.read_u16()
    x_mm = (x_raw / 65_535) * PAPER_WIDTH - PAPER_WIDTH / 2 + PAPER_X_OFFSET
    y_mm = (y_raw / 65_535) * PAPER_HEIGHT + PAPER_Y_OFFSET
    return x_mm, y_mm


def update_arm():
    """Read the knobs and move the shoulder and elbow if the target is valid."""
    x_mm, y_mm = knobs_to_position()
    shoulder_angle, elbow_angle = inverse_kinematics(x_mm, y_mm, L1, L2)

    if shoulder_angle is None or elbow_angle is None:
        print("Target is outside the arm's reach; move the knobs to a reachable point.")
        return

    # Do not send either command unless both angles are safe.
    if not (0 <= shoulder_angle <= 180 and 0 <= elbow_angle <= 180):
        print("Target requires an angle outside the configured servo range.")
        return

    set_servo_angle(shoulder_pwm, shoulder_angle)
    set_servo_angle(elbow_pwm, elbow_angle)


def update_pen():
    """Toggle the pen servo on a debounced rising edge of the button."""
    if not hasattr(update_pen, "previous_state"):
        update_pen.previous_state = 0
        update_pen.last_change_ms = time.ticks_ms()
        update_pen.pen_is_down = False

    state = pen_switch.value()
    now = time.ticks_ms()

    if state != update_pen.previous_state and time.ticks_diff(now, update_pen.last_change_ms) >= 30:
        update_pen.last_change_ms = now
        update_pen.previous_state = state
        if state:
            update_pen.pen_is_down = not update_pen.pen_is_down
            duty = 3000 if update_pen.pen_is_down else PEN_UP
            pen_pwm.duty_u16(max(D_MIN, min(D_MAX, duty)))
            print("Pen down" if update_pen.pen_is_down else "Pen up")


def main():
    """Run the arm control loop until interrupted."""
    print("Starting robotic arm. Press Ctrl-C to stop.")
    pen_pwm.duty_u16(max(D_MIN, min(D_MAX, PEN_UP)))

    try:
        while True:
            update_arm()
            update_pen()
            time.sleep(POLL_INTERVAL_S)
    except KeyboardInterrupt:
        print("Stopping arm; raising pen.")
    finally:
        pen_pwm.duty_u16(max(D_MIN, min(D_MAX, PEN_UP)))


if __name__ == "__main__":
    main()
