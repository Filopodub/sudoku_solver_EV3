#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port, Button
from pybricks.tools import wait
from sudoku_plotter import SudokuPlotter

# Define a constant for the movement angle
MOVEMENT_ANGLE = 2  # You can change this value to adjust all movements
TESTING_STEPS = 30

# Create an instance of SudokuPlotter with motors on Ports A and B, and the color sensor on Port 4
sudoku_plotter = SudokuPlotter(Port.A, Port.B, Port.S4, step_size=20)
ev3 = EV3Brick()

# Beep to indicate the start of the program
sudoku_plotter.beep()

while True:
    # Wait for a button press
    pressed_buttons = ev3.buttons.pressed()

    # Control motor_x with left and right buttons
    if Button.LEFT in pressed_buttons:
        sudoku_plotter.move_x(MOVEMENT_ANGLE)  # Use the constant for the movement angle
        print(sudoku_plotter.get_position())  # Print current position after moving motor_x

    elif Button.RIGHT in pressed_buttons:
        sudoku_plotter.move_x(-MOVEMENT_ANGLE)  # Use the constant for reverse movement
        print(sudoku_plotter.get_position())  # Print current position after moving motor_x

    # Control motor_y with up and down buttons
    elif Button.UP in pressed_buttons:
        sudoku_plotter.move_y(MOVEMENT_ANGLE)  # Use the constant for the movement angle
        print(sudoku_plotter.get_position())  # Print current position after moving motor_y

    elif Button.DOWN in pressed_buttons:
        sudoku_plotter.move_y(-MOVEMENT_ANGLE)  # Use the constant for reverse movement
        print(sudoku_plotter.get_position())  # Print current position after moving motor_y

    # Run the main movement with the middle button
    elif Button.CENTER in pressed_buttons:
        # Move x times on the X-axis using the movement constant
        for _ in range(TESTING_STEPS):
            sudoku_plotter.move_x(MOVEMENT_ANGLE)  # Move forward
            print(sudoku_plotter.get_position())  # Print current position after moving motor_y
            sudoku_plotter.print_light_intensity()  # Detect and print the current light intensity
            wait(100)  # Optional: Add a small delay between movements to allow for detection

        # Move back to the starting position on the X-axis
        for _ in range(TESTING_STEPS):
            sudoku_plotter.move_x(-MOVEMENT_ANGLE)  # Move backward
            print(sudoku_plotter.get_position())  # Print current position after moving motor_y
            sudoku_plotter.print_light_intensity()  # Detect and print the current light intensity
            wait(100)  # Optional: Add a small delay between movements to allow for detection

        # Stop the motors
        sudoku_plotter.motor_x.stop()
        sudoku_plotter.motor_y.stop()

        # Indicate completion
        sudoku_plotter.ev3.speaker.beep()  # Beep again to indicate completion

        sudoku_plotter.print_black_count() 

    
    

    # Optional: Add a small wait to avoid spamming the button checks
    wait(100)


