import constants
import serial
import serial.tools.list_ports as port_list #serial.tools.list_ports is renamed as port_list
from random import randint
from time import sleep
from operator import itemgetter

t_score = "" #a global variable that saves the time interval value or a kind of error
LED_state = 0 # a global variable that saves the LED state: if it is 0, the LED is off, otherwise the LED is on.

def getInput(string):
    return input(string)

# delay_cmd INTERFACE
# the function delay_cmd() inserts a random delay from 10 to 20 seconds
# It has no input or output parameters
# It requires the functions randint from random Python package and sleep from time Python package

def delay_cmd():
    #generating a random integer between 10 and 20
    seconds_to_wait = randint(10, 20)
    #waiting a random number of seconds
    sleep(seconds_to_wait)

# send_ser_cmd() INTERFACE

# It receives a string as an input parameter, that is the command to send to a serial port.
# It returns a global variable, t_score, that is a string containing a time interval value and its
# measure unit (ms) or an error string.
# First of all, the function send_ser_cmd() opens a serial port and sets the communication parameters.
# If command_to_send is equal to "L 1" ("L 0"), but the global variable LED_state is equal to 1 (0),
# the user wants to turn on (turn off) the LED, but the LED is already turned on (turned off): the function
# updates t_score and return an error string equal to E0001 (E0000) is returned. If command_to_send is equal to "L 1"
# and LED_state is equal to 0, the function sends to the serial port "L 1" and updates LED_state to 1. If
# command_to_send is equal to "L 0" and LED_state is equal to 1, the function updates LED_state to 0,
# sends to the serial port "L 0" and then waits until 5 bytes from the port are
# received. The 5 bytes contains a time interval value and the function returns the string containing the
# time interval value and its measure unit.
# To convert into a string the byte object received by the serial port, the function makes use of
# t_score_byte_object_conversion_to_seconds, a function defined in the same module of the first.

def send_ser_cmd(command_to_send):

    global t_score
    global LED_state

    #if constants.debug_constant == 1:
        ##to print all the available serial ports use the following instructions
        #print ("The PC has the following available serial ports:\n")
        #ports = list(port_list.comports())
        #for p in ports:
        #    print (p)

    #setting the serial port
    ser = serial.Serial()
    ser.port = constants.serial_port_name #setting the name of the serial port
    ser.baudrate = 115200 #setting the baudrate
    ser.parity = serial.PARITY_NONE #setting the parity
    ser.bytesize = serial.EIGHTBITS #setting the bytesize
    ser.timeout = 100 #setting a timeout for ser.read (if ser.read takes more than 10 seconds, the program automatically moves forward).
    #No specifics about ser.stopbits: by default, ser.stopbits is equal to STOPBITS_ONE (ser.stopbits = serial.STOPBITS_TWO)

    ser.open() #opening the port

    if command_to_send == constants.commands_to_send[1] and LED_state == 0:
        if ser.isOpen():
            #turning on the LED
            LED_state = 1 #updating the LED state
            delay_cmd() #waiting random seconds
            ser.write(command_to_send.encode('ASCII')) #send the command to the serial port
            t_score_byte_object = ser.read(5) #read 5 bytes from the serial port .read returns a byte object
            t_score = t_score_byte_object_conversion_to_seconds (t_score_byte_object) #updating the t_score
    elif command_to_send == constants.commands_to_send[0] and LED_state == 1:
        #sending the command
        if ser.isOpen():
            #turning off the LED
            LED_state = 0 #updating the LED state
            delay_cmd() #waiting random seconds
            ser.write(command_to_send.encode('ASCII')) #send the command to the serial port
            t_score_byte_object = ser.read(5) #read 5 bytes from the serial port .read returns a byte object
            t_score = t_score_byte_object_conversion_to_seconds (t_score_byte_object) #updating the t_score
    elif command_to_send == constants.commands_to_send[1] and LED_state == 1:
        # the LED is already ON
        t_score = "E0001"
    else:
        # the LED is already OFF
        t_score = "E0000"

    return t_score

