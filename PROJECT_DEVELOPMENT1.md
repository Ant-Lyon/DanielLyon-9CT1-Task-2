# Assessment Task 2: MECHATRONICS DOCUMENTATION
## Requirements Outline

### Defining the Purpose
-------- The Need --------

In my home when I enter my bedroom, I never know if it will be the same. Either my hairbrush's gone, my books are on the floor, or, *I shudder to think*, my bedroom's suddenly.. TIDY?! Unacceptable! However whenever I inquire, it's always "When?" or "No I didn't" or some other unhelpful, error deflecting response. Therefore I need something to help me keep track of when my bedroom is entered, so I can see at what time it happened and hopefully find person who commited this blunder. Using evidence like living room cameras which stretch to my door, this shouldn't be too much of a case to crack.

-------- Proposed Solution --------

An open loop security system shines a laser into a light detector triggering a buzzing noise to alert the user when an intruder blocks the beam. To stop someone from unplugging the device, the memory overwrites the time every minute while the room is occupied but locks the time when they exit. This means if the system is turned off the memory still retains the very last time it was active, letting you know exactly when it stopped working.

### Key Actions
 - Laser shines into a light detector triggering a buzzing noise.
 - While room is occupied, the memory overwrites the time every minute but saves the final time the moment they exit. 
 - If switched off the memory retains the very last time it was active


### Functional Requirements
The functional requirements for my security system list the key actions the mechanism needs to follow to detect intrusions and record important information:
 
Buzzer Output - The system needs to activate a buzzer the exact moment the laser beam is broken and the light detector is triggered to alert the user that someone has entered the room. This will hopefully invoke paranoia as they know I have detected them.

Memory System Process - Every minute the system should delete the last time that was stored and replace it with a new one so the memory always stays updated. 

Time Logging Process - It must record and log the time the person leaves the room so the user knows exactly when the intruder left.

Data Storing Process -  If system is switched off it must retain the very last time it was active so the user can be notified.


### Test Cases
#### Buzzer Output:
| Test Case | Input     | Expected Output   |
|---------- |---------- |----------------   |
| Laser beam untouched | Light detector continuously recieves the laser light | System waits and does not trigger the buzzer |
| Intruder enters room | Laser beam is broken; light detector is triggered | Buzzer activates instantly to alert user. |

#### Time Logging Process:
| Test Case | Input     | Expected Output   |
|---------- |---------- |----------------   |
| Intruder inside room | Laser beam stays broken while person is inside | System waits and does not log a final time yet |
| Intruder leaves room | Laser beam is restored; light detector recieves light again | System captures the exact current time as the final time. |

#### Memory System Process:
| Test Case | Input     | Expected Output   |
|---------- |---------- |----------------   |
| Intruder inside room | Laser beam stays broken as time passes | System overwrites the previous time; replaces it with the current time in the memory |
| Intruder leaves room | Laser beam is restored | System stops deleting, retains the final exit time and saves it. |

#### Data Storing Process:
| Test Case | Input     | Expected Output   |
|---------- |---------- |----------------   |
| System is turned off | Cables and wires are disconnected or switches are turned off | System completely shuts down, but the final time is kept safe in the memory variable |
| System is turned back on | Cables and wires are connected and switches are turned on | System powers up and successfully displays the final time before the shutdown. |


### Non-Functional Requirements
The non-functional requirements for my security system list the performance expectations, speed, and accuracy the mechanism must sustain to achieve it's goal of running effectively and being reliable:

Efficiency - The system must run smoothly so that updating the memory every minute doesnt slow down/freeze the device.

Response Time - The buzzer must work within 0.5 seconds of the laser beam being broken so the intruder is alerted instantly.

Accuracy - The light detector must have 100% accuracy in distinguishing between the laser light and a normal bedroom light so it never starts a false alarm.




## Algorithms

### Flowchart (Two Subroutines and Mainline Routine)
![alt text](Flowchart.png)


