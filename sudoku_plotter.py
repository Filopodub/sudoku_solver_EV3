from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, TouchSensor
from pybricks.parameters import Port
from pybricks.tools import wait

class SudokuPlotter:
    def __init__(self, motor_x_port, motor_y_port, color_sensor_port, touch_sensor_y_port, touch_sensor_x_start_port, touch_sensor_x_end_port):
        self.ev3 = EV3Brick()
        self.motor_x = Motor(motor_x_port)
        self.motor_y = Motor(motor_y_port)
        self.color_sensor = ColorSensor(color_sensor_port)
        self.touch_sensor_y = TouchSensor(touch_sensor_y_port)
        self.touch_sensor_x_start = TouchSensor(touch_sensor_x_start_port)
        self.touch_sensor_x_end = TouchSensor(touch_sensor_x_end_port)
        self.current_x = 0
        self.current_y = 0
        self.black_count = 0

    def beep(self):
        self.ev3.speaker.beep()
        print("EV3 is Ready")

    def move_x(self, angle):
        self.motor_x.run_angle(speed=500, rotation_angle=-angle)
        self.current_x += angle
    
    def move_y(self, angle):
        self.motor_y.run_angle(speed=500, rotation_angle=angle*5)  # Adjusting movement scale for Y
        self.current_y += angle

    def set_X(self, position):
        self.current_x = 0

    def set_Y(self, position):
        self.current_y = 0

    def get_position(self):
        return self.current_x, self.current_y

    def print_light_intensity(self):
        light_intensity = self.color_sensor.reflection()
        threshold = 64  # Adjust based on testing
        if light_intensity < threshold:
            self.black_count += 1
            print("Detected Black Line")
        else:
            print("Detected White Area")

    def print_black_count(self):
        print("Number of Black Lines Detected:", self.black_count)
        self.black_count = 0  # Reset after printing

    def sensor_testing(self, movement_angle, steps):
        """
        Move along the X-axis until the bumper (touch sensor) is pressed.
        """
        for _ in range(steps):
            if self.touch_sensor_y.pressed() or self.touch_sensor_x.pressed():
                print("Touch sensor pressed, stopping movement.")
                break  # Stop if either bumper is pressed
            self.move_x(movement_angle)
            print(self.get_position())
            self.print_light_intensity()
            wait(100)

        self.motor_x.stop()
        self.ev3.speaker.beep()



    def bumper_handler_X(self, direction, steps_back, step_distance, set_position):
        self.beep()
        print("Reached bumper; waiting for release...")

        # Wait for the bumper to be released
        for _ in range(steps_back):
            self.move_x(step_distance)
            wait(200)

        self.beep()
        # Reset position to 0 on release
        self.set_X(set_position)
        print("Bumper released; position reset to 0.")
        self.direction = direction  # Change direction

    def bumper_handler_Y(self, step_distance):
        self.beep()
        print("Reached bumper; waiting for release...")

        # Wait for the bumper to be released
        while self.touch_sensor_y.pressed():
            self.move_y(step_distance)  # Moving backward
            wait(100)

        self.beep()
        # Reset position to 0 on release
        self.set_Y(0)
        print("Bumper released; position reset to 0.")

    def go_to_start(self, steps_back, step_distance):

        while not self.touch_sensor_x_start.pressed():
            self.move_x(-step_distance)
            wait(100)

        self.bumper_handler_X(1, steps_back, step_distance, 0)

        while not self.touch_sensor_y.pressed():
            self.move_y(-step_distance)
            wait(100)

        self.bumper_handler_Y(step_distance)

        print("All ready! Lets GOOOOOOOOOOOO!")
        wait(1000)

    def scanning_cycle(self, step_distance=10, steps_back=6):
        self.go_to_start(steps_back, step_distance)
        
        # Set the initial direction to move towards the end bumper
        self.direction = 1  # 1 for forward, -1 for backward
        last_position = 0   # To track the last position before bumper press

        # while self.current_y < end_value:
        while True:
            # Move a single step in the current direction
            self.move_x(self.direction * step_distance)
            print("Current position:", self.get_position())

            # Scan color at each step
            # self.print_light_intensity()

            # Check if we have reached the start bumper and need to reverse
            if self.touch_sensor_x_start.pressed() and self.direction == -1:
                self.bumper_handler_X(1, steps_back, step_distance, 0)
                self.move_y(step_distance)
                
            # Check if we have reached the end bumper and need to reverse
            elif self.touch_sensor_x_end.pressed() and self.direction == 1:
                last_position = self.current_x
                self.bumper_handler_X(-1, steps_back, -step_distance, last_position)
                self.move_y(step_distance)
                
            # Small delay between steps
            wait(200)
