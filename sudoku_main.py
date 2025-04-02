#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port, Button
from pybricks.tools import wait
from sudoku_plotter import SudokuPlotter

# Define a constant for the movement angle
MOVEMENT_ANGLE = 10  # You can change this value to adjust all movements
TESTING_STEPS = 30

# Create an instance of SudokuPlotter with motors on Ports A and B, and the color sensor on Port 4
# motor_x_port, motor_y_port, color_sensor_port, touch_sensor_y_port, touch_sensor_x_start_port, touch_sensor_x_end_port
sudoku_plotter = SudokuPlotter(Port.D, Port.A, Port.S4, Port.S1, Port.S2, Port.S3)
ev3 = EV3Brick()

# Beep to indicate the start of the program
sudoku_plotter.beep()
sudoku_plotter.go_to_start()

while True:
    # Wait for a button press
    pressed_buttons = ev3.buttons.pressed()

    # Control motor_x with left and right buttons
    if Button.LEFT in pressed_buttons:
        sudoku_plotter.motor_x.run_angle(200, MOVEMENT_ANGLE)  # Move motor_x left by the defined angle
        print(sudoku_plotter.get_position())  # Print current position after moving motor_x

    elif Button.RIGHT in pressed_buttons:
        sudoku_plotter.motor_x.run_angle(200, -MOVEMENT_ANGLE)  # Move motor_x right by the defined angle
        print(sudoku_plotter.get_position())  # Print current position after moving motor_x

    # Control motor_y with up and down buttons
    elif Button.UP in pressed_buttons:
        sudoku_plotter.motor_y.run_angle(200, MOVEMENT_ANGLE)  # Move motor_y up by the defined angle
        print(sudoku_plotter.get_position())  # Print current position after moving motor_y

    elif Button.DOWN in pressed_buttons:
        sudoku_plotter.motor_y.run_angle(200, -MOVEMENT_ANGLE)  # Move motor_y down by the defined angle
        print(sudoku_plotter.get_position())  # Print current position after moving motor_y

    # Run the main scanning cycle with the center button
    elif Button.CENTER in pressed_buttons:
        sudoku_plotter.scanning_cycle()

    # Optional: Add a small wait to avoid spamming the button checks
    wait(100)
