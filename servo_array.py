from servo import Servo

class Servo_Array():
    def __init__(self, dio_list, offset_list, num_servos = 15):
        self.servos: list[tuple[Servo, float]] = []
        for i in range(0, num_servos):
            servo = Servo(dio_list[i])
            offset = offset_list[i]
            self.servos.append((servo, offset))
            
            
    # Setpoint -> [0, 1]
    def move_servos(self, setpoints):
        for i, setpoint in enumerate(setpoints):
            servo, offset = self.servos[i]
            angle_raw = setpoint * 180
            angle_offset = min(max(angle_raw + offset, 0), 180)
            servo.set_angle(angle_offset)
            
