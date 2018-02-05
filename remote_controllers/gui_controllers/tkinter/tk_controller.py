"""
    tk_controller.py

    This file implements a tkinter GUI
    to control the movement of the microbit_robot over the radio interface.

    License: The MIT License (MIT)

    Copyright (c) 2018 Alan Yorinks

"""

from tkinter import *
from tkinter import ttk
import serial
import time
import sys
import glob


class TkController:
    def __init__(self):

        # find the microbit serail port
        print('Autodetecting serial port. Please wait...')
        if sys.platform.startswith('darwin'):
            locations = glob.glob('/dev/tty.[usb*]*')
            locations = glob.glob('/dev/tty.[wchusb*]*') + locations
            locations.append('end')
            # for everyone else, here is a list of possible ports
        else:
            locations = ['dev/ttyACM0', '/dev/ttyACM0', '/dev/ttyACM1',
                         '/dev/ttyACM2', '/dev/ttyACM3', '/dev/ttyACM4',
                         '/dev/ttyACM5', '/dev/ttyUSB0', '/dev/ttyUSB1',
                         '/dev/ttyUSB2', '/dev/ttyUSB3', '/dev/ttyUSB4',
                         '/dev/ttyUSB5', '/dev/ttyUSB6', '/dev/ttyUSB7',
                         '/dev/ttyUSB8', '/dev/ttyUSB9',
                         '/dev/ttyUSB10',
                         '/dev/ttyS0', '/dev/ttyS1', '/dev/ttyS2',
                         '/dev/tty.usbserial', '/dev/tty.usbmodem', 'com2',
                         'com3', 'com4', 'com5', 'com6', 'com7', 'com8',
                         'com9', 'com10', 'com11', 'com12', 'com13',
                         'com14', 'com15', 'com16', 'com17', 'com18',
                         'com19', 'com20', 'com21', 'com22', 'com23', 'com24',
                         'com25', 'com26', 'com27', 'com28', 'com29', 'com30',
                         'com31', 'com32', 'com33', 'com34', 'com35', 'com36',
                         'com1', 'end'
                         ]

        detected = None
        for device in locations:
            try:
                self.micro_bit_serial = serial.Serial(port=device, baudrate=115200,
                                                      timeout=.1)
                detected = device
                break
            except serial.SerialException:
                if device == 'end':
                    print('Unable to find Serial Port, Please plug in '
                          'cable or check cable connections.')
                    detected = None
                    exit()
            except OSError:
                pass
        self.com_port = detected

        # open and close the port to flush the serial buffers
        self.micro_bit_serial.close()
        self.micro_bit_serial.open()
        time.sleep(.05)
        print('micro:bit serial port: ', self.com_port)
        # setup root window
        self.root = Tk()
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # keep the window a fixed size
        self.root.wm_resizable(0, 0)

        self.root.title("micro:bit Robot Controller")

        # create content window into which everything else is placed
        self.content = ttk.Frame(self.root, padding=12, height=480, width=640)
        self.content.grid(column=0, row=0, sticky=(N, S, E, W))
        self.content.rowconfigure(0, weight=1)

        # associate all the images for the buttons

        self.spin_left_image = PhotoImage(file="images/spin_left.gif")
        self.spin_right_image = PhotoImage(file="images/spin_right.gif")
        self.right_image = PhotoImage(file="images/right.gif")
        self.left_image = PhotoImage(file="images/left.gif")
        self.forward_image = PhotoImage(file="images/forward.gif")
        self.reverse_image = PhotoImage(file="images/reverse.gif")

        self.create_control_frame()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.mainloop()

    def create_control_frame(self):
        """
        Create the control frame of the GUI
        :return:
        """

        # create the control frame
        control_frame = ttk.Labelframe(self.content, borderwidth=5, relief="raised", text="Robot Motion")
        control_frame.grid(column=0, row=0, sticky=(N, S, E, W))

        style = ttk.Style()
        style.configure("BW.TLabel", foreground="black", background="white")

        # create widgets and associate their events with handlers
        forward_button = ttk.Button(control_frame, image=self.forward_image)
        forward_button.bind("<Button-1>", self.forward_pressed)
        forward_button.bind("<ButtonRelease-1>", self.button_released)

        reverse_button = ttk.Button(control_frame, image=self.reverse_image)
        reverse_button.bind("<Button-1>", self.reverse_pressed)
        reverse_button.bind("<ButtonRelease-1>", self.button_released)

        left_button = ttk.Button(control_frame, image=self.left_image)
        left_button.bind("<Button-1>", self.left_pressed)
        left_button.bind("<ButtonRelease-1>", self.button_released)

        right_button = ttk.Button(control_frame, image=self.right_image)
        right_button.bind("<Button-1>", self.right_pressed)
        right_button.bind("<ButtonRelease-1>", self.button_released)

        spin_right_button = ttk.Button(control_frame, image=self.spin_right_image)
        spin_right_button.bind("<Button-1>", self.spin_right_pressed)
        spin_right_button.bind("<ButtonRelease-1>", self.button_released)

        spin_left_button = ttk.Button(control_frame, image=self.spin_left_image)
        spin_left_button.bind("<Button-1>", self.spin_left_pressed)
        spin_left_button.bind("<ButtonRelease-1>", self.button_released)

        spin_right_button.grid(column=4, row=0, pady=20, padx=(2, 30))
        spin_left_button.grid(column=2, row=0, pady=10, padx=(30, 2))
        forward_button.grid(column=3, row=1, pady=40)
        reverse_button.grid(column=3, row=3, pady=(40, 40))
        left_button.grid(column=2, row=2, sticky=W, padx=(30, 1))
        right_button.grid(column=4, row=2, sticky=E, padx=(1, 30))

    def forward_pressed(self, event):
        """
        Move robot forward
        :return:
        """
        self.write_to_mb('fwd')

    def reverse_pressed(self, event):
        """
        Move robot in reverse
        :return:
        """
        self.write_to_mb('rev')

    def left_pressed(self, event):
        """
        Move robot left
        :return:
        """
        self.write_to_mb('left')

    def right_pressed(self, event):
        """
        Move robot right
        :return:
        """
        self.write_to_mb('right')

    def spin_left_pressed(self, event):
        """
        Spin robot to the left
        :return:
        """
        self.write_to_mb('spin_left')

    def spin_right_pressed(self, event):
        """
        Spin robot to the right
        :return:
        """
        self.write_to_mb('spin_right')


    def button_released(self, event):
        """
        A gui button has been released. Send a message to stop the robot
        :return:
        """
        self.write_to_mb('stop')
        self.write_to_mb('stop')

    def write_to_mb(self, msg):
        msg = bytes(msg.encode())
        self.micro_bit_serial.write(msg)
        time.sleep(.05)

    def on_closing(self):
        """
        Destroy the window
        :return:
        """
        self.root.destroy()

tkc = TkController()