import pyb
import time

class DoubleStepper:
    def __init__(self, s1_pins, s2_pins):
        self.s1_pins = (pyb.Pin(s1_pins[0], pyb.Pin.OUT_PP), pyb.Pin(s1_pins[1], pyb.Pin.OUT_PP))
        self.s2_pins = (pyb.Pin(s2_pins[0], pyb.Pin.OUT_PP), pyb.Pin(s2_pins[1], pyb.Pin.OUT_PP))
        
        self.s1_position = 0
        self.s2_position = 0
        
    def set_step_high(self):
        self.s1_pins[0].high()
        self.s2_pins[0].high()
        
    def set_step_low(self):
        self.s1_pins[0].low()
        self.s2_pins[0].low()
        
    def set_dir_high(self):
        self.s1_pins[1].high()
        self.s2_pins[1].high()
        
    def set_dir_low(self):
        self.s1_pins[1].low()
        self.s2_pins[1].low()
        
    def move(self, steps, speed_delay=0.0001):
        if steps > 0:
            self.set_dir_high()
            direction = 1
        else:
            self.set_dir_low()
            direction = -1
            
        count = abs(steps)
        for _ in range(count):
            self.set_step_high()
            time.sleep_us(2) # type: ignore
            self.set_step_low()
            
            self.position += direction
            
            time.sleep(speed_delay)
            
        