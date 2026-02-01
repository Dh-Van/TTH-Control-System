import pyb # type: ignore
from giga_pinmap import SERVO_MAP
import time

# Registry to ensure we don't re-initialize a hardware timer already in use
_TIMER_POOL = {}

class Servo:
    def __init__(self, pin_name):
        tid, chid, af_idx = SERVO_MAP[pin_name]
        
        if tid not in _TIMER_POOL:
            # For Timer 1 and 8, sometimes freq=50 doesn't set the deadtime correctly
            # Let's use a standard 16-bit period for predictable results
            _TIMER_POOL[tid] = pyb.Timer(tid, freq=50)
            
        self.tim = _TIMER_POOL[tid]
        self.pin = pyb.Pin(pin_name, mode=pyb.Pin.ALT, af=af_idx)
        
        # Explicitly setting Timer.PWM here is key
        self.ch = self.tim.channel(chid, pyb.Timer.PWM, pin=self.pin)

    def set_angle(self, angle):
        angle = max(0, min(180, angle))
        target_us = 500 + (angle / 180.0 * 2000)
        
        # Use pulse_width_percent if pulse_width is failing on certain timers
        # 500us / 20000us = 2.5% duty
        # 2500us / 20000us = 12.5% duty
        duty = (target_us / 20000.0) * 100
        
        # On some Giga builds, pulse_width() only works if the value is < period
        ticks = int((target_us / 20000.0) * self.tim.period())
        self.ch.pulse_width(ticks)
        
class ServoArray:
    def __init__(self, pin_order=None):
        """
        pin_order: Optional list of pin names to define index 0, 1, 2...
        If None, it uses the keys from SERVO_MAP in default order.
        """
        self.servos = {}
        # This list stores the order so that setpoints[0] works reliably
        self.index_map = [] 
        
        print("--- Initializing Servo Array ---")
        
        # Use provided order, or fall back to dictionary keys
        target_pins = pin_order if pin_order else list(SERVO_MAP.keys())
        
        for pin_name in target_pins:
            try:
                # Create the Servo object
                new_servo = Servo(pin_name)
                self.servos[pin_name] = new_servo
                # Add to our ordered list for indexed access
                self.index_map.append(new_servo)
                print(f"[OK] {pin_name} linked to index {len(self.index_map)-1}")
            except Exception as e:
                print(f"[FAILED] {pin_name}: {e}")
                self.index_map.append(None) # Placeholder to keep indices correct

    def move_one(self, pin_name, angle):
        if pin_name in self.servos:
            self.servos[pin_name].set_angle(angle)

    def move_all(self, angle):
        for s_obj in self.servos.values():
            if s_obj: s_obj.set_angle(angle)
            
    def move_one_norm(self, pin_name, setpoint):
        if pin_name in self.servos:
            self.servos[pin_name].set_angle(setpoint * 180)
            
    def move_all_norm(self, setpoints):
        """Maps a list of setpoints [0.1, 0.5...] to the index_map order."""
        for i, val in enumerate(setpoints):
            if i < len(self.index_map) and self.index_map[i]:
                self.index_map[i].set_angle(val * 180)
            
    def stop_all(self):
        """Stops the PWM signal on all pins, making servos go limp."""
        for s_obj in self.servos.values():
            if s_obj: s_obj.ch.pulse_width(0)
        print("All servos deactivated.")

    def kill_timers(self):
        """Completely shuts down the hardware timers."""
        for tid in _TIMER_POOL:
            _TIMER_POOL[tid].deinit()
        _TIMER_POOL.clear() # Clear the registry for fresh starts
        print("Hardware Timers destroyed.")
        
# D8, D12, D9, D15, D17, D19. D20, A2,    no work
# D2, D3, D6, D13, D15, A7, D7, D5, D11
if __name__ == "__main__":
    test_servo = Servo("D7")
    test_servo.set_angle(0)
    time.sleep(1)
    test_servo.set_angle(160)
    time.sleep(1)
    
'''
D13
D2
D5
A7
D7
D15
D3
'''