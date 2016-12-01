#!/usr/bin/env python

from os import system
import curses
import configparser
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
           return self.config.getint(self.get_active_phase(), 'continue_manual')

      def get_continue_manual(self, phase):
           return self.config.get(phase, 'continue_manual')

      def get_active_action(self):
           return self.config.getint(self.get_active_phase(), 'action')

      def get_action(self, phase):
           return self.config.get(phase, 'action')


      def hasNextPhase(self):
           if self.phase_index < len(self.phases) - 1:
                 return 1
           else:
                 return 0

      def next(self):
           self.phase_index = self.phase_index + 1
      
class Heater:
      def __init__(self):
           self.heating = 0

      def heater_on(self):
           self.heating = 1

      def heater_off(self):
          self.heating = 0

      def heater_toggle(self):
          self.heating = not self.heating

      def is_heating(self):
           return self.heating

class Beeper:
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

	 


def getMinAndSek(secs):
     minutes = int((secs % 3600 ) / 60)
     seconds = secs % 60
     if(minutes == 0 and seconds == 0):
          return "--:--"
     else:
          return  '{:>3}:{:0>2}'.format(minutes, seconds)

def paint_screen(screen, recipe, termometer, timer, heater, beeper):
     screen.clear()
     screen.border(0)
     screen.addstr(2, 2, "Pi-Brew")
     screen.addstr(4, 2, "Running recipe " + recipe.get_name())
     screen.addstr(4, 30, "Temperatur: " + str(termometer.sensor_temp) + " °C" )
     screen.addstr(4, 55, "Gesammtzeit: " + getMinAndSek(int(timer.get_total_time())) + " min" )

     if heater.is_heating():
          screen.addstr(6, 30, "Heater: ON" )
     else:
          screen.addstr(6, 30, "Heater: OFF" )

     if beeper.is_beeping():
          screen.addstr(6, 55, "Beeper: ON" )
     else:
          screen.addstr(6, 55, "Beeper: OFF" )



     phase_num = 0

     for phase in recipe.get_phases():
          if phase != 'Main':
               temp = recipe.get_temp(phase)
               temp_div = termometer.temp_div()

               time = recipe.get_time(phase)
               time_div = timer.time_left()

               continue_manual = recipe.get_continue_manual(phase)
               action = recipe.get_action(phase)
			
               screen.addstr(9 + (phase_num * 2), 2, phase)
               screen.addstr(9 + (phase_num * 2), 30,  str(temp) + '°C')
               screen.addstr(9 + (phase_num * 2), 50,  str(time) + ' min')
               
               if phase == recipe.get_active_phase():
                    screen.addstr(9 + (phase_num * 2), 40,  str(temp_div) + '°C')
                    screen.addstr(9 + (phase_num * 2), 58,  getMinAndSek(time_div) + ' min')
			

               if continue_manual == '0':
                    screen.addstr(9 + (phase_num * 2), 70, 'auto')
               else:
                    screen.addstr(9 + (phase_num * 2), 70, 'manuel')

               if action == '1':
                    screen.addstr(9 + (phase_num * 2), 80, 'Alert')
               elif action == '2':
                     screen.addstr(9 + (phase_num * 2), 80, 'End')
               else:
                     screen.addstr(9 + (phase_num * 2), 80, ' - ')
                     
               phase_num = phase_num + 1

     
     if timer.isFinish() and not recipe.hasNextPhase():
         screen.addstr(9 + (phase_num * 2) + 2, 2, "========== DONE ==========")

     screen.addstr(9 + (phase_num * 2) + 4, 2, "Please enter '0' to exit.")
     if beeper.is_beeping():
         screen.addstr(9 + (phase_num * 2) + 4, 30, "To stop beeper hit <SPACE>.")
     screen.refresh()

def initPhase(recipe, timer, termometer, beeper):
     timer.stop()
     temp = recipe.get_active_temp()
     termometer.start(temp)
     beeper.set_active()
 
def show_recept(screen, recipe):
     refresh_interval = recipe.get_refresh_interval()
     screen.timeout(refresh_interval * 1000)
      
     timer = Timer()
     termometer = Termometer()
     heater = Heater()
     beeper = Beeper()

     initPhase(recipe, timer, termometer, beeper)               
     
     y = 0

     while y != ord('0'):    
          termometer.read_sensor_temp()
          
          if(y == ord(' ')):
                beeper.beeping_off()

          if(termometer.temp_div() >= 0.0 ):           
               heater.heater_off()
          else:
               heater.heater_on() 
          
          # Ist die Zieltemperatur erreicht und der Phasenzeit hat noch nicht begonnen,
          # DANN starte den Phasen timer
          if ((termometer.get_phase_reached()) and (not timer.get_started())):h
                _start_time = recipe.get_active_time()
                timer.start(int(_start_time))
                termometer.doStay()

          if (not recipe.get_active_continue_manual()) and timer.isFinish() and recipe.hasNextPhase():
               if(recipe.get_active_action() > 0):
                    beeper.beeping_on()
               recipe.next()
               initPhase(recipe, timer, termometer, beeper)    
               termometer.goUp()

          if recipe.get_active_continue_manual() and timer.isFinish() and recipe.hasNextPhase():
               if beeper.is_active():
                    beeper.beeping_on()
                    beeper.set_unactive()

               if(y == ord('c')):
                   recipe.next()
                   initPhase(recipe, timer, termometer, beeper)    
                   termometer.goUp()
          
              
          if timer.isFinish() and not recipe.hasNextPhase():
               timer.stop_total_time()
               
               if beeper.is_active():
                    beeper.beeping_on()
                    beeper.set_unactive()

          paint_screen(screen, recipe, termometer, timer, heater, beeper)
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

