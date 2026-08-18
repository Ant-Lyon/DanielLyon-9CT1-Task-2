from machine import RTC, Pin
import time
import ds1302

picoRTC = RTC()
timestamp = picoRTC.datetime()

dsRTC = ds1302.DS1302(Pin(13), Pin(12), Pin(11))
dsRTC.start()
dsRTC.date_time(timestamp[:7])


print(timestamp)
print(dsRTC.date_time())
time.sleep(1)
print(dsRTC.date_time())

eventDate = "-".join([str(timestamp[0])[-2:], str(timestamp[1]), str(timestamp[2])])
eventTime = ":".join([str(timestamp[4]), str(timestamp[5])])
print(eventDate, eventTime)
