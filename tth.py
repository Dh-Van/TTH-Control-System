from servo import ServoArray
from stepper import Stepper
import json, time, sys

class TTH:
    SERVO_PINS = [
        "D13", "D2", "D5", "A7", "D7", "D15", "D3"
    ]
    
    SERVO_POSITIONS = [2, 3, 5, 6, 8, 10, 11]
    SERVO_RELATIVE_POSITION = [position % 2 for position in SERVO_POSITIONS]
    
    STEPS_PER_INCH = 3246.48973
    
    def __init__(self, source, is_json = False) -> None:
        self.servo_array = ServoArray(self.SERVO_PINS)
        self.setpoints = []
        
        self.gantry = Stepper(["D51", "D50"])
        self.position = 0
        
        if(is_json):
            with open(source, 'r') as f:
                data = json.load(f)    
                self.setpoints = self.parse_json(data)
        else:
            self.setpoints = source
            
        self.servo_array.move_all_norm([0] * 7)
        
        self.true_position = 0
            
    def parse_json(self, json_data):        
        map_size = 15
        map = [[0.0 for _ in range(map_size)] for _ in range(map_size)]
        
        for pin in json_data['pins']:
            row = pin['row']
            column = pin['col']
            height = pin['height']
            
            map[row][column] = height
            
        final_map = []
        for servo_index in self.SERVO_POSITIONS:
            final_map.append(map[servo_index])
            
        return final_map
    
    # Default will be one row
    def move_gantry(self, steps = None):
        if(steps is None):
            steps = -self.STEPS_PER_INCH
        self.gantry.move(steps)
        self.true_position += steps
        time.sleep(0.5)
    
    def set_servos_position(self, setpoints):
        self.servo_array.move_all_norm(setpoints)
        time.sleep(0.5)
            
    def move_row(self):
            # 1. Grab the "current" column of data (Front)
            # If position is valid, grab the column 'self.position' from every servo row
            if 0 <= self.position < 15:
                front_row = [self.setpoints[i][self.position] for i in range(7)]
            else:
                front_row = [0.0] * 7
                
            # 2. Grab the "previous" column of data (Back)
            # If position-1 is valid, grab the column 'self.position-1' from every servo row
            if 0 <= self.position - 1 < 15:
                back_row = [self.setpoints[i][self.position - 1] for i in range(7)]
            else:
                back_row = [0.0] * 7
                
            curr_setpoints = [0.0] * 7
            
            for idx, relative_pos in enumerate(self.SERVO_RELATIVE_POSITION):
                if(relative_pos == 0):
                    # Back row servos get the OLD column data (lagging)
                    curr_setpoints[idx] = back_row[idx]
                elif(relative_pos == 1):
                    # Front row servos get the CURRENT column data
                    curr_setpoints[idx] = front_row[idx]
                    
            return curr_setpoints
        
    def cancel(self):
        try:
            self.move_gantry(-self.true_position)
        except KeyboardInterrupt:
            sys.exit(0)
        
    def visualize(self):
        for i in range(9):
            self.position = i
            current_setpoints = self.move_row()
            # self.set_servos_position(current_setpoints)
            self.set_servos_position([0.9] * 7)
            self.set_servos_position([0.0] * 7)
            self.move_gantry()
            
            print(self.true_position)
                
        self.move_gantry(-self.true_position)
        

if __name__ == "__main__":
    time.sleep(2)
    tth = TTH("test_map.json", True)
    # tth.visualize()
    # tth.move_gantry(7 * tth.STEPS_PER_INCH)
    
    tth.servo_array.move_all_norm([0] * 7)
    
    # time.sleep(10000)
    
    # tth.servo_array.stop_all()
    # tth.servo_array.kill_timers()