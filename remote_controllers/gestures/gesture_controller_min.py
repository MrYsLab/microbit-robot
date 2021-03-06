from microbit import*
import radio
last_gesture=''
def send_command(cmd):
 radio.on()
 radio.send(cmd)
 sleep(100)
 radio.off()
while True:
 gesture=accelerometer.current_gesture()
 if button_a.is_pressed():
  gesture='spin_left'
 if button_b.is_pressed():
  gesture='spin_right'
 if not last_gesture==gesture:
  last_gesture=gesture
  if gesture=='down':
   display.show(Image.ARROW_N)
   send_command('fwd')
  elif gesture=='up':
   display.show(Image.ARROW_S)
   send_command('rev')
  elif gesture=='left':
   display.show(Image.ARROW_W)
   send_command('left')
  elif gesture=='right':
   display.show(Image.ARROW_E)
   send_command('right')
  elif gesture=='spin_left':
   display.show(Image.ARROW_SW)
   send_command('spin_left')
  elif gesture=='spin_right':
   display.show(Image.ARROW_SE)
   send_command('spin_right')
  else:
   display.show(Image.NO)
   send_command('stop')
# Created by pyminifier (https://github.com/liftoff/pyminifier)
