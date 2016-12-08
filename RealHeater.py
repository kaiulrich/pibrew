#!/usr/bin/env python

import RPi.GPIO as GPIO


class RealHeater:
      def __init__(self, gpio):
           self.gpio = gpio
           self.heating = 0
           GPIO.setmode(GPIO.BCM)
           GPIO.setwarnings(False)
           GPIO.setup(self.gpio,GPIO.OUT)


      def heater_on(self):
           self.heating = 1
           GPIO.output(self.gpio,GPIO.HIGH)

      def heater_off(self):
          self.heating = 0
          GPIO.output(self.gpio,GPIO.LOW)

      def heater_toggle(self):
          if(self.heating):
                GPIO.output(self.gpio,GPIO.LOW)
          else:
                GPIO.output(self.gpio,GPIO.HIGH)

          self.heating = not self.heating

      def is_heating(self):
           return self.heating
