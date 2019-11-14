import v8080
from tkinter import *
import time
mainWindow=Tk()

def Step8080(cpu):
    
    while 1:
        cpu.decode()
        regA.set('A  : ' + str(hex(cpu.regA)))
        regB.set('B  : ' + str(hex(cpu.regB)))
        regC.set('C  : ' + str(hex(cpu.regC)))
        regPC.set('PC : ' + str(hex(cpu.regPC)))
        regSP.set('SP : ' + str(hex((cpu.regSPH<<8)|(cpu.regSPL))))
        mainWindow.update()
        #time.sleep()

cpu = v8080.v8080()
f = open("invaders2.asm", "rb")
cpu.RAM = bytearray(f.read())

regA=StringVar()
regB=StringVar()
regC=StringVar()
regPC=StringVar()
regSP=StringVar()

regALabel=Label(mainWindow,textvariable=regA)
regBLabel=Label(mainWindow,textvariable=regB)
regCLabel=Label(mainWindow,textvariable=regC)
regPCLabel=Label(mainWindow,textvariable=regPC)
regSPLabel=Label(mainWindow,textvariable=regSP)

regALabel.pack()
regBLabel.pack()
regCLabel.pack()
regPCLabel.pack()
regSPLabel.pack()

start_button=Button(mainWindow,text="RUN",command=Step8080(cpu))

start_button.pack()

mainWindow.mainloop()
