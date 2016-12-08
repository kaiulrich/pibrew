#!/usr/bin/env python


class SimBeeper:
      def __init__(self):
           self.beeping = 0
           self.active = 1

      def beeping_on(self):
           self.beeping = 1

      def beeping_off(self):
          self.beeping = 0

      def beeping_toggle(self):
          self.beeping = not self.beeping

      def set_unactive(self):
          self.active = 0

      def set_active(self):
          self.active = 1

      def is_active(self):
           return self.active

      def is_beeping(self):
           return self.beeping

