import pyb # type: ignore
from giga_pinmap import SERVO_MAP

class Servo:
    """
    A precise wrapper for STM32 Servos using hardware timers.
    """
    def __init__(self, pin_name, min_us=500, max_us=2500, max_angle=180):
        self.pin = pyb.Pin(pin_name)
        timer_id, channel_id = SERVO_MAP[pin_name]
        
        self.min_us = min_us
        self.max_us = max_us
        self.max_angle = max_angle
        
        # 1. Setup the Hardware Timer at 50Hz (20ms period)
        self.tim = pyb.Timer(timer_id, freq=50)
        self.ch = self.tim.channel(channel_id, pyb.Timer.PWM, pin=self.pin)
        
        # 2. Calculate Ticks per Microsecond (Precision Math)
        # We need this to convert microseconds directly to hardware clock ticks.
        # Timer period is 20,000 microseconds (1/50Hz).
        self.max_ticks = self.tim.period()
        self.ticks_per_us = self.max_ticks / 20000.0

    def set_angle(self, angle):
        """Moves the servo to the specified angle (deg)."""
        # 1. Safety Clamps
        if angle < 0: angle = 0
        if angle > self.max_angle: angle = self.max_angle
        
        # 2. Map Angle to Microseconds
        # Linear interpolation: result = min + (fraction * range)
        fraction = angle / self.max_angle
        target_us = self.min_us + (fraction * (self.max_us - self.min_us))
        
        # 3. Write to Hardware
        self._write_us(target_us)

    def _write_us(self, us):
        """Internal function to write raw microseconds."""
        ticks = int(us * self.ticks_per_us)
        self.ch.compare(ticks)

    def detach(self):
        """Stops the PWM signal. The servo will go limp/silent."""
        self.ch.pulse_width_percent(0)