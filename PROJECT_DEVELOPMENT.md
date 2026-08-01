# Assessment Task 2 - Mechatronics Documentation
## Requirements Outline

### Defining the purpose
**The need**

In my home when I enter my bedroom, I never know if it will be the same. Either my hairbrush's gone, my books are on the floor, or, *I shudder to think*, my bedroom's suddenly.. TIDY?! Unacceptable! However whenever I inquire, it's always "When?" or "No I didn't" or some other unhelpful, error deflecting response. Therefore I need something to help me keep track of when my bedroom is entered, so I can see at what time it happened and hopefully find out the deadbeat who commited this blunder. Using evidence like living room cameras which stretch to my door, this shouldn't be too much of an issue.

**Proposed solution**

### Identify key actions

### Functional requirements

### Test cases

### Non-functional requirements

FROM threading IMPORT Thread # https://docs.python.org/3/library/threading.html
FROM machine IMPORT Pin
IMPORT time

BEGIN logTime(logType)
    IF logType == "laser" THEN
        #log the laser idk
    ELSE IF logType == "status" THEN
        #log the status idk
    ENDIF
END logTime

BEGIN statusLogThread
    WHILE True DO
        logTime("status")
        Pause 60 seconds
    ENDWHILE
END statusLogThread

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
            # Turn off the system idk
        ENDIF

BEGIN buzz(action) # Different sounds from different situations
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
    START thread statusLogThread
    START thread userInputThread

    WRITE laser TO HIGH
    WHILE True DO
        WHILE isLaserClear == True DO # Checks if the laser is clear or blocked
            WAIT 10 seconds
            IF READ lightDetector == 0 THEN
                SET isLaserClear TO False
            ENDIF
        ENDWHILE

        WRITE laser to LOW
        CALL buzzerFunc WITH "doorAlarm"
        CALL logTime WITH "laser"

        WHILE isLaserClear == False DO # Checks if the laser can work again
            WAIT 5 seconds # Allows time to see the laser is visably off
            WRITE laser TO HIGH
            WAIT 100 ms # Time for the light detector to detect the laser
            IF READ lightDetector == 0 THEN
                WRITE laser TO LOW
            ELSE IF READ lightDetector == 1 THEN
                SET isLaserClear TO True # leaves the laser on for the next iteration in the external loop
            ENDIF
        ENDWHILE
    ENDWHILE
