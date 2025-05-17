from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait
from sudoku_plotter import SudokuPlotter
import time

class SudokuWriter:
    def __init__(self, motor_x_port, motor_y_port):
        self.ev3 = EV3Brick()
        self.motor_x = Motor(motor_x_port)
        self.motor_y = Motor(motor_y_port)
        self.cell_size_x = 408  
        self.cell_size_y = 1200  
        self.offset_x = 51
        self.offset_y = 0
        self.plotter = SudokuPlotter(
            motor_x_port=Port.D,
            motor_y_port=Port.A,
            color_sensor_port=Port.S4,
            touch_sensor_y_port=Port.S1,
            touch_sensor_x_start_port=Port.S2,
            touch_sensor_x_end_port=Port.S3
        )

        
    def beep(self):
        """Makes the EV3 beep."""
        self.ev3.speaker.beep()
        
    def move_to_x(self, col, i):
        """Move to the specified cell in the sudoku grid."""
        # Calculate target position
        target_x = self.offset_x + 50 + col * self.cell_size_x + i*108
    
        # Move to position
        self.motor_x.run_target(300, target_x)
        print("Moved to x position:", target_x)
    
    def move_to_y(self, row, i):
        """Move to the specified cell in the sudoku grid."""
        # Calculate target position
        target_y = self.offset_y + row * self.cell_size_y + (i-2)*300
    
        # Move to position
        self.motor_y.run_target(300, target_y)

    
        
    def write_number(self, number,i):
        """Write a specific number at the current position."""
        # Implement number writing patterns here
        # This will depend on how you want to physically mark the numbers
        if i == 1:
            if number in (1,3,7):
                self.motor_y.run_angle(300, 1200) 
            elif number in (4,5,9):
                self.write_line_y(1) # upline
            elif number in (6,8):
                self.write_line_y(2) # wholeline
            elif number == 2:
                self.write_line_y(3) # downline
        elif i == 2:
            if number == 2:
                self.write_line_y(1) # upline
            elif number in (1,3,4,7,8,9):
                self.write_line_y(2) # wholeline
            elif number in (5,6):
                self.write_line_y(3) # downline
        elif i == 3:
            if number in (1,4):
                self.motor_x.run_angle(300, 400)
            else:
                self.write_line_x() 
        elif i == 4:
            if number in (1,7):
                self.motor_x.run_angle(300, 400)
            else:
                self.write_line_x()
        elif i == 5:
            if number in (1,4,7):
                self.motor_x.run_angle(300, 400)
            else:
                self.write_line_x()
            
        
            
    def write_sudoku(self, sudoku_array):
        """Write the entire sudoku puzzle based on the array."""
        self.beep()  # Signal start
        
        self.motor_y.reset_angle(0)
        self.motor_x.reset_angle(0)

        # for col in range(9):
        #     for i in range(1,3):
        #         self.plotter.go_to_start_y()
        #         self.move_to_x(col, i)
        #         for row in range(9):
        #             number = sudoku_array[row][col]
        #             if number > 0:  # Only write non-zero values
        #                 print(number,i)
        #                 self.write_number(number,i)
 
        #             else:
        #                 print(number,i)
        #                 self.motor_y.run_angle(300, 1200)
        #         self.motor_y.run_angle(300, 9*1200 - 300)

        # self.plotter.go_to_start()
        for row in range(9):
            for i in range(3,6):
                self.plotter.go_to_start_x()
                self.move_to_y(row, i)
                for col in range(9):
                    number = sudoku_array[row][col]
                    if number > 0:  # Only write non-zero values
                        print(number,i)
                        self.write_number(number,i)
                    else:
                        print(number,i)
                        self.motor_x.run_angle(300, 400)
                    self.beep()
                self.motor_x.run_angle(1200, -3300)
  
                        
        self.beep()  # Signal completion
        
   
    def write_line_y(self,i,speed=300):
        self.motor_y.run_angle(speed, 300)
        if i == 1:
            print("Pen down")
            self.motor_y.run_angle(speed, 300)
            print("Pen up")
            self.motor_y.run_angle(speed, 300)
        elif i == 2:
            print("Pen down")
            self.motor_y.run_angle(speed, 600)
            print("Pen up")
        elif i == 3:
            self.motor_y.run_angle(speed, 300)
            print("Pen down")
            self.motor_y.run_angle(speed, 300)
            print("Pen up")

        self.motor_y.run_angle(speed, 300)

    def write_line_x(self,speed=300):
        self.motor_x.run_angle(speed, 150)
        print("Pen down")
        self.motor_x.run_angle(speed, 108)
        print("Pen up")
        self.motor_x.run_angle(speed, 150)
            
       
