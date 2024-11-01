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
        self.touch_sensor_x_start = TouchSensor(touch_sensor_x_start_port)  # X-axis start sensor (Port S3)
        self.touch_sensor_x_end = TouchSensor(touch_sensor_x_end_port)  # X-axis end sensor (Port S4)
        self.current_x = 0
        self.current_y = 0
        self.black_count = 0

    def beep(self):
        self.ev3.speaker.beep()
        print("EV3 is Ready")

    def move_x(self, angle):
        self.motor_x.run_angle(speed=500, rotation_angle=-angle)
        self.current_x += angle

    # def move_x(self, speed):
    #     self.motor_x.run(speed)

    def stop_x(self):
        self.motor_x.stop()
    
    def move_y(self, angle):
        self.motor_y.run_angle(speed=500, rotation_angle=angle*5)  # Adjusting movement scale for Y
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

    def set_starting_y_pos(self):
        """
        Move on the Y-axis until the bumper (touch sensor) is pressed,
        then reverse the movement until the bumper is released.
        Finally, reset the Y-axis position to 0.
        """
        # Move forward on the Y-axis until the bumper (touch sensor) is pressed
        while not self.touch_sensor_y.pressed():
            self.move_y(-10)  # Moving forward until bumper is pressed
            print(self.get_position())
            wait(100)

        # Stop and beep when the bumper is pressed
        self.motor_y.stop()
        self.ev3.speaker.beep()
        print("Y Bumper Pressed!")

        # Move back along the Y-axis until the bumper is released
        while self.touch_sensor_y.pressed():
            self.move_y(10)  # Moving backward
            print(self.get_position())
            wait(100)

        # Stop when the bumper is released
        self.motor_y.stop()
        self.ev3.speaker.beep()
        print("Y Bumper Released!")

        # Reset the Y position to 0
        self.current_y = 0
        print("Y position reset to 0.")

    def set_starting_x_pos(self):
        """
        Move on the X-axis until the bumper (touch sensor) is pressed,
        then reverse the movement until the bumper is released.
        Finally, reset the X-axis position to 0.
        """
        # Move forward on the X-axis until the bumper (touch sensor) is pressed
        while not self.touch_sensor_x.pressed():
            self.move_x(10)  # Moving forward until bumper is pressed
            print(self.get_position())
            wait(100)

        # Stop and beep when the bumper is pressed
        self.motor_x.stop()
        self.ev3.speaker.beep()
        print("X Bumper Pressed!")

        # Move back along the X-axis until the bumper is released
        while self.touch_sensor_x.pressed():
            self.move_x(-10)  # Moving backward
            print(self.get_position())
            wait(100)

        # Stop when the bumper is released
        self.motor_x.stop()
        self.ev3.speaker.beep()
        print("X Bumper Released!")

        # Reset the X position to 0
        self.current_x = 0
        print("X position reset to 0.")

    def bumper_testing(self, initial_y_movement=50, initial_x_movement=50):
        """
        Test the bumpers by first moving away from the sensor on both axes
        and then starting the respective processes.
        """
        # Move away from the Y bumper by the initial movement distance
        print("Moving away from Y bumper...")
        self.move_y(initial_y_movement)
        print(self.get_position())
        wait(500)  # Wait to ensure the motor moves fully

        # Perform the starting Y position setup
        print("Starting bumper test to set the Y starting position...")
        self.set_starting_y_pos()

        # Move away from the X bumper by the initial movement distance
        print("Moving away from X bumper...")
        self.move_x(initial_x_movement)
        print(self.get_position())
        wait(500)  # Wait to ensure the motor moves fully

        # Perform the starting X position setup
        print("Starting bumper test to set the X starting position...")
        self.set_starting_x_pos()
        
    def simultaneous_bumper_testing(self, initial_y_movement=50, initial_x_movement=50):
        """
        Move away from both bumpers simultaneously and then set starting positions.
        """
        print("Moving away from both bumpers simultaneously...")
        self.move_y(initial_y_movement)
        self.move_x(-initial_x_movement)

        # Wait for both motors to complete the movement
        wait(500)  # Adjust this wait time as needed

        # Start setting the Y and X starting positions
        print("Starting bumper test for Y and X positions...")
        self.set_starting_y_pos()
        self.set_starting_x_pos()


    def x_bumper_cycle(self):
        """
        Continuous cycle: moves along the X-axis between start and end bumpers.
        """
        # Start the cycle at the start bumper
        self.move_x(200)  # Move forward to reach start bumper
        while True:
            # Move towards the start position
            if self.touch_sensor_x_start.pressed():
                # Stop and reset to start position
                self.stop_x()
                self.ev3.speaker.beep()
                self.current_x = 0
                print("Reached X-axis start; position reset to 0.")

                # Back up a bit and start moving towards the end
                self.move_x(-200)
                wait(200)  # Adjust this delay for the distance needed

            # Move towards the end position
            elif self.touch_sensor_x_end.pressed():
                # Stop at the end position
                self.stop_x()
                self.ev3.speaker.beep()
                print("Reached X-axis end.")

                # Back up a bit and start moving towards the start again
                self.move_x(200)  # Reverse direction to go back to the start
                wait(200)  # Adjust this delay for the distance needed

            wait(50)  # Small delay for sensor polling


    def x_bumper_cycle_with_steps(self, step_distance=10, steps_back=6):
        """
        Continuous cycle along the X-axis between start and end bumpers.
        Moves in steps, scanning color after each step.
        """
        # Set the initial direction to move towards the end bumper
        self.direction = 1  # 1 for forward, -1 for backward
        last_position = 0   # To track the last position before bumper press

        while True:
            # Move a single step in the current direction
            self.move_x(self.direction * step_distance)
            print("Current X position:", self.current_x)

            # Scan color at each step
            self.print_light_intensity()

            # Check if we have reached the start bumper and need to reverse
            if self.touch_sensor_x_start.pressed() and self.direction == -1:
                self.stop_x()
                self.ev3.speaker.beep()
                print("Reached start bumper; waiting for release...")

                # Wait for the start bumper to be released
                for _ in range(steps_back):
                    self.move_x(step_distance)
                    wait(200)

                self.ev3.speaker.beep()
                # Reset position to 0 on release
                self.current_x = 0
                print("Start bumper released; position reset to 0.")
                self.direction = 1  # Change direction to forward

            # Check if we have reached the end bumper and need to reverse
            elif self.touch_sensor_x_end.pressed() and self.direction == 1:
                self.stop_x()
                self.ev3.speaker.beep()
                print("Reached end bumper; waiting for release...")
                last_position = self.current_x

                # Wait for the end bumper to be released
                for _ in range(steps_back):
                    self.move_x(-step_distance)
                    wait(200)

                self.ev3.speaker.beep()
                # Set position to last position before pressing end bumper
                self.current_x = last_position
                print("End bumper released; position set to last position before bumper was pressed.")
                self.direction = -1  # Change direction to backward

            # Small delay between steps
            wait(200)
