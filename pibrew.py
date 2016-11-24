#!/usr/bin/env python

from os import system
import curses
import configparser

x = 0

def run_recept():
     config = configparser.ConfigParser()
     config.read('pibrew.ini')
     recipe = config['Main']['recipe']
     screen.clear()
     screen.border(0)
     screen.addstr(2, 2, "Pi-Brew")
     screen.addstr(4, 2, "Running " + recipe + ". Please enter a '0' to exit")
     screen.refresh()

     x = screen.getch()
     
     while x != ord('0'):
          x = screen.getch()
          screen.refresh()




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

