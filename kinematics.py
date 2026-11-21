import math

def inverse_kinematics(x_mm: float, y_mm: float, L1: float, L2: float):
    """
    Converts Cartesian (x_mm, y_mm) coordinates into shoulder and elbow angles (in degrees)
    using the Law of Cosines. Returns (None, None) if the target is out of reach.
    """
    distance = math.hypot(x_mm, y_mm)

    # Check physical workspace boundaries and prevent ZeroDivisionError at (0, 0)
    if distance == 0 or distance > (L1 + L2) or distance < abs(L1 - L2):
        return None, None

    # Calculate elbow angle (theta2) with floating-point clamping to prevent ValueError
    cos_theta2 = (distance**2 - L1**2 - L2**2) / (2 * L1 * L2)
    cos_theta2 = max(-1.0, min(1.0, cos_theta2))
    theta2 = math.acos(cos_theta2)

    # Calculate shoulder angle (theta1) with floating-point clamping
    cos_alpha = (L2**2 + distance**2 - L1**2) / (2 * L2 * distance)
    cos_alpha = max(-1.0, min(1.0, cos_alpha))
    theta1 = math.atan2(y_mm, x_mm) - math.acos(cos_alpha)

    return math.degrees(theta1), math.degrees(theta2)