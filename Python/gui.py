import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
## import our .py files
import lib as lib
from lib import *
import constants

#### GUI STRUCTURE ####

###########################
# LEDON ## VOID ## LEDOFF #
# TEXT  ## TIME ## ERROR  #
# VOID  ## QUIT ## VOID   #
###########################

####       END     ####

#### functions declaration

## turn on/off function check the value of t_score in lib.py
## if it is E0001 or E0000 the lead is already ON/OFF
## in those scenarios there is no change in t_score value
## an error sentence is displayed on the GUI
def turn_on_LED():
    tmp =""
    tmp=lib.send_ser_cmd(constants.commands_to_send[1])
    print("L1")
    if(tmp=="E0001"):
        error_flag.set("LED ALREADY\nON")
    elif(tmp==""):
        t_score.set(tmp)        
        error_flag.set("")
        
def turn_off_LED():
    tmp =""
    tmp=lib.send_ser_cmd(constants.commands_to_send[0])
    print("L0")
    if(tmp=="E0000"):
        error_flag.set("LED ALREADY\nOFF")
    elif(tmp==""):
        t_score.set(tmp)        
        error_flag.set("")
        
def quit_prog():
    root.quit()
####

root= Tk()

error_flag= StringVar()
error_flag.set("")
t_score= StringVar()
t_score.set("65 ms")

#### Frame and root
root.title("Reflexes Measurer")

mainFrame= Frame(root, bg='white')

## managing the main frame with pack
mainFrame.pack(fill=BOTH, expand=1)

## setting the frame weight for cols and rows
## in order to resize it with the main window
for row in range(1,4):
    for col in range(1,4):
        mainFrame.columnconfigure(col, weight=1)
    mainFrame.rowconfigure(row, weight=1)

#### widgets declaration

## buttons to be pressed to turn ON/OFF the LED
led_off=tk.Button(mainFrame, text="LED \n\nOFF", command= turn_off_LED, bg= "gray64", relief="solid", highlightbackground="gray20", font="Helvetica 20 bold ", activebackground="SkyBlue1", highlightthickness=4, width=14, height= 5, pady=10)
led_on=tk.Button(mainFrame, text="LED \n\nON", command= turn_on_LED, bg="green2", relief="solid", highlightbackground="dark green", font="Helvetica 20 bold ", activebackground="SkyBlue1", highlightthickness=4, width=14, height= 5, pady=10)

## labels to show the time score
text_score_lab=tk.Label(mainFrame, text="Your time score is: ", font="Helvetica 15", bg='white', height=4)
t_score_lab=tk.Label(mainFrame, textvariable=t_score, font="Helvetica 35 bold", bg='white')

## label to show a possible error due to LED already ON or already OFF
error_lab=tk.Label(mainFrame, textvariable=error_flag,  font="Helvetica 25 bold", bg='white', fg='red', justify='center')

## button to quit program
quit_button=tk.Button(mainFrame, text="QUIT", command=quit_prog, bg='red3', highlightbackground="firebrick4", font="Helvetica 20 bold ", activebackground="SkyBlue1", highlightthickness=4, pady=5, width=3, height=1)

#### end widgets declaration


#### widgets configuration
## each widget is managed with the grid geometry manager
## in order to have a matrix-like organization

text_score_lab.grid(row=2, column=1, sticky=(E))
text_score_lab.grid_rowconfigure(2, weight=1)
text_score_lab.grid_columnconfigure(1, weight=1)

t_score_lab.grid(row=2, column=2, sticky=(W))
t_score_lab.grid_rowconfigure(2, weight=1)
t_score_lab.grid_columnconfigure(2, weight=1)

error_lab.grid(row=2, column=3, sticky=(N, E, S, W))
error_lab.grid_rowconfigure(2, weight=1)
error_lab.grid_columnconfigure(3, weight=1)

led_on.grid(row=1, column=1, sticky=(N, S, W, E))
led_on.grid_rowconfigure(1,weight=1)
led_on.grid_columnconfigure(1,weight=2)
led_off.grid(row=1, column=3, sticky=(N, S, E, W))
led_off.grid_rowconfigure(1,weight=1)
led_off.grid_columnconfigure(3,weight=2)

quit_button.grid(row=3, column=2, sticky= S)

#### end widgets configuration

root.mainloop()
