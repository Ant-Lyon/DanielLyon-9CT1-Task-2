from machine import Pin, ADC, PWM
import _thread
import time

def logTime(logType): # Takes the type of time log and logs it
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
    with logLock:
        logTime("status")
    time.sleep(5)

def turnOn(device, tone=None): # Turns on a device but first checks whether or not stopSystem is True. If it is, it will not turn anything on
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
    elif action == "incorrectPassword":
        turnOn("buzzer", 156) # Eb3
        time.sleep(0.3)
        buzzer.duty_u16(0)
        turnOn("buzzer", 98) # G2
        time.sleep(0.5)
        buzzer.duty_u16(0)


laserPin = Pin(16, Pin.OUT)
lightDetector = ADC(Pin(26))
buzzer = PWM(Pin(17))
timestamp = None
isLaserClear = True
logLock = _thread.allocate_lock()
buzzLock = _thread.allocate_lock()
_thread.start_new_thread(statusLogThread, ())

laserPin.value(1)
time.sleep(0.5) # Time for the LDR to detect the laser
while isLaserClear: # Technically I don't need to use isLaserClear as a condition, but it makes it easier to identify the loops
    if lightDetector.read_u16() < 40000:
        laserPin.value(0)
        with logLock: # Log before buzzing because buzzing takes time and I need logging to be done at detection
            logTime("laserBlocked")
        with buzzLock:
            buzz("doorAlarm")
        isLaserClear = False
    time.sleep_ms(20)
        
while not isLaserClear:
    time.sleep(5)
    turnOn("laserPin")
    time.sleep(0.5)
    if lightDetector.read_u16() < 40000:
        laserPin.value(0)
    else: # The laser will be kept on
        with logLock:
            logTime("laserClear")
        isLaserClear = True