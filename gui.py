import v8080
#from tkinter import *
import tkinter as tk
import time
mainWindow=tk.Tk()

def Run8080(cpu, a):
	for i in range(0, a):
		Step8080(cpu)

def Step8080(cpu):
	
	cpu.decode()
	regA.set('A  : ' + str(hex(cpu.regA)))
	regB.set('B  : ' + str(hex(cpu.regB)))
	regC.set('C  : ' + str(hex(cpu.regC)))
	regD.set('D  : ' + str(hex(cpu.regD)))
	regE.set('E  : ' + str(hex(cpu.regE)))
	regH.set('H  : ' + str(hex(cpu.regH)))
	regL.set('L  : ' + str(hex(cpu.regL)))
	regPC.set('PC : ' + str(hex(cpu.regPC)))
	regSP.set('SP : ' + str(hex((cpu.regSPH<<8)|(cpu.regSPL))))
	pcPlus = ''
	UpcommingInst.delete('1.0', tk.END)
	
	for i in range(0, 10):
			pcPlus = pcPlus + str(hex(cpu.RAM[cpu.regPC + i])) + '\n'

	UpcommingInst.insert(tk.END, pcPlus)
	mainWindow.update()
	return
	#time.sleep()

#Create the CPU
cpu = v8080.v8080()
f = open("invaders2.asm", "rb")
cpu.RAM = bytearray(f.read())

#Create the frames
RegFrame = tk.Frame(mainWindow)
RegFrame.pack(side=tk.LEFT)

ButtonFrame = tk.Frame(mainWindow)
ButtonFrame.pack(side=tk.RIGHT)

#Create variables and their labels
regA=tk.StringVar()
regB=tk.StringVar()
regC=tk.StringVar()
regPC=tk.StringVar()
regSP=tk.StringVar()
regD=tk.StringVar()
regE=tk.StringVar()
regH=tk.StringVar()
regL=tk.StringVar()

regALabel=tk.Label(RegFrame,textvariable=regA)
regBLabel=tk.Label(RegFrame,textvariable=regB)
regCLabel=tk.Label(RegFrame,textvariable=regC)
regPCLabel=tk.Label(RegFrame,textvariable=regPC)
regSPLabel=tk.Label(RegFrame,textvariable=regSP)
regDLabel=tk.Label(RegFrame,textvariable=regD)
regELabel=tk.Label(RegFrame,textvariable=regE)
regHLabel=tk.Label(RegFrame,textvariable=regH)
regLLabel=tk.Label(RegFrame,textvariable=regL)

regALabel.pack()
regBLabel.pack()
regCLabel.pack()
regDLabel.pack()
regELabel.pack()
regHLabel.pack()
regLLabel.pack()
regPCLabel.pack()
regSPLabel.pack()

#Create user entry box
StepEntry = tk.Entry(ButtonFrame, width=8)
StepEntry.pack()

#Create Buttons
step_button=tk.Button(ButtonFrame,text="Step",command=lambda : Step8080(cpu)).pack()
run_button=tk.Button(ButtonFrame,text="Run",command=lambda : Run8080(cpu, int(StepEntry.get()))).pack()

#Static text box
pcPlus = ''
UpcommingInst=tk.Text(ButtonFrame, height=10, width=5)
UpcommingInst.pack()
UpcommingInst.insert(tk.END, pcPlus)

tk.mainloop()
