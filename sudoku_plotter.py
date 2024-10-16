from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port

class SudokuPlotter:
    def __init__(self, motor_x_port, motor_y_port, color_sensor_port, step_size=20):
        self.ev3 = EV3Brick()
        self.motor_x = Motor(motor_x_port)
        self.motor_y = Motor(motor_y_port)
        self.color_sensor = ColorSensor(color_sensor_port)  # Assuming you are using a color sensor
        self.current_x = 0
        self.current_y = 0
        self.black_count = 0  # Count of detected black lines

    def beep(self):
        self.ev3.speaker.beep()

    def move_x(self, angle):
        self.motor_x.run_angle(speed=500, rotation_angle=angle)
        self.current_x += angle
    
    def move_y(self, angle):
        self.motor_y.run_angle(speed=500, rotation_angle=angle)
        self.current_y += angle

    def move_to(self, target_x, target_y):
        delta_x = target_x - self.current_x
        delta_y = target_y - self.current_y
        self.move_x(delta_x)
        self.move_y(delta_y)

    def reset_position(self):
        self.current_x = 0
        self.current_y = 0

    def get_position(self):
        return self.current_x, self.current_y

    def print_light_intensity(self):
         # Read the current reflected light intensity from the color sensor
        light_intensity = self.color_sensor.reflection()
        
        # Set a threshold to distinguish between black (low reflection) and white (high reflection)
        threshold = 65  # Adjust based on testing; lower for darker black
        
        if light_intensity < threshold:
            self.black_count += 1  # Increment the black count
            print("Detected Black Line")
            return "Black"
        else:
            print("Detected White Area")
            return "White"


    def print_black_count(self):
        print("Number of Black Lines Detected:", self.black_count/2)
        self.black_count = 0  # Reset the count after printing



