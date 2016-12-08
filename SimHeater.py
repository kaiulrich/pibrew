#!/usr/bin/env python

class SimHeater:
      def __init__(self, gpio):
           self.heating = 0

      def heater_on(self):
           self.heating = 1

      def heater_off(self):
          self.heating = 0

      def heater_toggle(self):
          self.heating = not self.heating

      def is_heating(self):
           return self.heating