### Psuedocode
START

    --- System Setup ---
    Set up system and memory variables
    Turn system ON
    Set alarm state to ON
    Turn laser ON
    Run Minute_logging()

    --- Main Monitoring ---
    LOOP forever
        Check light detector
        IF laser is NOT blocked THEN
            INPUT 'Continue monitoring?'
                IF answer == NO THEN
                    Turn system OFF
                    EXIT LOOP
                ELSE
                    Go back to checking light detector
                ENDIF

        ELSE IF laser is blocked THEN
            Run Intrusion_Logging()
            INPUT 'Continue monitoring?'
                IF answer == NO THEN
                    Turn system OFF
                    EXIT LOOP
                ELSE
                    Go back to checking light detector
                ENDIF
        ENDIF
    ENDLOOP

END


START Minute_logging()
    
    LOOP forever
        INPUT 'Is system ON?'
            IF answer == YES THEN
                Record current time
                Save time to memory variable
                Wait 1 minute

            ELSE
                Wait 1 minute
                END MinuteLogging
            ENDIF
    ENDLOOP

END Minute_logging


Start Intrusion_logging()
    
    Record intrusion time
    Activate buzzer
    Save intrusion time to memory
    END IntrusionLogging

END Intrusion_logging




## Development and Integration


Add your first attempt as a code window in your markdown documentation:
eg: 

 ```Python 
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
 ```


## Testing and Debugging

### Test Cases
#### Buzzer Output:
| Test Case | Input     | Expected Output   |
|---------- |---------- |----------------   |
| Laser beam untouched | Light detector continuously recieves the laser light | System waits and does not trigger the buzzer     |
| Intruder enters rooms | Laser beam is broken; light detector is triggered | Buzzer activates instantly to alert user. |

This worked very well, but only when I used a 10 K olm resistor for my voltage divider. We don't really know why it works except that a ratio is made by the two resistors, but Daniel Lyon's Dad who is an electrican said you don't need to know exactly HOW it works, just that it does, and how use it. The 10 K olm resistor meant we had the maximum u16 range, with at dark light levels averaged 1500 but with the laser shining into it at around 60000. Suprisingly, even in dark and very bright areas when the laser shone at the LDR the voltage would be 60000, then in light areas drop to around 50000. This made us toggle the system so that when the LDR detectors a light level of under 55000, it will detect.

The green buzzer broke, so we used Brandon's but then his broke. Rachael then told us to use the passive buzzer from Daniel's engineering kit, so we used that. We first tested the frequency of 440 (A note, octave 4), and liked it so stuck with it.

#### Time Logging Process:
| Test Case | Input     | Expected Output   |
|---------- |---------- |----------------   |
| Intruder inside room | Laser beam stays broken while person is inside | System waits and does not log a final time yet |
| Intruder leaves room | Laser beam is restored; light detector recieves light again | System captures the exact current time as the final time. |

When the time is logged you only know when the person closed the door, because the time overrights every minute until the LDR detectors light again. This means we don't know when they came into the room, only when they left, or even just went they closed the door presuming they did. Furthermore, the system is then limited to one log, because if they come inside again you only see the last time the door was closed. So to fix these issues, instead of overwriting the file with the 'w' tuple in the 'open()' method, we replaced it with the 'a' argument instead. In addition, we made it so the time logs when the door was opened. Once the door is opened, every five seconds the laser will shine (or 2 seconds if the buzzer was just activated, which takes 3 seconds), wait 0.5 seconds are the LDR to detect, and if the LDR does it will stay on and wait for the door to be opened again. As well as this, in the same .txt file it will log the time the door is closed. This means you have a good idea of when the door is opened, and when perhaps it was closed again.

When we implemented this and tested it, when the laser was tripped, it instantly turned off, appended a log, then after 5 seconds shone are half a second then turned off again, unless the door was closed again and the LDR detected the light, making it stay on and finally logging when the door was closed. So no, this test case failed, not because of faulty code but a turn to a better idea, so we never tested it.

