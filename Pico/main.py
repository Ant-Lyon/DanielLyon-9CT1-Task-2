from machine import Pin, ADC
import threading
import time

isLaserClear = True
passwordString = ""
laserPin = Pin(16, Pin.OUT)
lightDetector = ADC(Pin(16))
buzzer = PWM(Pin(17))
led = Pin(19, Pin.OUT)
stopSystem = False
time = None
Thread(target=statusLogThread).start()
# Thread(target=userInputThread).start()

def logTime(logType): # Takes the type of time log and logs it
    if not stopSystem:
        if logType == "laserBlocked":
            with open('LogFiles\DoorLog.txt', a, encoding="utf-8") as DoorLog:
                DoorLog.write(f"Door OPENED at {time}\n")
        elif logType == "laserClear":
            with open('LogFiles\DoorLog.txt', a, encoding="utf-8") as DoorLog:
                DoorLog.write(f"Door CLOSED at {time}\n")
        elif logType == "status":
            with open('LogFiles\statusLog.txt', w, encoding="utf-8") as SystemLog:
                SystemLog.write(f"{time} OPERATIONAL")
        elif logType == "shutdown":
            with open('LogFiles\StatusLog.txt', w, encoding="utf-8") as SystemLog:
                SystemLog.write(f"{time} AUTHORISED SHUTDOWN")

def statusLogThread(): # Every 20ms it logs the status of the device, so I know when it was last on
    while True:
        while not stopSystem:
            logTime("status")
            time.sleep(5)
        time.sleep_ms(20)

def turnOn(device, tone=None): # Turns on a device but first checks whether or not stopSystem is True. If it is, it will not turn anything on
    if not stopSystem:
        if device == "laserPin":
            laserPin.value(1)
        elif device == "buzzer":
            buzzer.freq(tone)
            buzzer.duty_u16(32728) # A 50% duty cycle makes the buzzer produce sound symmetrically, making it as loud, clear, and efficent as possible

def buzz(action): # Different buzzer noises for different scenarios
    if action == "doorAlarm":
        for i in range(3):
            turnOn("buzzer", 440) # A4
            time.sleep(0.5)
            buzzer.value(0)
            time.sleep(0.5)

def userInputThread(): # Every 20ms it checks whether a button is being pressed and either turns off the device or preforms some other function
    buttonMain = Pin(20, Pin.INPUT, Pin.PULL_DOWN)
    button1 = Pin(21, Pin.INPUT, Pin.PULL_DOWN)
    button2 = Pin(22, Pin.INPUT, Pin.PULL_DOWN)
    button3 = Pin(23, Pin.INPUT, Pin.PULL_DOWN)
    button4 = Pin(24, Pin.INPUT, Pin.PULL_DOWN)
    
    while True:
        while not stopSystem:
            time.sleep_ms(20)
            if buttonMain.value() == 1:
                passwordString = ""
                while len(passwordString) < 4:
                    time.sleep_ms(20)
                    if button1.value() == 1:
                        passwordString = passwordString + "1"
                    elif button1.value() == 2:
                        passwordString = passwordString + "1"
                    elif button1.value() == 3:
                        passwordString = passwordString + "1"
                    elif button1.value() == 4:
                        passwordString = passwordString + "1"
            if "1234" in passwordString:
                logTime("shutdown")
                while not doorLog.closed and not statusLog.closed: # Making sure not to turn off anything until the logs are complete. Not doing this could cause corruption
                    time.sleep_ms(20)
                laserPin.value(0)
                stopSystem = True # When stopSystem is True, it is safe to unplug the device
        while stopSystem:
            time.sleep_ms(20)
            if buttonMain.value() == 1:
                stopSystem = False
'''stopSystem will prevent any actuators from being turned on again, or any logs to happen.
This prevents anything from happening until the loops in the MainThread finish and don't execute again.'''
            
laserPin.value(1)
time.sleep(0.5) # Time for the LDR to detect the light
while True:
    while isLaserClear and not stopSystem: # Technically I don't need to use isLaserClear as a condition, but it makes it easier to identify the loops
        if lightDetector.read_u16() < 40000:
            laserPin.value(0)
            buzz("doorAlarm")
            logTime("laserBlocked")
            isLaserClear = False
        time.sleep_ms(20)
            
    while not isLaserClear and not stopSystem:
        time.sleep(5)
        turnOn("laserPin")
        time.sleep(0.5)
        if lightDetector.read_u16() < 40000:
            laserPin.value(0)
        else: # The laser will be kept on
            logTime("laserClear")
            isLaserClear = True
    
    if stopSystem: # 20 ms is so small it doesn't matter if it runs for no reason, but this if statement tells me what it does
        time.sleep_ms(20)
            
            
# Modules:
# Passive buzzer, two colour LED, light dependant resistor, and RTC.