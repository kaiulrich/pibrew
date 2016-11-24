#!/usr/bin/env python

from os import system
import curses

def get_param(prompt_string):
     screen.clear()
     screen.border(0)
     screen.addstr(2, 2, prompt_string)
     screen.refresh()
     input = screen.getstr(10, 10, 60)
     return input

def execute_cmd(cmd_string):
     system("clear")
     a = system(cmd_string)
     print ""
     if a == 0:
          print "Command executed correctly"
     else:
          print "Command terminated with error"
     raw_input("Press enter")
     print ""

x = 0

def run_recept:
     while x != ord('0'):
          screen.clear()
          screen.border(0)
          screen.addstr(2, 2, "Pi-Brew")
          screen.addstr(4, 2, "Please enter a number...")
          screen.addstr(6, 4, "1 - Run recipe")
          screen.addstr(7, 4, "2 - Re-run recipe")
          screen.addstr(9, 4, "3 - Exit")
          screen.refresh()

	     x = screen.getch()

	     if x == ord('1'):
		  username = get_param("Enter the username")
		  curses.endwin()
		  execute_cmd("echo 'Start rezept: " + username + "'")
	     if x == ord('2'):
		  curses.endwin()
		  execute_cmd("echo 'Restart running rezept'")



while x != ord('3'):
     screen = curses.initscr()

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
          username = get_param("Enter the username")
          curses.endwin()
          execute_cmd("echo 'Start rezept: " + username + "'")
     if x == ord('2'):
          curses.endwin()
          execute_cmd("echo 'Restart running rezept'")
    

curses.endwin()

