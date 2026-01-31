import time
from servo_array import Servo_Array
# 1. Pick your pin
PINS = ["D2", "D4"]

servo_array = Servo_Array(PINS, [0, 0], 2)

servo_array.move_servos([1.0, 1.0])
time.sleep(1)
servo_array.move_servos([0.0, 0.0])