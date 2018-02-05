from microbit import pin0,pin8,pin12,pin15,pin16,Image,sleep
class KMotor:
 FORWARD=0
 REVERSE=1
 MOTOR_1=0
 MOTOR_2=1
 def __init__(self):
  self.motor_off(KMotor.MOTOR_1)
  self.motor_off(KMotor.MOTOR_2)
  display.clear()
 def motor_on(self,motor,direction,speed=100):
  if not 0<=speed<=100:
   display.show(Image.NO)
   return
  speed=self._scale(speed)
  if direction==KMotor.FORWARD:
   if motor==KMotor.MOTOR_1:
    pin8.write_analog(speed)
    pin12.write_digital(0)
   elif motor==KMotor.MOTOR_2:
    pin0.write_analog(speed)
    pin16.write_digital(0)
  else:
   if motor==KMotor.MOTOR_1:
    pin12.write_analog(speed)
    pin8.write_digital(0)
   elif motor==KMotor.MOTOR_2:
    pin16.write_analog(speed)
    pin0.write_digital(0)
 def motor_off(self,motor):
  if motor==KMotor.MOTOR_1:
   pin8.write_analog(0)
   pin12.write_analog(0)
  else:
   pin0.write_analog(0)
   pin16.write_analog(0)
 def motor_brake(self,motor):
  if motor==KMotor.MOTOR_1:
   pin8.write_digital(1)
   pin12.write_digital(1)
  else:
   pin0.write_digital(1)
   pin16.write_digital(1)
 def _scale(self,value):
  new_value=(1023/100)*value
  return int(new_value)
from microbit import display
import radio
class Robot:
 def __init__(self):
  self.km=KMotor()
  display.show(Image.HAPPY)
  self.dispatch={'fwd':self.go_forward,'rev':self.go_reverse,'left':self.go_left,'right':self.go_right,'spin_right':self.spin_right,'spin_left':self.spin_left,'stop':self.stop,}
  radio.on()
  while True:
   if not pin15.read_digital():
    self.go_reverse()
    sleep(1000)
    self.go_right()
    sleep(1000)
    self.stop()
   cmd=radio.receive()
   if cmd is None:
    pass
   else:
    op=self.dispatch.get(cmd,None)
    if op:
     op()
 def go_forward(self):
  display.show(Image.ARROW_N)
  self.km.motor_on(self.km.MOTOR_1,self.km.FORWARD,60)
  self.km.motor_on(self.km.MOTOR_2,self.km.FORWARD,60)
 def go_reverse(self):
  display.show(Image.ARROW_S)
  self.km.motor_on(self.km.MOTOR_1,self.km.REVERSE,70)
  self.km.motor_on(self.km.MOTOR_2,self.km.REVERSE)
 def go_left(self):
  display.show(Image.ARROW_W)
  self.km.motor_on(self.km.MOTOR_1,self.km.FORWARD,40)
  self.km.motor_on(self.km.MOTOR_2,self.km.FORWARD)
 def go_right(self):
  display.show(Image.ARROW_E)
  self.km.motor_on(self.km.MOTOR_1,self.km.FORWARD)
  self.km.motor_on(self.km.MOTOR_2,self.km.FORWARD,40)
 def spin_right(self):
  display.show(Image.ARROW_SE)
  self.km.motor_on(self.km.MOTOR_1,self.km.FORWARD)
  self.km.motor_on(self.km.MOTOR_2,self.km.REVERSE)
 def spin_left(self):
  display.show(Image.ARROW_SW)
  self.km.motor_on(self.km.MOTOR_2,self.km.FORWARD)
  self.km.motor_on(self.km.MOTOR_1,self.km.REVERSE)
 def stop(self):
  self.km.motor_off(self.km.MOTOR_1)
  self.km.motor_off(self.km.MOTOR_2)
  display.clear()
r=Robot()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
