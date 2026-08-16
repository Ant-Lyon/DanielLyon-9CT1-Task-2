import os
import time
from machine import Pin, ADC, PWM

buzzerPin = PWM(Pin(17))
def buzz(tone):
    buzzerPin.freq(tone)
    buzzerPin.duty_u16(32728)

buzz(156)
time.sleep(0.3)
buzzerPin.duty_u16(0)
buzz(98)
time.sleep(0.5)
buzzerPin.duty_u16(0)
