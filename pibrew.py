#!/usr/bin/env python

from os import system
import curses
import configparser
import time

class Timer:
      def __init__(self):
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

class Termometer:
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
           self.sensor_temp = self.sensor_temp + self.up
   
           if(not self.phase_reached and self.sensor_temp >= self.phase_temp):
                self.phase_reached = 1

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

class Recipe:
      def __init__(self, config):
           self.config = config
           self.phases = config.sections()
           self.phase_index = 1

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
           return self.config.get(self.get_active_phase(), 'continue_manual')

      def get_continue_manual(self, phase):
           return self.config.get(phase, 'continue_manual')

      def get_active_action(self):
           return self.config.get(self.get_active_phase(), 'action')

      def get_action(self, phase):
           return self.config.get(phase, 'action')


      def hasNextPhase(self):
           if self.phase_index < len(self.phases):
                 return 1
           else:
                 return 0

      def next(self):
           self.phase_index = self.phase_index + 1
      
class Heater:
      def __init__(self):
           self.heater_on = 0

      def heater_on(self):
           self.heater_on = 1

      def heater_off(self):
          self.heater_on = 0

      def heater_toggle(self):
          self.heater_on = not self.heater_on

      def is_heater_on(self):
           return self.heater_on


def getMinAndSek(secs):
     minutes = int((secs % 3600 ) / 60)
     seconds = secs % 60
     if(minutes == 0 and seconds == 0):
          return "--:--"
     else:
          return  '{:>3}:{:0>2}'.format(minutes, seconds)

def paint_screen(screen, recipe, termometer, timer):
     screen.clear()
     screen.border(0)
     screen.addstr(2, 2, "Pi-Brew")
     screen.addstr(4, 2, "Running recipe " + recipe.get_name())
     screen.addstr(4, 30, "Temperatur: " + str(termometer.sensor_temp) + " °C" )
     phase_num = 0

     for phase in recipe.get_phases():
          if phase != 'Main':
               temp = recipe.get_temp(phase)
               temp_div = termometer.temp_div()

               time = recipe.get_time(phase)
               time_div = timer.time_left()

               continue_manual = recipe.get_continue_manual(phase)
               action = recipe.get_action(phase)
			
               screen.addstr(8 + (phase_num * 2), 2, phase)
               screen.addstr(8 + (phase_num * 2), 30,  str(temp) + '°C')
               screen.addstr(8 + (phase_num * 2), 50,  str(time) + ' min')
               
               if phase == recipe.get_active_phase():
                    screen.addstr(8 + (phase_num * 2), 40,  str(temp_div) + '°C')
                    screen.addstr(8 + (phase_num * 2), 58,  getMinAndSek(time_div) + ' min')
			

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

def initPhase(recipe, timer, termometer):
     timer.stop()
     temp = recipe.get_active_temp()
     termometer.start(temp)
 
def show_recept(screen, recipe):
     refresh_interval = recipe.get_refresh_interval()
     screen.timeout(refresh_interval * 1000)
      
     timer = Timer()
     termometer = Termometer()
     initPhase(recipe, timer, termometer)               
     
     y = 0

     while y != ord('0'):    
          termometer.read_sensor_temp()

          if ((termometer.get_phase_reached()) and (not timer.get_started())):
                _start_time = recipe.get_active_time()
                timer.start(int(_start_time))
                termometer.doStay()

          if timer.isFinish() and recipe.hasNextPhase():
               recipe.next()
               initPhase(recipe, timer, termometer)    
               termometer.goUp()

          paint_screen(screen, recipe, termometer, timer)
          y = screen.getch()


def main(args):
     config = configparser.ConfigParser()
     config.read('pibrew.ini')
     recipe = Recipe(config)
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
               recipe = Recipe(config)
               show_recept(screen, recipe)

          if x == ord('2'):
              show_recept(screen, recipe)

     curses.endwin()

curses.wrapper(main)

