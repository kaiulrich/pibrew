#!/usr/bin/env python

class RealHeater:
      def __init__(self, gpio):
           self.gpio = gpio
           self.heating = 0
           GPIO.setmode(GPIO.BCM)
           GPIO.setwarnings(False)
           GPIO.setup(gpio,GPIO.OUT)


      def heater_on(self):
           self.heating = 1
           GPIO.output(gpio,GPIO.HIGH)

      def heater_off(self):
          self.heating = 0
          GPIO.output(gpio,GPIO.LOW)

      def heater_toggle(self):
          if(self.heating):
                GPIO.output(gpio,GPIO.LOW)
          else:
                GPIO.output(gpio,GPIO.HIGH)

          self.heating = not self.heating

      def is_heating(self):
           return self.heating
