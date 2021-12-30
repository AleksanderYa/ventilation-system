from machine import Pin
from machine import I2C
from machine import Signal
from machine import Timer
from machine import RTC
from time import sleep
from time import localtime
import dht
import time


# Fun control
class Fun:
    def __init__(self, pin:int, name:str=None):
        _pin_ = Pin(pin, Pin.OUT)
        # to normally open output -> invert=True
        self._pin_control = Signal(_pin_, invert=True)
        self.name = name

    def on(self):
        self._pin_control.on()
        print(b"{0}-fun is on".format(self.name))
        
    def off(self):
        self._pin_control.off()
        print(b"{0}-fun is off".format(self.name))

class Fun_controller:
    def __init__(self):
        self.toilet_fun = Fun(name='Toilet', pin=16)
        self.bathroom_fun = Fun(name='Bathroom', pin=2)
            
    def start(self):
        self.toilet_fun.on()
        sleep(1)
        self.toilet_fun.off()
        
        self.bathroom_fun.on()
        sleep(1)
        self.bathroom_fun.off()

class DHT:
    """
        DHT (Digital Humidity & Temperature)
    """
    def __init__(self, pin:int):
        sensor = dht.DHT11(Pin(0, Pin.IN, Pin.PULL_UP))
        
        
def humm():
    '''
    Возвращает влажность с датчика от 0 до 95...
    '''
    try:
        sensor = dht.DHT11(Pin(0, Pin.IN, Pin.PULL_UP)) # инициалицация сенсора
        sleep(1) # спим сикунду что бы собрать более точные данные
        sensor.measure() # что то там важное, толи сбор данных с датчика
        hum =  sensor.humidity() # конкретно влажность
        return hum
    except Exception as e:
        err()
        print(e)
        
# Time control      
class Real_time:
    
    def __init__(self):
        self._time = localtime()
        self.real_time = RTC()
        
    def now(self):
        res = self.real_time.datetime()
        print(res)
        return res   

class Timers:
    
    def __init__(self,id_timer):
        """
        id- in must be for init Timer class, its positional nomber of  timer
        func - what function is callback
        mode=True, timer mode. If True ONE_SHOT mode, alse PERIODIC
        period - in miliseconds  
        """
        try:
            self.id_timer = id_timer
            self.timer = Timer(self.id_timer)
        except Exception as e:
            print('set_timer', e)
            
    def set_timer(self, *args):
        # self, mode=Timer.ONE_SHOT, period=2000, callback=lambda:print('hi')
        try:
            self.timer.init(*args, mode=Timer.ONE_SHOT, callback=lambda:print('hi'), period=1000)
        except Exception as e:
            print('set_timer', e)
            
# Light sensor

class Light_control:
    
    def __init__(self, first_pin_i2c:int=5, second_pin_i2c:int=4):
        self.sensor = I2C(Pin(first_pin_i2c), Pin(second_pin_i2c))

    def is_there_light(self):
        try:
            result = Light_sensor.value(self.sensor)
            print('{result}'.format())
        except Exception as e:
            print(e)
            
        return result
 
class Light_sensors:
    
    OP_SINGLE_HRES1 = 0x20
    OP_SINGLE_HRES2 = 0x21
    OP_SINGLE_LRES = 0x23

    DELAY_HMODE = 180  # 180ms in H-mode
    DELAY_LMODE = 24  # 24ms in L-mode
    
    @staticmethod 
    def value(i2c, mode=OP_SINGLE_HRES1, i2c_addr=0x23):
        """
            Performs a single sampling. returns the result in lux
        """

        i2c.writeto(i2c_addr, b"\x00")  # make sure device is in a clean state
        i2c.writeto(i2c_addr, b"\x01")  # power up
        i2c.writeto(i2c_addr, bytes([mode]))  # set measurement mode

        time.sleep_ms(DELAY_LMODE if mode == OP_SINGLE_LRES else DELAY_HMODE)

        raw = i2c.readfrom(i2c_addr, 2)
        i2c.writeto(i2c_addr, b"\x00")  # power down again

        # we must divide the end result by 1.2 to get the lux
        return ((raw[0] << 24) | (raw[1] << 16)) // 78642