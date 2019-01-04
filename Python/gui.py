import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk

#### GUI STRUCTURE ####

###########################
# LEDON ## VOID ## LEDOFF #
# TEXT  ## TIME ## VOID   #
# VOID  ## QUIT ## VOID   #
###########################

####       END     ####

#### Variables definition

####

#### functions declaration
#def change_pic():
#    if(t_score=="L1"):
#        img= ImageTk.PhotoImage(file='/home/luca/Downloads/GUI/lumaca.jpg')
#    elif(t_score=="L0"):
#        img= ImageTk.PhotoImage(file='/home/luca/Downloads/GUI/ghepardo.jpg')
#    else:
#        img= ImageTk.PhotoImage(file='white.png')
def turn_on_led():
    t_score.set("L1")
    change_pic()
    return lambda: print("L1")

def turn_off_led():
    t_score.set("L0")
    change_pic()
    return lambda: print("L0")

def quit_prog():
    root.quit()
    return exit()
####

root= Tk()

t_score= StringVar()
t_score.set("65")

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
led_off=tk.Button(mainFrame, text="LED \n\nOFF", command= turn_off_led, bg= "gray64", relief="solid", highlightbackground="gray20", font="Helvetica 20 bold ", activebackground="SkyBlue1", highlightthickness=4, width=8, height= 3, pady=10)
led_on=tk.Button(mainFrame, text="LED \n\nON", command= turn_on_led, bg="green2", relief="solid", highlightbackground="dark green", font="Helvetica 20 bold ", activebackground="SkyBlue1", highlightthickness=4, width=8, height= 3, pady=10)

## labels to show the time score
text_score_lab=tk.Label(mainFrame, text="Your time score is: ", font="Helvetica 15", bg='white')
t_score_lab=tk.Label(mainFrame, textvariable=t_score, font="Helvetica 35 bold", bg='white')

## button to quit program
quit_button=tk.Button(mainFrame, text="QUIT", command=quit_prog, bg='red3', highlightbackground="firebrick4", font="Helvetica 20 bold ", activebackground="SkyBlue1", highlightthickness=4, pady=5, width=3, height=1)

#img= ImageTk.PhotoImage(file='white.png')
#pic=tk.Label(frame, image=img,  pady=50, borderwidth=5, bg='white', textvariable=t_score)

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

led_on.grid(row=1, column=1, sticky=(N, S, W, E))
led_on.grid_rowconfigure(1,weight=1)
led_on.grid_columnconfigure(1,weight=2)
led_off.grid(row=1, column=3, sticky=(N, S, E, W))
led_off.grid_rowconfigure(1,weight=1)
led_off.grid_columnconfigure(3,weight=2)

quit_button.grid(row=3, column=2, sticky= S)

#pic.grid(row=2, column=3, sticky=(N, S, E, W))
#pic.grid_rowconfigure(2, weight=1)
#pic.grid_columnconfigure(3, weight=1)

#### end widgets configuration

root.mainloop()
