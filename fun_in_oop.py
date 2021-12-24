from machine import Pin
from machine import Signal
from machine import RTC
#from machine import ADC
from time import sleep
from light_sensor import lum
import dht
import time


class Fun:


    def __init__(self, pin: int):
        _pin_ = Pin(pin, Pin.OUT)
        # to normally open output -> invert=True
        self._pin_control = Signal(_pin_, invert=True)

    def on_fun(self):
        self._pin_control.on()
        return f"Fun {1} on"

    def off_fun(self):
        self._pin_control.off()
        return f"Fun {1} off"


class Fun_toilet(Fun):
    pass

class Fun_bathroom(Fun):
    pass

class Fun_out(Fun):
    pass

class DHT:
    """
        DHT (Digital Humidity & Temperature)
    """
    def __init__(self, pin):
        pass
    
    
class Light_sensor:
    def __init__(self):
        pass
    