# Assessment Task 2 - Mechatronics Documentation
## Requirements Outline

### Defining the purpose
**The need**

In my home when I enter my bedroom, I never know if it will be the same. Either my hairbrush's gone, my books are on the floor, or, *I shudder to think*, my bedroom's suddenly.. TIDY?! Unacceptable! However whenever I inquire, it's always "When?" or "No I didn't" or some other unhelpful, error deflecting response. Therefore I need something to help me keep track of when my bedroom is entered, so I can see at what time it happened and hopefully find out the deadbeat who commited this blunder. Using evidence like living room cameras which stretch to my door, this shouldn't be large of a case to crack.

**Proposed solution**

### Identify key actions

### Functional requirements

### Test cases

### Non-functional requirements

FROM threading IMPORT Thread # https://docs.python.org/3/library/threading.html
FROM machine IMPORT Pin
IMPORT time

BEGIN logTime(logType)
    IF stopSystem == False THEN
        IF logType == "laserBlocked" THEN
            SET doorLog TO OPEN 'LogFiles\DoorLog.txt' (mode=append)
            TO doorLog WRITE f"Door OPENED at {time}\n"
            CLOSE doorLog
        ELSE IF logType == "laserClear" THEN
            SET doorLog TO OPEN 'LogFiles\DoorLog.txt' (mode=append)
            TO doorLog WRITE f"Door CLOSED at {time}\n"
            CLOSE doorLog
        ELSE IF logType == "status" THEN
            SET statusLog TO OPEN 'Logfiles\StatusLog.txt' (mode=write)
            TO statusLog WRITE f"{time} OPERATIONAL"
            CLOSE statusLog
        ELSE IF logType == "shutdown" THEN
            SET statusLog TO OPEN 'LogFiles\StatusLog.txt' (mode=write)
            TO statusLog WRITE f"{time} AUTHORISED SHUTDOWN"
            CLOSE statusLog
        ENDIF
    ENDIF
END logTime

BEGIN statusLogThread
    WHILE stopSystem == False DO
        logTime("status")
        Pause 60 seconds
    ENDWHILE
END statusLogThread

START turnOn(device, tone=None) # This method is to make sure no devices turn on again 
    IF stopSystem == False THEN
        IF device == "laser" THEN
            WRITE laser TO low
        ELSE IF device == "buzzer" THEN
            WRITE buzzer TO HIGH (tone)
        ENDIF
    ENDIF

BEGIN userInputThread
    # Button creation below:
    SET button1 TO pin AS input (PULL_DOWN)
    SET button2 TO pin AS input (PULL_DOWN)
    SET button3 TO pin AS input (PULL_DOWN)
    SET button4 TO pin AS input (PULL_DOWN)
    SET button5 TO pin AS input (PULL_DOWN)
    SET button6 TO pin AS input (PULL_DOWN)
    SET button7 TO pin AS input (PULL_DOWN)
    SET button8 TO pin AS input (PULL_DOWN)
    SET button9 TO pin AS input (PULL_DOWN)

    WHILE True DO
        WAIT 10ms
        IF READ button1 == 1 THEN
            passwordString ADD "1"
        ELSE IF READ button2 == 1 THEN
            passwordString ADD "2"
        ELSE IF READ button3 == 1 THEN
            passwordString ADD "3"
        ELSE IF READ button4 == 1 THEN
            passwordString ADD "4"
        ELSE IF READ button5 == 1 THEN
            passwordString ADD "5"
        ELSE IF READ button6 == 1 THEN
            passwordString ADD "6"
        ELSE IF READ button7 == 1 THEN
            passwordString ADD "7"
        ELSE IF READ button8 == 1 THEN
            passwordString ADD "8"
        ELSE IF READ button9 == 1 THEN
            passwordString ADD "9"
        ENDIF
    
        IF "123456" IN passwordString THEN
            logTime(shutdown)
            WHILE doorLog.closed == False OR statusLog.closed == False DO
                WAIT 20 ms
            ENDWHILE
            SET stopSystem TO True # Immediately prevents any further changes to external devices
            WRITE laser TO LOW # Turns off device, now there's no risk it will turn back on
        ENDIF

BEGIN buzz(action) # Different sounds for different situations
    IF action == "doorAlarm" THEN
        FOR i = 0 TO 2 STEP 1 # Loops 3 times
            WRITE buzzer TO HIGH (0.2secs, lowSound)
            WAIT 0.2 secs
        NEXT i
    ELSE IF action == "armingLaser" THEN
        WRITE buzzer TO HIGH (0.2secs, lowSound)
        WAIT 0.2 secs
        WRITE buzzer TO HIGH (0.2secs, middleSound)
        WAIT 0.2 secs
        WRITE buzzer TO HIGH (0.2secs, highSound)
    ELSE IF action == "disarmingLaser" THEN
        WRITE buzzer TO HIGH (0.2secs, highSound)
        WAIT 0.2 secs
        WRITE buzzer TO HIGH (0.2secs, middleSound)
        WAIT 0.2 secs
        WRITE buzzer TO HIGH (0.2secs, lowSound)
END buzzerThread

BEGIN
    SET isLaserClear TO True
    SET passwordString TO ""
    SET laser TO pin AS output
    SET lightDetector TO pin AS input
    SET buzzer TO pin AS output
    SET led TO pin AS output
    SET stopSystem TO False # This is the only boolean I promise
    START thread statusLogThread
    START thread userInputThread

    WRITE laser TO HIGH
    WHILE True DO
        WHILE isLaserClear == True AND NOT stopSystem DO # Checks if the laser is clear or blocked
            WAIT 5 seconds
            IF READ lightDetector == 0 THEN
                WRITE laser to LOW
                CALL buzz WITH "doorAlarm"
                CALL logTime WITH "laserBlocked"
                SET isLaserClear TO False
            ENDIF
        ENDWHILE

        WHILE isLaserClear == False AND NOT stopSystem DO # Checks if the laser can work again
            WAIT 5 seconds # Allows time to see the laser is visably off
            WRITE laser TO HIGH
            WAIT 100 ms # Time for the light detector to detect the laser
            IF READ lightDetector == 0 THEN
                WRITE laser TO LOW
            ELSE IF READ lightDetector == 1 THEN
                CALL logTime with "laserClear"
                SET isLaserClear TO True # leaves the laser on for the next iteration in the external loop
            ENDIF
        ENDWHILE

        IF stopSystem == True THEN
            WAIT 1 second
        ENDIF
    ENDWHILE
