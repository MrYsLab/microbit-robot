from microbit import pin0,pin1,pin2,pin8,pin12,pin16,button_a,button_b,sleep
import radio
class GamerBit:
 def __init__(self,callback,scans=1):
  self.pins=[pin0,pin1,pin2,pin8,pin12,pin16,button_a,button_b]
  self.callback=callback
  self.number_of_scans=scans
  for pin in self.pins[:-2]:
   pin.set_pull(pin.PULL_UP)
  self.previous_readings=[0]*8
  self.current_readings=[0]*8
  self._scanner()
 def scan(self):
  readings=[int(not pin.read_digital())for pin in self.pins[:-2]]
  readings.append(int(button_a.is_pressed()))
  readings.append(int(button_b.is_pressed()))
  self.current_readings=[int(self.current_readings[pin]or readings[pin])for pin in range(0,len(readings))]
 def _scanner(self):
  pin_ids=['pin0','pin1','pin2','pin8','pin12','pin16','button_a','button_b']
  while True:
   for scans in range(0,self.number_of_scans):
    self.scan()
   report={}
   for x in range(0,8):
    if self.current_readings[x]!=self.previous_readings[x]:
     report[pin_ids[x]]=self.current_readings[x]
   self.previous_readings=self.current_readings
   self.current_readings=[0]*8
   if report:
    if self.callback:
     self.callback(report)
def gb_callback(report):
 radio.on()
 for key in report:
  value=report[key]
  if value==0:
   radio.send('stop')
   radio.send('stop')
   sleep(10)
   radio.send('stop')
  else:
   if key=='pin0':
    radio.send('fwd')
    print('fwd')
   elif key=='pin8':
    radio.send('rev')
    print('rev')
   elif key=='pin1':
    radio.send('left')
    print('left')
   elif key=='pin2':
    radio.send('right')
    print('right')
   elif key=='pin12':
    radio.send('spin_left')
    print('spin_left')
   elif key=='pin16':
    radio.send('spin_right')
    print('spin_right')
   else:
    pass
 radio.off()
gb=GamerBit(gb_callback)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
