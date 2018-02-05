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
