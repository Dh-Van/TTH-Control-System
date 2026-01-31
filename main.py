import time
from servo_array import Servo_Array
from servo import Servo

# 1. Pick your pin
PINS = ["D2", "D6"]

# servo = Servo("D2", min_us=500, max_us=2600)
# servo.set_angle(0)
# time.sleep(2.5)
# servo.set_angle(180)
# time.sleep(2.5)

servo_array = Servo_Array(PINS, [0, 0], 2)
servo_array.move_servos([0.0, 0.0])
time.sleep(1.0)
servo_array.move_servos([0.0, 1.0])
time.sleep(1.0)
servo_array.move_servos([0.0, 0.0])

print("Servo DONE!")