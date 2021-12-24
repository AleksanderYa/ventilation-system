from machine import Pin
from machine import Signal
from machine import RTC
#from machine import ADC
from time import sleep
from light_sensor import lum
import dht
import time


class Fun:
    def __init__(self, pin):
        pin_ = Pin(pin, Pin.OUT)
        pin_control = Signal(pin_, invert=True)
    
    
class DHT:
"""
    DHT (Digital Humidity & Temperature)
"""
    def __init__(self, pin):
        pass
    
    
class Light_sensor:
    def __init__(self):
        pass
    