#!/usr/bin/env python

from os import system
import curses
import configparser



def run_recept():
     config = configparser.ConfigParser()
     config.read('pibrew.ini')
     recipe = config['Main']['recipe']
     y = 0
     
     while y != ord('0'):
          screen.clear()
          screen.border(0)
          screen.addstr(2, 2, "Pi-Brew")
          screen.addstr(4, 2, "Running " + recipe)
          phase_num = 0
          for phase in config.sections():
                if phase != 'Main':
                     screen.addstr(8 + (phase_num * 2), 2, phase)
                     screen.addstr(8 + (phase_num * 2), 30, config.get(phase, 'temp') + '°C')
                     screen.addstr(8 + (phase_num * 2), 40, config.get(phase, 'time') + ' min')

                     if config.get(phase, 'continue_manual') == '0':
                          screen.addstr(8 + (phase_num * 2), 50, 'auto')
                     else:
                          screen.addstr(8 + (phase_num * 2), 50, 'manuel')

                     if config.get(phase, 'action') == '0':
                          screen.addstr(8 + (phase_num * 2), 60, 'No Action')
                     elif config.get(phase, 'action') == '1':
                           screen.addstr(8 + (phase_num * 2), 60, 'Alert')
                     elif config.get(phase, 'action') == '2':
                           screen.addstr(8 + (phase_num * 2), 60, 'End')
                     else:
                           screen.addstr(8 + (phase_num * 2), 50, config.get(phase, 'action'))


                     phase_num = phase_num + 1

          screen.addstr(8 + (phase_num * 2) + 2, 2, "Please enter '0' to exit")
  
          screen.refresh()
          y = screen.getch()



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
          run_recept()

     if x == ord('2'):
          run_recept()


    

curses.endwin()

