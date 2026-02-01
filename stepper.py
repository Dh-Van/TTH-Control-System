import pyb # type: ignore
import time

class Stepper:
    def __init__(self, stepper_pins):
        self.pins = (pyb.Pin(stepper_pins[0], pyb.Pin.OUT_PP), pyb.Pin(stepper_pins[1], pyb.Pin.OUT_PP))
        
        self.position = 0
        
        
    def move(self, steps, speed_delay=1600):
        if steps > 0:
            self.pins[1].high()
            direction = 1
        else:
            self.pins[1].low()
            direction = -1
            
        count = abs(steps)
        for _ in range(count):
            self.pins[0].high()
            time.sleep_us(2) # type: ignore
            self.pins[0].low()
            
            self.position += direction
            
            time.sleep_us(speed_delay) # type: ignore
            
    def get_position(self):
        return self.position
            
        
if __name__ == "__main__":
    stepper = Stepper(["D51", "D50"])
    stepper.move(10000000)