#!/usr/bin/env python
import time

class Timer:
      def __init__(self):   
           self.total_time = 0
           self.total_time_runninng = 1
           self.total_time_start = time.time()
           self.started = 0
           self.start_time = 0
           self.phase_end = 0
        
      def start(self, phase_end):
           self.started = 1
           self.start_time = time.time()
           self.phase_end = phase_end * 60

      def stop(self):
           self.started = 0
           self.start_time = 0
           self.phase_end = 0
 
      def time_done(self):
           _time_done = int(time.time() - self.start_time)
           _end = self.phase_end
           if _time_done > _end:
                return _end
           else:
                return _time_done

      def isFinish(self):
           if (self.started == 0):
                return 0
           elif self.time_done() >= self.phase_end :
                return 1
           else :
                return 0   
   
      def time_left(self):
          if self.isFinish():
               return 0
          else:
               return int(self.phase_end - self.time_done())

      def get_started(self):
          return self.started

      def get_start_time(self):
          return self.start_time

      def get_phase_end(self):
          return self.phase_end

      def get_total_time(self):
          if(self.total_time_runninng):
               self.total_time = time.time() - self.total_time_start
          return self.total_time

      def stop_total_time(self):
          self.total_time_runninng = 0
