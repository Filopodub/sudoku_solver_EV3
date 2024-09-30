from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port

class SudokuPlotter:
    def __init__(self, motor_x_port, motor_y_port):
        self.ev3 = EV3Brick()
        self.motor_x = Motor(motor_x_port)
        self.motor_y = Motor(motor_y_port)
        
        # Initialize current positions
        self.current_x = 0
        self.current_y = 0

    def beep(self):
        # Beep to indicate start
        self.ev3.speaker.beep()

    def move_x(self, angle):
        # Move motor_x by a specific angle and update current_x position
        self.motor_x.run_angle(speed=500, rotation_angle=angle)
        self.current_x += angle
    
    def move_y(self, angle):
        # Move motor_y by a specific angle and update current_y position
        self.motor_y.run_angle(speed=500, rotation_angle=angle)
        self.current_y += angle

    def move_to(self, target_x, target_y):
        # Move to a specific position from current_x and current_y
        delta_x = target_x - self.current_x
        delta_y = target_y - self.current_y
        
        # Move X and Y by the calculated deltas
        self.move_x(delta_x)
        self.move_y(delta_y)

    def reset_position(self):
        # Reset both X and Y positions to zero
        self.current_x = 0
        self.current_y = 0

    def get_position(self):
        # Return current X and Y positions
        return self.current_x, self.current_y
