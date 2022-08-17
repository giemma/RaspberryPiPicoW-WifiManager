import os
import sys
import uos
import network
import machine
import socket
import time
import displayutility
import displaycolors as Colors
import wifimanager.wifimanager as wifimanager

led = machine.Pin("LED",machine.Pin.OUT)
reset_button = machine.Pin(16, machine.Pin.IN)

display = displayutility.DisplayUtility()
display.WriteLines(["Display: OK"])

WiFIManager = wifimanager.WiFiManager(display)

while True:
    
    logic_state = reset_button.value()
    if logic_state == True:     
      WiFIManager.ClearCredentials()
      display.WriteLines(["Reset","on","2 seconds"], color=Colors.BLACK, background=Colors.YELLOW)
      time.sleep(2)
      machine.reset()
      
      
    time.sleep(1)
    led.off()
    time.sleep(1)
    led.on()
    
#sub_save_credentials('X1','Y2')

#time.sleep(2)
#credentials = sub_read_credentials()
#print(credentials[0])
#print(credentials[1])
#raise RuntimeError('test')


















