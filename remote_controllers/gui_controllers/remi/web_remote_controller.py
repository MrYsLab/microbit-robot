"""
    web_remote_controller.py

    This file implements a remi GUI
    to control the movement of the microbit_robot over the radio interface.

    License: The MIT License (MIT)

    Copyright (c) 2018 Alan Yorinks

"""
import remi.gui as gui
from remi.gui import *
from remi import start, App
import serial
import time
import sys
import glob
import socket


class RobotController(App):
    def __init__(self, *args, **kwargs):
        self.com_port = None
        self.micro_bit_serial = None
        if not 'editing_mode' in kwargs.keys():
            super(RobotController, self).__init__(*args, static_file_path='./res/')

    def idle(self):
        # idle function called every update cycle
        pass

    def main(self):
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
        print('Port found: ', self.com_port)
        return RobotController.construct_ui(self)

    @staticmethod
    def construct_ui(self):
        main_frame = Widget()
        main_frame.attributes['class'] = "Widget"
        main_frame.attributes['editor_constructor'] = "()"
        main_frame.attributes['editor_varname'] = "main_frame"
        main_frame.attributes['editor_tag_type'] = "widget"
        main_frame.attributes['editor_newclass'] = "False"
        main_frame.attributes['editor_baseclass'] = "Widget"
        main_frame.style['margin'] = "0px"
        main_frame.style['width'] = "800px"
        main_frame.style['height'] = "463px"
        main_frame.style['position'] = "absolute"
        main_frame.style['display'] = "block"
        main_frame.style['left'] = "121px"
        main_frame.style['top'] = "81px"
        main_frame.style['overflow'] = "auto"
        btn_forward = Button('Forward')
        btn_forward.attributes['class'] = "Button"
        btn_forward.attributes['editor_constructor'] = "('Forward')"
        btn_forward.attributes['editor_varname'] = "btn_forward"
        btn_forward.attributes['editor_tag_type'] = "widget"
        btn_forward.attributes['editor_newclass'] = "False"
        btn_forward.attributes['editor_baseclass'] = "Button"
        btn_forward.style['margin'] = "0px"
        btn_forward.style['width'] = "100px"
        btn_forward.style['height'] = "30px"
        btn_forward.style['position'] = "absolute"
        btn_forward.style['display'] = "block"
        btn_forward.style['overflow'] = "auto"
        btn_forward.style['left'] = "340px"
        btn_forward.style['top'] = "110px"
        main_frame.append(btn_forward, 'btn_forward')
        btn_reverse = Button('Reverse')
        btn_reverse.attributes['class'] = "Button"
        btn_reverse.attributes['editor_constructor'] = "('Reverse')"
        btn_reverse.attributes['editor_varname'] = "btn_reverse"
        btn_reverse.attributes['editor_tag_type'] = "widget"
        btn_reverse.attributes['editor_newclass'] = "False"
        btn_reverse.attributes['editor_baseclass'] = "Button"
        btn_reverse.style['margin'] = "0px"
        btn_reverse.style['width'] = "100px"
        btn_reverse.style['height'] = "30px"
        btn_reverse.style['position'] = "absolute"
        btn_reverse.style['display'] = "block"
        btn_reverse.style['overflow'] = "auto"
        btn_reverse.style['left'] = "340px"
        btn_reverse.style['top'] = "246px"
        main_frame.append(btn_reverse, 'btn_reverse')
        btn_left = Button('Left')
        btn_left.attributes['class'] = "Button"
        btn_left.attributes['editor_constructor'] = "('Left')"
        btn_left.attributes['editor_varname'] = "btn_left"
        btn_left.attributes['editor_tag_type'] = "widget"
        btn_left.attributes['editor_newclass'] = "False"
        btn_left.attributes['editor_baseclass'] = "Button"
        btn_left.style['margin'] = "0px"
        btn_left.style['width'] = "100px"
        btn_left.style['height'] = "30px"
        btn_left.style['position'] = "absolute"
        btn_left.style['display'] = "block"
        btn_left.style['overflow'] = "auto"
        btn_left.style['left'] = "190px"
        btn_left.style['top'] = "172px"
        btn_right = Button('Right')
        btn_right.attributes['class'] = "Button"
        btn_right.attributes['editor_constructor'] = "('Right')"
        btn_right.attributes['editor_varname'] = "btn_right"
        btn_right.attributes['editor_tag_type'] = "widget"
        btn_right.attributes['editor_newclass'] = "False"
        btn_right.attributes['editor_baseclass'] = "Button"
        btn_right.style['margin'] = "0px"
        btn_right.style['width'] = "100px"
        btn_right.style['height'] = "30px"
        btn_right.style['position'] = "absolute"
        btn_right.style['display'] = "block"
        btn_right.style['overflow'] = "auto"
        btn_right.style['left'] = "490px"
        btn_right.style['top'] = "172px"
        btn_right.style['border-style'] = "none"
        btn_left.append(btn_right, 'btn_right')
        main_frame.append(btn_left, 'btn_left')
        btn_spin_right = Button('Spin Right')
        btn_spin_right.attributes['class'] = "Button"
        btn_spin_right.attributes['editor_constructor'] = "('Spin Right')"
        btn_spin_right.attributes['editor_varname'] = "btn_spin_right"
        btn_spin_right.attributes['editor_tag_type'] = "widget"
        btn_spin_right.attributes['editor_newclass'] = "False"
        btn_spin_right.attributes['editor_baseclass'] = "Button"
        btn_spin_right.style['margin'] = "0px"
        btn_spin_right.style['width'] = "100px"
        btn_spin_right.style['height'] = "30px"
        btn_spin_right.style['position'] = "absolute"
        btn_spin_right.style['display'] = "block"
        btn_spin_right.style['overflow'] = "auto"
        btn_spin_right.style['left'] = "490px"
        btn_spin_right.style['top'] = "360px"
        main_frame.append(btn_spin_right, 'btn_spin_right')
        lbl_RobotController = Label('Robot Controller')
        lbl_RobotController.attributes['class'] = "Label"
        lbl_RobotController.attributes['editor_constructor'] = "('Robot Controller')"
        lbl_RobotController.attributes['editor_varname'] = "lbl_RobotController"
        lbl_RobotController.attributes['editor_tag_type'] = "widget"
        lbl_RobotController.attributes['editor_newclass'] = "False"
        lbl_RobotController.attributes['editor_baseclass'] = "Label"
        lbl_RobotController.style['margin'] = "0px"
        lbl_RobotController.style['width'] = "212px"
        lbl_RobotController.style['height'] = "31px"
        lbl_RobotController.style['position'] = "absolute"
        lbl_RobotController.style['display'] = "block"
        lbl_RobotController.style['overflow'] = "auto"
        lbl_RobotController.style['left'] = "300px"
        lbl_RobotController.style['top'] = "27px"
        lbl_RobotController.style['border-width'] = "0px"
        lbl_RobotController.style['font-size'] = "24px"
        main_frame.append(lbl_RobotController, 'lbl_RobotController')
        btn_spin_left = Button('Spin Left')
        btn_spin_left.attributes['class'] = "Button"
        btn_spin_left.attributes['editor_constructor'] = "('Spin Left')"
        btn_spin_left.attributes['editor_varname'] = "btn_spin_left"
        btn_spin_left.attributes['editor_tag_type'] = "widget"
        btn_spin_left.attributes['editor_newclass'] = "False"
        btn_spin_left.attributes['editor_baseclass'] = "Button"
        btn_spin_left.style['margin'] = "0px"
        btn_spin_left.style['width'] = "100px"
        btn_spin_left.style['height'] = "30px"
        btn_spin_left.style['position'] = "absolute"
        btn_spin_left.style['display'] = "block"
        btn_spin_left.style['overflow'] = "auto"
        btn_spin_left.style['left'] = "190px"
        btn_spin_left.style['top'] = "360px"
        main_frame.append(btn_spin_left, 'btn_spin_left')
        main_frame.children['btn_forward'].set_on_mousedown_listener(self.onmousedown_btn_forward)
        main_frame.children['btn_forward'].set_on_mouseup_listener(self.onmouseup_btn_forward)
        main_frame.children['btn_reverse'].set_on_mousedown_listener(self.onmousedown_btn_reverse)
        main_frame.children['btn_reverse'].set_on_mouseup_listener(self.onmouseup_btn_reverse)
        main_frame.children['btn_left'].set_on_mousedown_listener(self.onmousedown_btn_left)
        main_frame.children['btn_left'].set_on_mouseup_listener(self.onmouseup_btn_left)
        main_frame.children['btn_left'].children['btn_right'].set_on_mousedown_listener(self.onmousedown_btn_right)
        main_frame.children['btn_left'].children['btn_right'].set_on_mouseup_listener(self.onmouseup_btn_right)
        main_frame.children['btn_spin_right'].set_on_mousedown_listener(self.onmousedown_btn_spin_right)
        main_frame.children['btn_spin_right'].set_on_mouseup_listener(self.onmouseup_btn_spin_right)
        main_frame.children['btn_spin_left'].set_on_mousedown_listener(self.onmousedown_btn_spin_left)
        main_frame.children['btn_spin_left'].set_on_mouseup_listener(self.onmouseup_btn_spin_left)

        self.main_frame = main_frame
        return self.main_frame

    def onmousedown_btn_forward(self, emitter, x, y):
        print('fdown')
        self.write_to_mb('fwd')

    def onmouseup_btn_forward(self, emitter, x, y):
        print('fup')
        self.write_to_mb('stop')

    def onmousedown_btn_reverse(self, emitter, x, y):
        self.write_to_mb('rev')

    def onmouseup_btn_reverse(self, emitter, x, y):
        self.write_to_mb('stop')

    def onmousedown_btn_left(self, emitter, x, y):
        self.write_to_mb('left')

    def onmouseup_btn_left(self, emitter, x, y):
        self.write_to_mb('stop')

    def onmousedown_btn_right(self, emitter, x, y):
        self.write_to_mb('right')

    def onmouseup_btn_right(self, emitter, x, y):
        self.write_to_mb('stop')

    def onmousedown_btn_spin_right(self, emitter, x, y):
        self.write_to_mb('spin_right')

    def onmouseup_btn_spin_right(self, emitter, x, y):
        self.write_to_mb('stop')

    def onmousedown_btn_spin_left(self, emitter, x, y):
        self.write_to_mb('spin_left')

    def onmouseup_btn_spin_left(self, emitter, x, y):
        self.write_to_mb('stop')
        self.write_to_mb('stop')

    def write_to_mb(self, msg):
        msg = bytes(msg.encode())
        self.micro_bit_serial.write(msg)

#Configuration
configuration = {'config_project_name': 'RobotController',
                 'config_address': '0.0.0.0', 'config_port': 8081,
                 'config_multiple_instance': True, 'config_enable_file_cache': True,
                 'config_start_browser': True, 'config_resourcepath': './res/'}

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # use the google dns
    s.connect(('8.8.8.8', 0))
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(RobotController, address=s.getsockname()[0], port=configuration['config_port'],
                        multiple_instance=configuration['config_multiple_instance'],
                        enable_file_cache=configuration['config_enable_file_cache'],
                        start_browser=configuration['config_start_browser'])
