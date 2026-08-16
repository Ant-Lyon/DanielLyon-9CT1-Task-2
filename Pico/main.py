from machine import Pin, ADC, PWM
import _thread
import time

def logTime(logType): # Takes the type of time log and logs it
    if not stopSystem:
        if logType == "laserBlocked":
            with open('LogFiles/DoorLog.txt', 'a') as DoorLog:
                DoorLog.write(f"Door OPENED at {timestamp}\n")
        elif logType == "laserClear":
            with open('LogFiles/DoorLog.txt', 'a') as DoorLog:
                DoorLog.write(f"Door CLOSED at {timestamp}\n")
        elif logType == "status":
            with open('LogFiles/StatusLog.txt', 'w') as StatusLog:
                StatusLog.write(f"{timestamp} OPERATIONAL")
        elif logType == "shutdown":
            with open('LogFiles/StatusLog.txt', 'w') as StatusLog:
                StatusLog.write(f"{timestamp} AUTHORISED SHUTDOWN")

def statusLogThread(): # Every 5 seconds it logs the status of the device, so I know when it was last on
    while not stopSystem:
        with logLock:
            logTime("status")
        time.sleep(5)
    

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
            buzzer.duty_u16(0)
            time.sleep(0.5)
    elif action == "correctPassword":
        turnOn("buzzer", )
    elif action == "incorrectPassword":
        turnOn("buzzer", 156) # Eb3
        time.sleep(0.3)
        buzzer.duty_u16(0)
        turnOn("buzzer", 98) # G2
        time.sleep(0.5)
        buzzer.duty_u16(0)

def userInputThread(): # Every 20ms it checks whether a button is being pressed and either turns off the device or preforms some other function
    buttonMain = Pin(14, Pin.INPUT, Pin.PULL_DOWN)
    button1 = Pin(10, Pin.INPUT, Pin.PULL_DOWN)
    button2 = Pin(11, Pin.INPUT, Pin.PULL_DOWN)
    button3 = Pin(12, Pin.INPUT, Pin.PULL_DOWN)
    button4 = Pin(13, Pin.INPUT, Pin.PULL_DOWN)

    passwordString = ""
    while True:
        time.sleep_ms(20)
        if button1.value() == 1:
            passwordString = passwordString + "1"
        elif button2.value() == 1:
            passwordString = passwordString + "2"
        elif button3.value() == 1:
            passwordString = passwordString + "3"
        elif button4.value() == 1:
            passwordString = passwordString + "4"
        elif buttonMain.value() == 1:
            if passwordString[-4:] == "1234":
                
        if "1234" in passwordString:
            with logLock:
                logTime("shutdown")
            while logLock.locked(): # Making sure not to turn off anything until the logs are complete. Not doing this could cause corruption
                time.sleep_ms(20)
            laserPin.value(0)
            stopSystem = True # When stopSystem is True, it is safe to unplug the device
        else:
            buzz("incorrectPassword")
            passwordString = ""
    while stopSystem:
        time.sleep_ms(20)
        if buttonMain.value() == 1:
            stopSystem = False
'''stopSystem will prevent any actuators from being turned on again, or any logs to happen.
This prevents anything from happening until the loops in the MainThread finish and don't execute again.'''

def LDRprint():
    while True:
        print(lightDetector.read_u16())
        time.sleep_ms(20)



laserPin = Pin(16, Pin.OUT)
lightDetector = ADC(Pin(26))
buzzer = PWM(Pin(17))
led = Pin(19, Pin.OUT)
timestamp = None
passwordString = ""
isLaserClear = True
stopSystem = False
logLock = _thread.allocate_lock()
buzzLock = _thread.allocate_lock()
_thread.start_new_thread(statusLogThread, ())
# _thread.start_new_thread(statusLogThread, ()) # Work on this later
# _thread.start_new_thread(LD Rprint, ())

laserPin.value(1)
time.sleep(0.5) # Time for the LDR to detect the laser
while True:
    while isLaserClear and not stopSystem: # Technically I don't need to use isLaserClear as a condition, but it makes it easier to identify the loops
        if lightDetector.read_u16() < 40000:
            laserPin.value(0)
            with logLock: # Log before buzzing because buzzing takes time and I need logging to be instantanious
                logTime("laserBlocked")
            with buzzLock:
                buzz("doorAlarm")
            isLaserClear = False
        time.sleep_ms(20)
            
    while not isLaserClear and not stopSystem:
        time.sleep(5)
        turnOn("laserPin")
        time.sleep(0.5)
        if lightDetector.read_u16() < 40000:
            laserPin.value(0)
        else: # The laser will be kept on
            with logLock:
                logTime("laserClear")
            isLaserClear = True
    
    if stopSystem: # 20 ms is so small it doesn't matter if it runs for no reason, but this if statement tells me what it does
        time.sleep_ms(20)
                    
            
# Modules:
# Passive buzzer, two colour LED, light dependant resistor, and RTC.
