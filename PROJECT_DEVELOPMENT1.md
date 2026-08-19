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
 
Buzzer Output - The system needs to activate a buzzer the exact moment the laser beam is broken and the light detector is triggered to alert the user that someone has entered the room.

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

#Enter code here

 ```


## Testing and Debugging

### Test Cases
#### Buzzer Output:
| Test Case | Input     | Expected Output   |
|---------- |---------- |----------------   |
| Laser beam untouched | Light detector continuously recieves the laser light | System waits and does not trigger the buzzer     |
| Intruder enters rooms | Laser beam is broken; light detector is triggered | Buzzer activates instantly to alert user. |

This worked very well, but only when I used a 10 K olm resistor for my voltage divider. We don't really know why it works except that a ratio is made by the two resistors, but Daniel Lyon's Dad wwho is an electrican said you don't need to know exactly HOW it works, just that it does, and how use it. The 10 K olm resistor meant we had the maximum u16 range, with at dark light levels averaged 1500 but with the laser shining into it at around 60000. Suprisingly, even in dark and very bright areas when the laser shone at the LDR the voltage would be 60000, then in light areas drop to around 50000. This made us toggle the system so that when the LDR detectors a light level of under 55000, it will detect.

The green buzzer broke, so we used Brandon's but then his broke. Rachael then told us to use the passive buzzer from Daniel's engineering kit, so we used that. We first tested the frequency of 440 (A note, octave 4), and liked it so stuck with it.

#### Time Logging Process:
| Test Case | Input     | Expected Output   |
|---------- |---------- |----------------   |
| Intruder inside room | Laser beam stays broken while person is inside | System waits and does not log a final time yet |
| Intruder leaves room | Laser beam is restored; light detector recieves light again | System captures the exact current time as the final time. |

This worked very well, but only when we used a 10 K olm resistor for my voltage divider. We don't really know why it works except that a ratio is made by the two resistors, but Daniel Lyon's Dad who is an electrican said you don't need to know exactly HOW it works, just that it does, and how use it. The 10 K olm resistor meant we had the maximum u16 range, with at dark light levels averaged 1500 but with the laser shining into it at around 60000. Suprisingly, even in dark and very bright areas when the laser shone at the LDR the voltage would be 60000, then in light areas drop to around 50000. This made us toggle the system so that when the LDR detectors a light level of under 55000, it will detect.

When the time is logged you only know when the person closed the door, because the time overrights every minute until the LDR detectors light again. This means we don't know when they came into the room, only when they left, or even just went they closed the door presuming they did. Furthermore, the system is then limited to one log, because if they come inside again you only see the last time the door was closed. So to fix these issues, instead of overwriting the file with the 'w' tuple in the 'open()' method, we replaced it with the 'a' argument instead. In addition, we made it so the time logs when the door was opened. Once the door is opened, every five seconds the laser will shine (or 2 seconds if the buzzer was just activated, which takes 3 seconds), wait 0.5 seconds are the LDR to detect, and if the LDR does it will stay on and wait for the door to be opened again. As well as this, in the same .txt file it will log the time the door is closed. This means you have a good idea of when the door is opened, and when perhaps it was closed again.

#### Memory System Process:
| Test Case | Input     | Expected Output   |
|---------- |---------- |----------------   |
| Intruder inside room | Laser beam stays broken as time passes | System overwrites the previous time; replaces it with the current time in the memory |
| Intruder leaves room | Laser beam is restored | System stops deleting, retains the final exit time and saves it. |

We needed a way to deal with somebody sabotaging the system and turning it off. So, every five seconds the time will be logged, then five seconds later it will overwrite the previous

#### Data Storing Process:
| Test Case | Input     | Expected Output   |
|---------- |---------- |----------------   |
| System is turned off | Cables and wires are disconnected or switches are turned off | System completely shuts down, but the final time is kept safe in the memory variable |
| System is turned back on | Cables and wires are connected and switches are turned on | System powers up and successfully displays the final time before the shutdown. |


WRITE A PARAGRAPH EVALUATING


### Final Product


Film a video of your final product working. Include this in your Github repo if it fits, or submit separately to Google Classroom.

Include all final Thonny / VS Code files and folder structure in your Github, all test cases in your documentation, and include all commits. 