#### Status Logging Process:
| Test Case | Input     | Expected Output   |
|---------- |---------- |----------------   |
| System is turned off | Cables and wires are disconnected or switches are turned off | System completely shuts down, but the final time is kept safe in the memory variable |
| System is turned back on | Cables and wires are connected and switches are turned on | System powers up and successfully displays the final time before the shutdown. |

We needed a way to deal with somebody sabotaging the system and turning it off. So, every five seconds the time will be logged in a seperate .txt file, then five seconds later it will overwrite the previous (using 'w') so that if the system is turned off then the last time it was on will be logged. This means we can see who entered the bedroom at that time, and messed with the system. Overall no changed to our original idea for this one.

### Final Evaluation

#### Evaluate your Final Test in Relation to Functional Criteria
The system successfully could detect with no error when the door was opened, and then closed and it could differentiate between these because when the door is opened the laser cannot reach the LDR. The buzzer worked very well, and the data logging process for the door was perfect. Instead of overwriting the time until the door is closed, it would append the time to a .txt file when it was opened AND closed with great accuracy and speed. Last minute, we made it so a new one of these doorLog files would be made, separated by the dates, so we have one for everyday so it doesn't get too big and lead to a doomscrolling session. The status logger worked very well. Using the '_thread' library for MicroPython, it could successfully log the time every 5 seconds, overwriting itself when 5 seconds elapsed again. this meant we could easily know when the system was last turned off and find out who preformed the sabotage. This also improved the security of the system so people could know not to touch it. The RTC we used, the DS1302 with a driver that was found on GitHub, also worked very well. It kept the time accurately, and the driver made it very easy to read and write the time. Overall, for the functional parts the system was very successful.

#### Evaluate your Final Test in Relation to Non-Functional Criteria
The non-functional criteria was met to the full extent. As we said before, laser could differenciate the difference between the door opened and closed very well. This is because, again, when the door opens the tripwire is set off, and when it says that way the door blocks the laser. So, every five seconds when the laser turns on for half a second to check is the LDR picked up the light, if it doesn't pick it up then the door is opened, and if it does then it is closed. When we first turned on our program, we gave the LDR half a second to detect whether the laser is hitting it, same when we were doing the same to see of the door is closed again. However, when the tripwire is primed (door is closed), We give a delay of 20ms between checks, for maximum speed. The reason for this is because we want system to log when it is opened immediately, and at the start we give it a lot of time so that the system doesn't accidently go wrong. Like at the beginning we don't want it to immediately think the door is opened.

#### Evaluate your Final Performance in Relation to the Identified Need
Due to the success in meeting all the functional requirements with quality, our needs where absolutely met. The system could successfully log whenever the door was opened for closed, with the added security of the status logger. This means if, say, Daniel Lyon's sister comes into Daniel's room looking to plunder a hairbrush, the device will log when she came in and out, as well as hopefully invoke paranoia since she knows she is not slick. Then if she comes up with the bright idea to tamper with the system, it will log when she did it, leaving great evidence for an interrogation.

#### Evaluate your Project in Relation to Project Management
We managed time with our project well, only behind behind by about half a week at times. For the main file, we first researched what we need, being threads and the 'open()' method. We then worked on making sure the laser and the LDR worked somewhat well, then moved on to making the log for the door, and the status log using the '_thread' library. The whole time, the 'timestamp' variable was set to 'None', until we added the programming for the RTC, then configured the logs to fit the time. We then ran some tests to see the light level when the LDR was shone by the laser (60000), then calibrated the minimum light level required to set off the system (55000). Then we wired it up to a door and tested to see if the whole thing worked (which it did), and filmed it.

#### Evaluate your Project in Relation to Peer Feedback.


#### Justify Future Improvements you could make to your Final Product