def uploadMem(name,score,window,mode):
    if name != "":
        strings=[]
        flag_setted=False
        with open(constants.mem_file,"r") as mem_pointer:
            for line in mem_pointer:
                temp=line.split()
                if temp[0]==name:
                    if int(score)<int(temp[1]):
                        strings+=[(temp[0],score)]
                    else:
                        strings+=[(temp[0],temp[1])]
                    flag_setted=True
                else:
                    strings+=[(temp[0],temp[1])]
        if flag_setted==False:
            strings+=[(name,score)]
        strings.sort(key=(itemgetter(1)))
        strings.sort(key=len)
        with open(constants.mem_file,"w") as mem_pointer:
            if len(strings)>constants.maxLeaders:
                max=constants.maxLeaders
            else:
                max=len(strings)
            for i in range(0,max):
                mem_pointer.write(strings[i][0]+" "+strings[i][1]+'\n')
    if mode==constants.gui_mod:
        quit_window(window)

# t_score_string_conversion_to_seconds() INTERFACE
# The function t_score_byte_object_conversion_to seconds converts a byte object into a string object
# It receives one input parameter. a byte object, and returns a string
# The byte object input parameter should contain the value of a time interval expressed as b'Thhhh', or, in other words,
# it is a byte object of 5 bytes, where hhhh is the hexadecimal value of the time interval, and T is a character
# The string contains the time interval value converted into seconds, a white space and the character 's' (its measure unit)

def t_score_byte_object_conversion_to_seconds (t_score_byte_object):
    t_score_string = t_score_byte_object.decode('ASCII') #converting the byte object into a string object
    t_score = int(t_score_string[1:], 16) #converting the string t_score into seconds
    t_score_to_print = str(t_score) + ' ms' #adding the measure unit to t_score
    return t_score_to_print

# turn_on_LED() INTERFACE
# The function turn_on_LED() is called when the user from terminal wants to turn on the LED.
# It returns an integer: 0 if the LED is turning on, 3 if the LED is already turned on.
# It makes use of the function send_ser_cmd.

def turn_on_LED_terminal():
    send_ser_cmd(constants.commands_to_send[1])
    if t_score == "E0001":
        print ('The LED is already turned on!')
        return 3
    else:
        print ('Your time score is:', t_score)
        c = getInput("Do you want to save you score? N/y\n")
        if c=="y":
            name = getInput("Please insert your name:\n")
            uploadMem(name,t_score[0:-3],None,None)
        else:
            return 0

# turn_on_LED() INTERFACE
# The function turn_on_LED() is called by the button LED ON. It sends to the serial port the command to turn off the LED (L 1).
# It returns an integer: 0 if the LED is turning off, 3 if the LED is already turned off.
# It makes use of the function send_ser_cmd.

def turn_off_LED_terminal():
    send_ser_cmd(constants.commands_to_send[0])
    if t_score == "E0000":
        print ('The LED is already turned off!')
        return 3
    else:
        print ('Your time score is: ', t_score)
        c = getInput("Do you want to save you score? N/y\n")
        if c=="y":
            name = getInput("Please insert your name:\n")
            uploadMem(name,t_score[0:-3],None,None)
        return 0

def displayLeaderboard_terminal():
    with open(constants.mem_file,"r") as mem_pointer:
        i=0
        for line in mem_pointer:
            strings=line.split()
            spaces0=" "*(2-len(str(i)))
            spaces1=" "*(15-len(strings[0]))
            spaces2=" "*(5-len(strings[1]))
            print("{}{} {}{} {}{}ms".format(spaces0,i+1,strings[0],spaces1,spaces2,strings[1]))
            i+=1

def quit_window(window):
    window.destroy()

def displayMenu():
    print("Digit one of the following options:")
    for i in range(len(constants.men_options)):
        print(constants.men_options[i])
