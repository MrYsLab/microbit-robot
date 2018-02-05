"""
    microbit_robot.py

    This file implements the code needed to run the motors on a simple
    2 wheel robot and perform collision avoidance.

    It utilizes the KMotor library to control the motors.

    It provides collision avoidance using
    a Sharp GP2Y0D810Z0F Digital Distance sensor.

    The Robot class listens for commands over the radio interface.

    License: The MIT License (MIT)

    Copyright (c) 2018 Alan Yorinks

"""
from microbit import pin0, pin8, pin12, pin15, pin16, Image, sleep


class KMotor:
    """
    This class is used to control 2 motors with the Kitronic
    Motor Driver Board
    """

    # Motor Directions
    FORWARD = 0
    REVERSE = 1

    # Motor Selectors
    MOTOR_1 = 0
    MOTOR_2 = 1

    def __init__(self):
        """
        Turn off both motors and clear the display
        """
        self.motor_off(KMotor.MOTOR_1)
        self.motor_off(KMotor.MOTOR_2)
        display.clear()

    def motor_on(self, motor, direction, speed=100):
        """
        Turn motor with the given direction and speed.
        If speed is out of range, the NO image will
        be displayed and no motor will be turned on.
        :param motor: KMotor.MOTOR1 or KMotor.Motor2
        :param direction: KMotor.FORWARD or KMOTOR.REVERSE
        :param speed: 0 - 100
        :return:
        """
        # make sure the speed is within range
        if not 0 <= speed <= 100:
            # not display a "NO" and return
            display.show(Image.NO)
            return

        # speed needs to be scaled from 0-100 to 0-1023
        speed = self._scale(speed)

        # Move Motor Forward
        if direction == KMotor.FORWARD:
            if motor == KMotor.MOTOR_1:
                pin8.write_analog(speed)
                pin12.write_digital(0)
            elif motor == KMotor.MOTOR_2:
                pin0.write_analog(speed)
                pin16.write_digital(0)

        # Move Motor In Reverse
        else:
            if motor == KMotor.MOTOR_1:
                pin12.write_analog(speed)
                pin8.write_digital(0)
            elif motor == KMotor.MOTOR_2:
                pin16.write_analog(speed)
                pin0.write_digital(0)

    def motor_off(self, motor):
        """
        Place motor in coast mode
        :param motor: KMotor.MOTOR1 or KMotor.Motor2
        :return:
        """
        if motor == KMotor.MOTOR_1:
            pin8.write_analog(0)
            pin12.write_analog(0)
        else:
            pin0.write_analog(0)
            pin16.write_analog(0)

    def motor_brake(self, motor):
        """
        Brake the selected motor.
        :param motor:
        :return:
        """
        if motor == KMotor.MOTOR_1:
            pin8.write_digital(1)
            pin12.write_digital(1)
        else:
            pin0.write_digital(1)
            pin16.write_digital(1)

    def _scale(self, value):
        """
        Scale the speed from 0-100 to 0-1023
        :param value: 0-100
        :return: scaled speed
        """
        new_value = (1023 / 100) * value
        return int(new_value)


from microbit import display
import radio


class Robot:
    """
    This class runs a simple 2 wheel/2motor robot.
    It listens for commands over the radio interface
    and dispatches the method associated with the command.

    It also monitors the Sharp GP2Y0D810Z0F Digital Distance Sensor
    for objects that are in front of the robot
    """

    def __init__(self):
        """
        Instantiate an instance of KMotor.
        Display a "smile" to let the use know that upon
        first power up, we are alive.
        Create a dispatch table for each radio command.
        Turn on the radio and wait for commands to come in.
        """

        # instantiate a motor object
        self.km = KMotor()

        # display something so that we know the board is
        # alive
        display.show(Image.HAPPY)

        # build a dispatch dictionary to allow us
        # to quickly execute each incoming command
        self.dispatch = {'fwd': self.go_forward,
                         'rev': self.go_reverse,
                         'left': self.go_left,
                         'right': self.go_right,
                         'spin_right': self.spin_right,
                         'spin_left': self.spin_left,
                         'stop': self.stop,
                         }
        # turn on the micro:bit radio so that we can receive commands.
        radio.on()

        while True:
            # check to see if we need to perform an avoidance maneuver.
            # when an object is near, the distance sensor returns a digital 0.
            # if a crash is imminent, reverse and go right
            if not pin15.read_digital():
                self.go_reverse()
                sleep(1000)
                self.go_right()
                sleep(1000)
                self.stop()

            # get next command
            cmd = radio.receive()
            if cmd is None:
                pass
            else:
                # move motors based on command
                # fetch command from command table
                op = self.dispatch.get(cmd, None)
                # if a command has been fetched, execute it
                if op:
                    op()

    # motion command handlers
    def go_forward(self):
        display.show(Image.ARROW_N)
        # adjust speeds to help robot go straight
        self.km.motor_on(self.km.MOTOR_1, self.km.FORWARD, 60)
        self.km.motor_on(self.km.MOTOR_2, self.km.FORWARD, 60)

    def go_reverse(self):
        display.show(Image.ARROW_S)
        # adjust speeds to help robot go straight
        self.km.motor_on(self.km.MOTOR_1, self.km.REVERSE, 70)
        self.km.motor_on(self.km.MOTOR_2, self.km.REVERSE)

    def go_left(self):
        display.show(Image.ARROW_W)
        # adjust speed to turn the robot
        self.km.motor_on(self.km.MOTOR_1, self.km.FORWARD, 40)
        self.km.motor_on(self.km.MOTOR_2, self.km.FORWARD)

    def go_right(self):
        display.show(Image.ARROW_E)
        # adjust speed to turn the robot
        self.km.motor_on(self.km.MOTOR_1, self.km.FORWARD)
        self.km.motor_on(self.km.MOTOR_2, self.km.FORWARD, 40)

    def spin_right(self):
        display.show(Image.ARROW_SE)
        self.km.motor_on(self.km.MOTOR_1, self.km.FORWARD)
        self.km.motor_on(self.km.MOTOR_2, self.km.REVERSE)

    def spin_left(self):
        display.show(Image.ARROW_SW)
        self.km.motor_on(self.km.MOTOR_2, self.km.FORWARD)
        self.km.motor_on(self.km.MOTOR_1, self.km.REVERSE)

    def stop(self):
        self.km.motor_off(self.km.MOTOR_1)
        self.km.motor_off(self.km.MOTOR_2)
        display.clear()


# instantiate a Robot
r = Robot()
