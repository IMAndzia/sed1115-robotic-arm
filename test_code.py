import sys
import unittest
from unittest.mock import MagicMock, patch

machine_mock = MagicMock()
machine_mock.PWM.side_effect = (MagicMock(), MagicMock(), MagicMock())
sys.modules["machine"] = machine_mock
import ROBOT_ARM


class TestServoAnglesAtPoints(unittest.TestCase):
    def setUp(self):
        ROBOT_ARM.shoulder_pwm.reset_mock()
        ROBOT_ARM.elbow_pwm.reset_mock()

    @patch("ROBOT_ARM.read_knobs")
    def test_servo_angles_at_sample_points(self, mock_read_knobs):
        sample_points = (
            (155, 155, 0, 90),
            (0, 155, 30, 120),
            (0, 310, 90, 0),
        )

        for x, y, expected_shoulder, expected_elbow in sample_points:
            with self.subTest(x=x, y=y):
                mock_read_knobs.return_value = (
                    (x + ROBOT_ARM.L1 + ROBOT_ARM.L2) / (2 * (ROBOT_ARM.L1 + ROBOT_ARM.L2)) * 65535,
                    (y + ROBOT_ARM.L1 + ROBOT_ARM.L2) / (2 * (ROBOT_ARM.L1 + ROBOT_ARM.L2)) * 65535,
                )
                ROBOT_ARM.shoulder_pwm.reset_mock()
                ROBOT_ARM.elbow_pwm.reset_mock()

                ROBOT_ARM.ITS_ALIVE()

                x_actual = (
                    mock_read_knobs.return_value[0] / 65535
                    * (2 * (ROBOT_ARM.L1 + ROBOT_ARM.L2))
                    - (ROBOT_ARM.L1 + ROBOT_ARM.L2)
                )
                y_actual = (
                    mock_read_knobs.return_value[1] / 65535
                    * (2 * (ROBOT_ARM.L1 + ROBOT_ARM.L2))
                    - (ROBOT_ARM.L1 + ROBOT_ARM.L2)
                )
                shoulder_angle, elbow_angle = ROBOT_ARM.inverse_kinematics(x_actual, y_actual)

                self.assertAlmostEqual(shoulder_angle, expected_shoulder, places=2)
                self.assertAlmostEqual(elbow_angle, expected_elbow, places=2)
                shoulder_duty = ROBOT_ARM.translate(shoulder_angle)
                elbow_duty = ROBOT_ARM.translate(elbow_angle)
                ROBOT_ARM.shoulder_pwm.duty_u16.assert_called_once_with(shoulder_duty)
                ROBOT_ARM.elbow_pwm.duty_u16.assert_called_once_with(elbow_duty)

                print(
                    f"Point ({x}, {y}) mm: shoulder={shoulder_angle:.2f} degrees "
                    f"(PWM duty {shoulder_duty}), elbow={elbow_angle:.2f} degrees "
                    f"(PWM duty {elbow_duty})"
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
