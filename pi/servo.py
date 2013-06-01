# Servo Control - thanks adafruit!! (http://learn.adafruit.com/adafruits-raspberry-pi-lesson-8-using-a-servo-motor/software)
import time
def set(property, value):
    with open("/sys/class/rpi-pwm/pwm0/" + property, 'w') as f:
        f.write(value)
        f.close()

def setServo(angle):
    set("servo", str(angle))



delay_period = 0.01

# 0 = forward
# 180 = backwards
# active = 0 = stop.

class ServoControl(object):
    def __init__(self):
        set("active", "0")
        set("delayed", "1")
        set("mode", "servo")
        set("servo_max", "180")
        set("servo", "0")
        self._is_on = False

    def start(self):
        set("active", "1")
        self._is_on = True
    
    def stop(self):
        set("active", "0")
        set("delayed", "1")
        self._is_on = False

    def pulse(self, dt):
        self.start()
        time.sleep(dt)
        self.stop()

    def is_on(self):
        return self._is_on
        
    def forward(self):
        setServo(0)
        
    def backwards(self):
        setServo(180)
    
class DummyServoControl(object):
    def __init__(self):
        self._is_on = False

    def start(self):
        self._is_on = True
    
    def stop(self):
        self._is_on = False

    def is_on(self):
        return self._is_on
        
    def forward(self):
        pass
        
    def backwards(self):
        pass
    
