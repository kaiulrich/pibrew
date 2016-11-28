#!/usr/bin/env python

from os import system
import curses
import configparser
import time

class Timer:
      def __init__(self):
           self.running = 0
           self.start_time = 0
           self.time_to_run = 0
        
      def start(self, time_to_run):
           self.running = 1
           self.start_time = time.time()
           self.time_to_run = time_to_run

      def stop(self):
           self.running = 0
           self.start_time = 0
           self.time_to_run = 0
 
      def time(self):
           t = (time.time() - self.start_time) / 60
           if t > self.time_to_run:
                return self.time_to_run
           else:
                return t

      def isFinish(self):
           if self.running == 1 and self.time() > self.time_to_run * 60 :
                return 1
           else :
                return 0   
   
      def time_left(self):
          if self.isFinish():
               return 0
          else:
               return int(self.time_to_run - self.time())

class Termometer:
      def __init__(self):
          self.phase_reached = 0
          self.sensor_temp = 43.0
          self.phase_temp = 0.0         

      def start(self, phase_temp):
           self.phase_reached = 0
           self.phase_temp = phase_temp
           

      def stop(self):
           self.phase_reached = 0
           self.sensor_temp = 0
           self.phase_temp = 0


      def read_sensor_temp(self):
           self.sensor_temp = self.sensor_temp + 1
   
           if(not self.phase_reached and self.sensor_temp >= self.phase_temp):
                self.phase_reached = 1

      def temp_div(self):
           return self.sensor_temp - self.phase_temp





def paint_screen(screen, recipe, config, termometer, timer, active_phase):
     screen.clear()
     screen.border(0)
     screen.addstr(2, 2, "Pi-Brew")
     screen.addstr(4, 2, "Running recipe " + recipe)
     screen.addstr(4, 30, "Temperatur: " + str(termometer.sensor_temp) + " °C" )
     phase_num = 0

     for phase in config.sections():
          if phase != 'Main':
               temp = config.getint(phase, 'temp')
               temp_div = termometer.temp_div()

               time = config.getint(phase, 'time')
               time_div = timer.time_left()

               continue_manual = config.get(phase, 'continue_manual')
               action = config.get(phase, 'action')
			
               screen.addstr(8 + (phase_num * 2), 2, phase)
               screen.addstr(8 + (phase_num * 2), 30,  str(temp) + '°C')
               screen.addstr(8 + (phase_num * 2), 50,  str(time) + ' min')
               
               if phase == active_phase:
                    screen.addstr(8 + (phase_num * 2), 40,  str(temp_div) + '°C')
                    screen.addstr(8 + (phase_num * 2), 60,  str(time_div) + ' min')
			

               if continue_manual == '0':
                    screen.addstr(8 + (phase_num * 2), 70, 'auto')
               else:
                    screen.addstr(8 + (phase_num * 2), 70, 'manuel')

               if action == '1':
                    screen.addstr(8 + (phase_num * 2), 80, 'Alert')
               elif action == '2':
                     screen.addstr(8 + (phase_num * 2), 80, 'End')
               else:
                     screen.addstr(8 + (phase_num * 2), 80, ' - ')
                     
               phase_num = phase_num + 1

     screen.addstr(8 + (phase_num * 2) + 2, 2, "Please enter '0' to exit")
     screen.refresh()

def initPhase(config, phase_index, timer, termometer):
     phases = config.sections()
     active_phase = phases[phase_index]

     time = config.getint(active_phase, 'time')
     temp = config.getint(active_phase, 'temp')
     timer.start(time)
     termometer.start(temp)
     return active_phase

def show_recept(screen, config):
     refresh_interval = int(config['Main']['refresh_interval'])
     screen.timeout(refresh_interval * 1000)
      
     recipe = config['Main']['recipe']
     phases = config.sections()
     num_of_phases = len(phases)

     phase_index = 1
     timer = Timer()
     termometer = Termometer()
     active_phase = initPhase(config, phase_index, timer, termometer)               

     y = 0

     while y != ord('0'):    
          termometer.read_sensor_temp()

          if termometer.phase_reached and not timer.running:
                timer.start(time)

          if timer.isFinish() and phase_index < num_of_phases:
               phase_index = phase_index + 1  
               active_phase = initPhase(config, phase_index, timer, termometer)              
 
          paint_screen(screen, recipe, config, termometer, timer, active_phase)
          y = screen.getch()


def main(args):
     config = configparser.ConfigParser()
     config.read('pibrew.ini')
     x = 0
     while x != ord('3'):
          screen = curses.initscr()
          curses.cbreak()
          curses.noecho()
          curses.curs_set(0) 

          screen.clear()
          screen.border(0)
          screen.addstr(2, 2, "Pi-Brew")
          screen.addstr(4, 2, "Please enter a number...")
          screen.addstr(6, 4, "1 - Run recept")
          screen.addstr(7, 4, "2 - Re-run recept")
          screen.addstr(9, 4, "3 - Exit")
          screen.refresh()

          x = screen.getch()

          if x == ord('1'):
               show_recept(screen, config)

          if x == ord('2'):
              show_recept(screen, config)

     curses.endwin()

curses.wrapper(main)

