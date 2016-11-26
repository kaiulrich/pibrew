#!/usr/bin/env python

from os import system
import curses
import configparser
import atexit

def my_cleanup(name):
    print (name)

atexit.register(my_cleanup, 'first')


def get_sensor_temp(sensor_temp):
     sensor_temp = sensor_temp + 1
     return sensor_temp

def paint_screen(screen, recipe, config, currentTemp, currentTime, active_phase):
     screen.clear()
     screen.border(0)
     screen.addstr(2, 2, "Pi-Brew")
     screen.addstr(4, 2, "Running recipe " + recipe)
     screen.addstr(4, 30, "Temperatur: " + str(currentTemp) + " °C" )
     phase_num = 0

     for phase in config.sections():
          if phase != 'Main':
               temp = config.getfloat(phase, 'temp')
               temp_div = currentTemp - temp

               time = config.getint(phase, 'time')
               time_div = time - currentTime
               if time_div < 0:
                     time_div = 0

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



def show_recept(screen, config):
     refresh_interval = int(config['Main']['refresh_interval'])
     screen.timeout(refresh_interval * 1000)
      
     recipe = config['Main']['recipe']
     phases = config.sections()

     active_phase = phases[2]
	
     currentTemp = 15
     currentTime = 12
     
     y = 0

 
     while y != ord('0'):
          currentTemp = get_sensor_temp(currentTemp)
          currentTime = 12
		
          atexit.register(my_cleanup, str(currentTemp))
          paint_screen(screen, recipe, config, currentTemp, currentTime, active_phase)
	
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

