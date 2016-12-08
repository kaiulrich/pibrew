#!/usr/bin/env python

import RPi.GPIO as GPIO

class ActiveBeeper:
      def __init__(self, gpio):
           self.gpio = gpio
           self.beeping = 0
           self.active = 1

      def beeping_on(self):
           self.beeping = 1
           GPIO.output(self.gpio,GPIO.HIGH)

      def beeping_off(self):
          self.beeping = 0
          GPIO.output(self.gpio,GPIO.LOW)

      def beeping_toggle(self):
          if(self.beeping):
                GPIO.output(self.gpio,GPIO.LOW)
          else:
                GPIO.output(self.gpio,GPIO.HIGH)

          self.beeping = not self.beeping

      def set_unactive(self):
          self.active = 0

      def set_active(self):
          self.active = 1

      def is_active(self):
           return self.active

      def is_beeping(self):
           return self.beeping

