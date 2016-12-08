#!/usr/bin/env python

from os import system
import curses
import configparser
import time
from Timer import Timer
from Recipe import Recipe

from SimTermometer import SimTermometer
from SimHeater import SimHeater
from SimBeeper import SimBeeper

from DS18B20Termometer import DS18B20Termometer
from ActiveBeeper import ActiveBeeper
from RealHeater import RealHeater

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

     message = "Press '0' to exit."
     if beeper.is_beeping():
         message = message + "    Press 'SPACE' to stop beep."
 
     if recipe.is_waiting():
         message = message + "    Press 'c' to end active phase."
 
     screen.addstr(9 + (phase_num * 2) + 4, 2, message)
     
     screen.refresh()

def initPhase(recipe, timer, termometer, beeper):
     timer.stop()
     temp = recipe.get_active_temp()
     termometer.start(temp)
     beeper.set_active()
     recipe.end_waiting()
 
def show_recept(screen, recipe, termometer, heater, beeper):
     refresh_interval = recipe.get_refresh_interval()
     screen.timeout(refresh_interval * 1000)
      
     timer = Timer()

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
          if ((termometer.get_phase_reached()) and (not timer.get_started())):
               _start_time = recipe.get_active_time()
               timer.start(int(_start_time))
               termometer.doStay()

          # Ist die phase zu Ende und es gibt eine nächste phase .....
          if timer.isFinish() and recipe.hasNextPhase():        
  
               # ..... und der Phasenuebergang ist automatisch
               if not recipe.get_active_continue_manual():
                    if(recipe.get_active_action() > 0):
                         beeper.beeping_on()
                    recipe.next()
                    initPhase(recipe, timer, termometer, beeper)    
                    termometer.goUp()

               # ..... und der Phasenuebergang ist manuell
               if recipe.get_active_continue_manual():
                    
                    recipe.set_waiting()
                    if beeper.is_active():
                         beeper.beeping_on()
                         beeper.set_unactive()

                    if(y == ord('c')):
                        recipe.next()
                        initPhase(recipe, timer, termometer, beeper)    
                        termometer.goUp()
          
          # die letzte Phase ist beendet    
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
          #screen.addstr(7, 4, "2 - Re-run recept")
          screen.addstr(7, 4, "3 - Exit")
          screen.refresh()

          x = screen.getch()

          if x == ord('1'):
               if recipe.get_simulation():
                    termometer = SimTermometer()
                    heater = SimHeater()
                    beeper = SimBeeper()
               else:
                    termometer = DS18B20Termometer()
                    heater = RealHeater()
                    beeper = ActiveBeeper()
                
               recipe = Recipe(config)
               show_recept(screen, recipe, termometer, heater, beeper)

          #if x == ord('2'):
          #    show_recept(screen, recipe)

     curses.endwin()

curses.wrapper(main)

