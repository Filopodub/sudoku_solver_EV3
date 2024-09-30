#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Button
from sudoku_plotter import SudokuPlotter
from pybricks.tools import wait

# Create an instance of SudokuPlotter
sudoku_plotter = SudokuPlotter(Port.A, Port.B)
ev3 = EV3Brick()

# Beep to indicate the start of the program
sudoku_plotter.beep()

while True:
    # Wait for a button press
    pressed_buttons = ev3.buttons.pressed()

    # Control motor_x with left and right buttons
    if Button.LEFT in pressed_buttons:
        sudoku_plotter.move_x(10)  # Move motor_x by 10 degrees
        print(sudoku_plotter.get_position())  # Print current position after moving motor_x

    elif Button.RIGHT in pressed_buttons:
        sudoku_plotter.move_x(-10)  # Move motor_x by -10 degrees (reverse)
        print(sudoku_plotter.get_position())  # Print current position after moving motor_x

    # Control motor_y with up and down buttons
    elif Button.UP in pressed_buttons:
        sudoku_plotter.move_y(10)  # Move motor_y by 10 degrees
        print(sudoku_plotter.get_position())  # Print current position after moving motor_y

    elif Button.DOWN in pressed_buttons:
        sudoku_plotter.move_y(-10)  # Move motor_y by -10 degrees (reverse)
        print(sudoku_plotter.get_position())  # Print current position after moving motor_y

    # Run the main movement with the middle button
    elif Button.CENTER in pressed_buttons:
        # Move to a specific position
        sudoku_plotter.move_to(180, 180)

        # Stop the motors
        sudoku_plotter.motor_x.stop()
        sudoku_plotter.motor_y.stop()

        # Indicate completion
        sudoku_plotter.ev3.speaker.beep()  # Beep again to indicate completion

        # Print the final position
        print(sudoku_plotter.get_position())

    # Quit the program with the back button (no need cos' it is predefined)
    elif Button.BEACON in pressed_buttons:
        print("Quitting the program.")
        break  # Exit the loop and end the program

    # Optional: Add a small wait to avoid spamming the button checks
    wait(100)
