"""
    gui_radio_bridge.py
    This file is loaded onto a micro:bit and bridges the serial interface
    of the tkinter and remi GUI's to the micro:bit radio.
    The microbit must be connected to USB on the PC
    License: The MIT License (MIT)
    Copyright (c) 2018 Alan Yorinks
"""
from microbit import*
import radio
while True:
 data=uart.readline()
 sleep(8)
 if data:
  cmd=str(data,'utf-8').rstrip()
  radio.on()
  radio.send(cmd)
  radio.off()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
