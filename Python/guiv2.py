#!/usr/bin/python3

import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
## import our .py files
import lib as lib
from lib import *
import constants
from operator import itemgetter
#### GUI STRUCTURE ####

###########################
# LEDON ## VOID ## LEDOFF #
# TEXT  ## TIME ## ERROR  #
# VOID  ## QUIT ## VOID   #
###########################

####       END     ####

#### functions declaration

#def set_score(score):
#    scoreWindow=Toplevel()
#    for row in range(1,3):
#        for col in range(1,3):
#            mainFrame.columnconfigure(col, weight=1)
#        mainFrame.rowconfigure(row, weight=1)
#    l=tk.Label(scoreWindow, textvariable="Do you want to save result?",  font="Helvetica 25 bold", bg='white', fg='red', justify='center')

def uploadMem(name,score,window):
    strings=[]
    with open(constants.mem_file,"r") as mem_pointer:
        for line in mem_pointer:
            temp=line.split()
            strings+=[(temp[0],temp[1])]
    strings+=[(name,str(score))]
    #for i in range(len(strings)):
    #    print("{} {}".format(strings[i][0],strings[i][1]))
    strings.sort(key=itemgetter(1))

    with open(constants.mem_file,"w") as mem_pointer:
        if len(strings)>constants.maxLeaders:
            max=constants.maxLeaders
        else:
            max=len(strings)
        for i in range(0,max):
            mem_pointer.write(strings[i][0]+" "+strings[i][1]+'\n')
    quit_window(window)

def saveResult(result):
    saveWindow=Toplevel()
    for row in range(1,3):
            for col in range(1,3):
                saveWindow.columnconfigure(col, weight=1)
            saveWindow.rowconfigure(row, weight=1)
    name=tk.Label(saveWindow,textvariable="Name:",bg='white',fg='black')
    name.grid(row=1,column=1,sticky=(W))
    nick=tk.Entry(saveWindow,bg='white',fg='black')
    nick.grid(row=1,column=2,sticky=(E))
    yesButton=tk.Button(saveWindow,text="Yes", command=lambda: uploadMem(nick.get(),result,saveWindow), bg='red3', highlightbackground="firebrick4", font="Helvetica 20 bold ", activebackground="SkyBlue1", highlightthickness=4, pady=5, width=5, height=1)
    yesButton.grid(row=2,column=1,sticky=(N, S, W, E))
    noButton=tk.Button(saveWindow,text="No", command=lambda:quit_window(saveWindow), bg='red3', highlightbackground="firebrick4", font="Helvetica 20 bold ", activebackground="SkyBlue1", highlightthickness=4, pady=5, width=5, height=1)
    noButton.grid(row=2,column=2,sticky=(N, S, W, E))

## turn on/off function check the value of t_score in lib.py
## if it is E0001 or E0000 the lead is already ON/OFF
## in those scenarios there is no change in t_score value
## an error sentence is displayed on the GUI
def turn_on_LED():
    error_flag.set("")
    tmp =""
    tmp=lib.send_ser_cmd(constants.commands_to_send[1])
    if(tmp=="E0001"):
        error_flag.set("LED ALREADY\nON")
    else:
        t_score.set(tmp)
        set_score(tmp)

def turn_off_LED():
    error_flag.set("")
    tmp =""
    tmp=lib.send_ser_cmd(constants.commands_to_send[0])
    if(tmp=="E0000"):
        error_flag.set("LED ALREADY\nOFF")
    else:
        t_score.set(tmp)
        set_score(tmp)

def quit_window(window):
    window.destroy()

def displayLeaderboard():
    leaderboard=Toplevel()
    leaderboard.title("Leaderboard")
    for row in range(1,constants.maxLeaders+2):
        for col in range(1,4):
            leaderboard.columnconfigure(col, weight=1)
        leaderboard.rowconfigure(row, weight=1)
    with open(constants.mem_file,"r") as mem_pointer:
        i=0
        for line in mem_pointer:
            strings=line.split()
            lnum=tk.Label(leaderboard,
                        text=i,
                        fg='black',
                        bg='white',
                        font='Helvetica 25 bold',
                        justify='center')
            lname=tk.Label(leaderboard,
                        text=strings[0],
                        fg='black',
                        bg='white',
                        font='Helvetica 25 bold',
                        justify='center')
            lscore=tk.Label(leaderboard,
                        text=strings[1],
                        fg='black',
                        bg='white',
                        font='Helvetica 25 bold',
                        justify='center')
            lnum.grid(row=i, column=1, sticky=(N, S, W, E))
            lname.grid(row=i, column=2, sticky=(N, S, W, E))
            lscore.grid(row=i, column=3, sticky=(N, S, W, E))
            i+=1
    quit_button=tk.Button(leaderboard,
                        text="QUIT",
                        command=lambda: quit_window(leaderboard),
                        bg='red3',
                        highlightbackground="firebrick4",
                        font="Helvetica 20 bold ",
                        activebackground="SkyBlue1",
                        highlightthickness=4,
                        pady=5,
                        width=3,
                        height=1)
    quit_button.grid(row=i, columnspan=3, sticky= (N, S, W, E))
####

root= Tk()

error_flag= StringVar()
error_flag.set("")
t_score= StringVar()
t_score.set("")

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
text_score_lab=tk.Label(mainFrame, text="Your time score is: ", font="Helvetica 15", bg='white',fg='black', height=4)
t_score_lab=tk.Label(mainFrame, textvariable=t_score, font="Helvetica 35 bold", bg='white', fg='black', width=8)

## label to show a possible error due to LED already ON or already OFF
error_lab=tk.Label(mainFrame, textvariable=error_flag,  font="Helvetica 25 bold", bg='white', fg='red', justify='center')

## save result
save=tk.Button(mainFrame, text="Save", command=lambda: saveResult(t_score), bg='red3', highlightbackground="firebrick4", font="Helvetica 20 bold ", activebackground="SkyBlue1", highlightthickness=4, pady=5, width=12, height=1)

## display leaderboard
leaderboard=tk.Button(mainFrame, text="Leaderboard", command=displayLeaderboard, bg='red3', highlightbackground="firebrick4", font="Helvetica 20 bold ", activebackground="SkyBlue1", highlightthickness=4, pady=5, width=12, height=1)

## button to quit program
quit_button=tk.Button(mainFrame, text="QUIT", command=lambda:quit_window(root), bg='red3', highlightbackground="firebrick4", font="Helvetica 20 bold ", activebackground="SkyBlue1", highlightthickness=4, pady=5, width=3, height=1)

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

save.grid(row=2, column=3, sticky=(N, S, E, W))
leaderboard.grid(row=3, column=1, sticky=N)
quit_button.grid(row=3, column=2, sticky= S)

#### end widgets configuration

root.mainloop()
