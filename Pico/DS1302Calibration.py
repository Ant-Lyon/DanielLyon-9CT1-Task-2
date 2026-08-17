from machine import RTC, Pin
import time
import ds1302

picoRTC = RTC()
timestamp = picoRTC.datetime()

dsRTC = ds1302.DS1302(Pin(9), Pin(8), Pin(7))
dsRTC.start()
dsRTC.date_time(timestamp[:7])


print(timestamp)
print(dsRTC.date_time())
time.sleep(1)
print(dsRTC.date_time())
