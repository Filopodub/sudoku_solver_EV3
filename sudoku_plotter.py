from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, TouchSensor
from pybricks.parameters import Port
from pybricks.tools import wait


class SudokuPlotter:
    def __init__(self, motor_x_port, motor_y_port, color_sensor_port, touch_sensor_y_port, touch_sensor_x_start_port, touch_sensor_x_end_port, csv_file="scanned_data.csv"):
        self.ev3 = EV3Brick()
        self.motor_x = Motor(motor_x_port)
        self.motor_y = Motor(motor_y_port)
        self.color_sensor = ColorSensor(color_sensor_port)
        self.touch_sensor_y = TouchSensor(touch_sensor_y_port)
        self.touch_sensor_x_start = TouchSensor(touch_sensor_x_start_port)
        self.touch_sensor_x_end = TouchSensor(touch_sensor_x_end_port)
        self.ready = False
        self.current_x = 0
        self.current_y = 0
        self.direction = 1  # 1 for forward, -1 for backward
        self.row_data = []  # Stores data for the current row
        self.csv_file = csv_file
        self.init_csv_file()

    def init_csv_file(self):
        """Initializes the text file and writes the header."""
        with open(self.csv_file, mode="w") as file:
            file.write("Row Data:\n")

    def beep(self):
        """Makes the EV3 beep."""
        self.ev3.speaker.beep()

    def move_x(self, angle):
        """Moves the X motor by the given angle."""
        self.motor_x.run_angle(speed=500, rotation_angle=-angle)
        self.current_x += angle
    
    def move_y(self, angle):
        """Moves the Y motor by the given angle."""
        self.motor_y.run_angle(speed=500, rotation_angle=angle*5)
        self.current_y += angle

    def set_X(self, position):
        """Sets the current X position."""
        self.current_x = position

    def set_Y(self, position):
        """Sets the current Y position."""
        self.current_y = position

    def get_position(self):
        """Returns the current X and Y position."""
        return self.current_x, self.current_y

    def save_value(self):
        """Saves the reflection value at the current position."""
        reflection = self.color_sensor.reflection()
        print(reflection)
        self.row_data.append(reflection)

    def write_row_data(self):
        """Writes the current row's data to the file."""
        # Reverse the data if the direction is backward
        if self.direction == -1:
            self.row_data.reverse()

        with open(self.csv_file, mode="a") as file:
            file.write(",".join(map(str, self.row_data)) + "\n")
        self.row_data = []  # Clear the row data for the next row

    def bumper_handler_X(self, direction, steps_back, step_distance, set_position):
        """Handles the X-axis bumper."""
        self.beep()
        print("Reached bumper; waiting for release...")

        # Write the current row data at both bumpers (start and end)
        self.write_row_data()

        for _ in range(steps_back):
            self.move_x(step_distance)
            wait(200)

        self.beep()
        # Reset position to 0 on release
        self.set_X(set_position)
        self.direction = direction  # Change direction

    def bumper_handler_Y(self, step_distance):
        """Handles the Y-axis bumper."""
        self.beep()
        print("Reached bumper; waiting for release...")

        while self.touch_sensor_y.pressed():
            self.move_y(step_distance)
            wait(100)

        self.beep()
        # Reset position to 0 on release
        self.set_Y(0)
        print("Bumper released; position reset to 0.")

    def go_to_start(self, steps_back, step_distance):
        """Moves to the starting position."""
        while not self.touch_sensor_x_start.pressed():
            self.move_x(step_distance)
            wait(100)

        self.bumper_handler_X(1, steps_back, -step_distance, 0)

        while not self.touch_sensor_y.pressed():
            self.move_y(-step_distance)
            wait(100)

        self.bumper_handler_Y(step_distance)

        self.ready = True
        print("All ready! Let's GOOOOOOOOOOOO!")
        print("Press middle button to start:")
        wait(1000)


    def scanning_cycle(self, speed=100, steps_back=1):
        """Performs the scanning cycle with continuous movement."""
        if not self.ready:
            print("Scanner is not ready. Initialize first.")
            return  

        print("Starting!")
        self.direction = 1  # 1 for forward, -1 for backward
        self.ready = False

        while self.current_y < 2000:
            # Start continuous movement in X direction
            self.motor_x.run(self.direction * speed)

            while not (self.touch_sensor_x_start.pressed() and self.direction == -1) and \
                not (self.touch_sensor_x_end.pressed() and self.direction == 1):
                
                self.save_value()  # Continuously scan color
                wait(100)  # Short delay for sensor reading
                
            # Stop X movement when bumper is reached
            self.motor_x.stop()

            # Handle bumper behavior and direction reversal
            if self.touch_sensor_x_start.pressed() and self.direction == -1:
                self.bumper_handler_X(1, steps_back, -10, 0)
            elif self.touch_sensor_x_end.pressed() and self.direction == 1:
                last_position = self.current_x
                self.bumper_handler_X(-1, steps_back, 10, last_position)

            # Move Y continuously for the next row
            self.motor_y.run_time(speed, 1000)  # Move Y-axis for a fixed duration
            self.current_y += 10  # Approximate movement tracking

            wait(200)  # Small delay between rows

