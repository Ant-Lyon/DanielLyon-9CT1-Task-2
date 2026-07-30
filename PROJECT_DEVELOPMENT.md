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

FROM threading IMPORT Thread
IMPORT time

BEGIN laserChecker
    time.sleep(60)
    IF lightDetector.online THEN
        isLaserOn = True
    ELSE
        isLaserOn = False
    ENDIF
END laserChecker

BEGIN
    thread = Thread(target=laserChecker)
    thread.start()

    WHILE isLaserOn
    time.sleep(0.02)
    IF lightDetector.online THEN
        isLaserOn = True
    ELSE
        isLaserOn = False
    ENDIF
    ENDWHILE

    



    IF not isLaserOn THEN
    