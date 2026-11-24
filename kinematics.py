
import math

L1 = 155
L2 = 155


def inverse_kinematics(
    x_mm: float,
    y_mm: float,
    L1: float = L1,
    L2: float = L2,
    min_angle_deg: float = -180.0,
    max_angle_deg: float = 180.0,
):
    """Convert  coordinates into shoulder and elbow angles in degrees."""
    x_pos = float(x_mm)
    y_pos = float(y_mm)

    l1 = float(L1)
    l2 = float(L2)

    dist_sq = x_pos * x_pos + y_pos * y_pos
    dist = math.sqrt(dist_sq) if dist_sq > 0.0 else 0.0

    max_span = l1 + l2
    if dist > max_span and dist > 0.0:
        scale_factor = max_span / dist
        x_pos *= scale_factor
        y_pos *= scale_factor
        dist_sq = x_pos * x_pos + y_pos * y_pos

    cos_elbow = (dist_sq - l1 * l1 - l2 * l2) / (2.0 * l1 * l2)
    cos_elbow = max(-1.0, min(1.0, cos_elbow))
    elbow_rad = math.acos(cos_elbow)
    elbow_deg = math.degrees(elbow_rad)

    k1 = l1 + l2 * math.cos(elbow_rad)
    k2 = l2 * math.sin(elbow_rad)
    shoulder_rad = math.atan2(y_pos, x_pos) - math.atan2(k2, k1)
    shoulder_deg = math.degrees(shoulder_rad)

    shoulder_deg = max(min_angle_deg, min(max_angle_deg, shoulder_deg))
    elbow_deg = max(min_angle_deg, min(max_angle_deg, elbow_deg))

    return shoulder_deg, elbow_deg


