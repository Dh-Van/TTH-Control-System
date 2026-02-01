import pyb
import machine

def deep_scan():
    print("--- Scanning Pin Board Names ---")
    # This looks at the actual attributes of the Board object
    names = [item for item in dir(machine.Pin.board) if not item.startswith("_")]
    print(f"Found {len(names)} pins: {names}")
    
    print("\n--- Testing PWM on Found Pins ---")
    for name in names:
        try:
            # Try to get the pin object from the board namespace
            p_obj = getattr(machine.Pin.board, name)
            
            # Try to see if pyb.Timer can associate with it
            # We'll try to find which timer/channel it's on by brute force
            for t_id in [1, 2, 3, 4, 5, 8, 12, 15]:
                try:
                    tim = pyb.Timer(t_id, freq=50)
                    # This is the test: can we attach a channel to this pin object?
                    for ch_id in range(1, 5):
                        try:
                            ch = tim.channel(ch_id, pyb.Timer.PWM, pin=p_obj)
                            print(f"SUCCESS: Pin {name} -> Timer {t_id}, Channel {ch_id}")
                            ch.pulse_width(0)
                            tim.deinit()
                        except:
                            continue
                    tim.deinit()
                except:
                    continue
        except Exception as e:
            continue

deep_scan()