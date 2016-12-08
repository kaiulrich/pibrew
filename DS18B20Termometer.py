#!/usr/bin/env python

class DS18B20Termometer:
      def __init__(self):
          self.up = 1
          self.phase_reached = 0
          self.sensor_temp = 43.0
          self.phase_temp = 0.0         

      def start(self, phase_temp):
           self.up = 1
           self.phase_reached = 0
           #self.sensor_temp = 43.0
           self.phase_temp = phase_temp
           

      def stop(self):
           self.up = 0
           self.phase_reached = 0
           self.sensor_temp = 0
           self.phase_temp = 0


      def read_sensor_temp(self):

           try:
               id = '28-000001de3702'
               mytemp = ''
               filename = 'w1_slave'
               f = open('/sys/bus/w1/devices/' + id + '/' + filename, 'r')
               line = f.readline() # read 1st line
               crc = line.rsplit(' ',1)
               crc = crc[1].replace('\n', '')
               if crc=='YES':
                 line = f.readline() # read 2nd line
                 mytemp = line.rsplit('t=',1)
               else:
                 mytemp = 99999
               f.close()

               self.sensor_temp = float(mytemp[1])

           except:
                self.sensor_temp = float(99999)

      def temp_div(self):
           return self.sensor_temp - self.phase_temp



      def goUp(self):
           self.up = 1

      def goDown(self):
           self.up = -1

      def doStay(self):
           self.up = 0


      def get_phase_reached(self):
           return self.phase_reached

      def get_sensor_temp(self):
           return self.sensor_temp

      def get_phase_temp(self):
           return self.phase_temp

      def get_up(self):
           return self.up
