from tkinter import *
import serial
from time import sleep

root = Tk()
root.geometry("900x700")
defaultbg = root.cget('bg')
frame = Frame(root, width=900, height=700)
keyHold = False

ser = serial.Serial('COM8', 9600)

def keydown(e):
    global keyHold, AIStarted
    if not keyHold:
        if(e.char == 'w'): 
            ser.write(b'F  ')
        if(e.char == 'd'): 
            ser.write(b'R  ')
        if(e.char == 'a'): 
            ser.write(b'L  ')
        if(e.char == 's'): 
            ser.write(b'B  ')
        keyHold = True
def keyup(e):
    global keyHold
    if(e.char == 'w'): 
        ser.write(b'S  ')
    if(e.char == 's'): 
        ser.write(b'S  ')
    if(e.char == 'a'): 
        ser.write(b'C  ')
    if(e.char == 'd'): 
        ser.write(b'C  ')
    
    keyHold = False

frame.bind("<KeyPress>", keydown)
frame.bind("<KeyRelease>", keyup)

frame.pack()
frame.focus_set()
root.mainloop()