from machine import Pin
import threading
import time

isLaserClear = True
passwordString = ""
laser = Pin(16, Pin.OUT)
lightDetector = Pin(17, Pin.IN, Pin.PULL_DOWN)
buzzer = Pin(18, Pin.OUT)
led = Pin(19, Pin.OUT)
stopSystem = False
time = None
Thread(target=statusLogThread).start()
Thread(target=userInputThread).start()

def logTime(logType):
    if not stopSystem:
        if logType == "laserBlocked":
            with open('LogFiles\DoorLog.txt', a, encoding="utf-8"):
                doorLog.write(f"Door OPENED at {time}\n")
        elif logType == "laserClear":
            with open('LogFiles\DoorLog.txt', a, encoding="utf-8"):
                doorLog.write(f"Door CLOSED at {time}\n")
        elif logType == "status":
            with open('LogFiles\statusLog.txt', w, encoding="utf-8"):
                doorLog.write(f"{time} OPERATIONAL")
        elif logType == "shutdown":
            with open('LogFiles\StatusLog.txt', w, encoding="utf-8"):
                doorLog.write(f"{time} AUTHORISED SHUTDOWN")

def statusLogThread():
    while True:
        while not stopSystem:
            logTime("status")
            time.sleep(5)
        time.sleep_ms(20)

def turnOn(device):
    if not stopSystem:
        if device == "laser":
            laser.value(1)
        elif device == "buzzer":
            buzzer.value(1)

def buzz(action):
    if action == "doorAlarm":
        for i in range(3):
            turnOn("buzzer")
            time.sleep(0.2)
            buzzer.value(0)

def userInputThread():
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
                while not doorLog.closed and not statusLog.closed:
                    time.sleep_ms(20)
                stopSystem = True
                laser.value(0)
        while stopSystem:
            time.sleep_ms(20)
            if buttonMain.value() == 1:
                stopSystem = False         
            
            

laser.value(1)
while True:
    while isLaserClear and not stopSystem:
        time.sleep(5)
        if lightDetector.value() == 0:
            laser.value(0)
            buzz("doorAlarm")
            logTime("laserBlocked")
            isLaserClear = False
            
    while not isLaserClear and not stopSystem:
        time.sleep(5)
        turnOn("laser")
        time.sleep_ms(100)
        if lightDetector.value() == 0:
            laser.value(0)
        elif lightDetector.value() == 1:
            logTime("laserClear")
            isLaserClear = True
    time.sleep_ms(20)
            
            
            