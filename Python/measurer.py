#!/usr/bin/python3
# The lab07 Python script uses the sys and the lib modules.
# It receives 2 parameters. The first one is implicit and is the name of the
# script, the second is the mode through which launch the script.
# The script can be executed in terminal or GUI mode.


import sys
import lib
import os

error_state = 0
if len(sys.argv) == 2: #check the number of parameters passed to the lab07 Pyhton module
    if sys.argv[1] == '-t' : #terminal mode
        print ('Welcome to the LAB07 script!')
        while True:
            lib.displayMenu()
            what_to_do_flag = lib.getInput('')
            if what_to_do_flag == 'q':
                print('Bye Bye!')
                sys.exit([error_state])
            elif what_to_do_flag == 'y':
                error_state = lib.turn_on_LED_terminal()
            elif what_to_do_flag == 'n':
                error_state = lib.turn_off_LED_terminal()
            elif what_to_do_flag == 'l':
                lib.displayLeaderboard_terminal()
            else:
                print ('Not allowed input!')
                error_state = 2

    elif sys.argv[1] == '-g' : #GUI mode
        os.system("python3 guiv2.py")
        sys.exit([0])
    else:
        print('Invalid parameter')
        sys.exit([2])
else:
    print('Invalid number of arguments')
    sys.exit([2])
