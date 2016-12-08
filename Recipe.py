#!/usr/bin/env python

import configparser

class Recipe:
      def __init__(self, config):
           self.config = config
           self.phases = config.sections()
           self.phase_index = 1
           self.waiting = 0

      def get_phases(self):
           return self.phases

      def get_name(self):
           return self.config.get('Main', 'recipe')

      def get_refresh_interval(self):
           return self.config.getint('Main', 'refresh_interval')

      def get_active_phase(self):
           return self.phases[self.phase_index]
      
      def get_active_time(self):
           return self.config.getint(self.get_active_phase(), 'time')

      def get_time(self, phase):
           return self.config.getint(phase, 'time')

      def get_active_temp(self):
           return self.config.getint(self.get_active_phase(), 'temp')

      def get_temp(self, phase):
           return self.config.getint(phase, 'temp')

      def get_active_continue_manual(self):
           return self.config.getint(self.get_active_phase(), 'continue_manual')

      def get_continue_manual(self, phase):
           return self.config.get(phase, 'continue_manual')

      def get_active_action(self):
           return self.config.getint(self.get_active_phase(), 'action')

      def get_action(self, phase):
           return self.config.get(phase, 'action')

      def set_waiting(self):
          self.waiting = 1

      def end_waiting(self):
          self.waiting = 0

      def is_waiting(self):
           return self.waiting


      def hasNextPhase(self):
           if self.phase_index < len(self.phases) - 1:
                 return 1
           else:
                 return 0

      def next(self):
           self.phase_index = self.phase_index + 1
