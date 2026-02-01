from servo import ServoArray
from stepper import DoubleStepper
import time

class Tactile:
    def __init__(self) -> None:
        MY_ROBOT_PINS = [
            "D13", "D2", "D5", "A7", "D7", "D15", "D3"
        ]

        self.robot = ServoArray(pin_order=MY_ROBOT_PINS)
        self.gantry = DoubleStepper(["D50", "D51"])

    def drop_rack(self):
        self.robot.move_all_norm([0] * 7)
        
    def move_next_row(self):
        self.gantry.move(1000)
        
    def run_loop(self, setpoints_list):
        for row in setpoints_list:
            self.move_next_row()
            time.sleep(1)
            self.robot.move_all_norm(row)
            time.sleep(1)
            
    def reset_rack(self):
        self.robot.move_all_norm([0.0] * 7)
        
    def move_gantry_far(self):
        self.gantry.move(-300)

if __name__ == "__main__":
    sample_setpoints = [
        [1, 0, 1, 0, 1, 0, 1],
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        [0.25, 0.5, 0.75, 0.15, 0.25, 0.15, 0.8],
        [1, 0, 1, 0, 1, 0, 1],
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        [0.25, 0.5, 0.75, 0.15, 0.25, 0.15, 0.8],
        [0, 0, 0, 0, 0, 0, 0]
    ]
    
    board = Tactile()
    # board.run_loop(sample_setpoints)
    board.reset_rack()
    # time.sleep(1)
    # board.move_gantry_far()