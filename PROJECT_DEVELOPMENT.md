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
    WHILE True
        time.sleep_ms(10)

BEGIN buzz(action) # Different sounds from different situations
    IF action == "doorAlarm" THEN
        FOR i = 0 TO 2 STEP 1 # Loops 3 times
            WRITE buzzer TO HIGH (0.2secs, lowSound)
            time.sleep(0.1)
        NEXT i
    ELSE IF action == "armingLaser" THEN
        WRITE buzzer TO HIGH (0.2, lowSound)
        time.sleep(0.1)
        WRITE buzzer TO HIGH (0.2secs, middleSound)
        time.sleep(0.1)
        WRITE buzzer TO HIGH (0.2secs, highSound)
    ELSE IF action == "disarmingLaser" THEN
        WRITE buzzer TO HIGH (0.2secs, highSound)
        time.sleep(0.1)
        WRITE buzzer TO HIGH (0.2secs, middleSound)
        time.sleep(0.1)
        WRITE buzzer TO HIGH (0.2secs, lowSound)
END buzzerThread




BEGIN
    SET isLaserClear TO True
    SET laser TO pin AS output
    WRITE laser TO HIGH
    SET lightDetector TO pin AS input 
    SET buzzer TO pin AS output
    START Thread (statusLogThread)
    thread(target=statusLogThread).start()


    WHILE True DO
        WHILE isLaserClear == True DO # Checks if the laser is clear or blocked
            WAIT 10 ms
            IF READ (lightDetector) == False THEN
                SET isLaserClear TO False
            ENDIF
        ENDWHILE

        WRITE laser to LOW
        CALL buzzerFunc WITH "doorAlarm"
        CALL logTime WITH "laser"
        ENDWHILE

        WHILE isLaserClear == False DO # Checks if the laser can work again
            time.sleep(5) # Allows time to see the laser is visably off
            laser.online()
            time.sleep_ms(10) # Time for the light detector to detect the laser
            IF lightDetector.offline THEN
                laser.offline()
            ELSE IF lightDetector.online THEN
                isLaserClear = True
            ENDIF
        ENDWHILE
    ENDWHILE



    



    IF not isLaserOn THEN
    