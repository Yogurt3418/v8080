import v8080
import tkinter as tk
from PIL import Image, ImageTk
import time
mainWindow=tk.Tk()

def ShowImage(cpu):
	screen = Image.new("RGB", (224, 256), "#000000")
	screen_pixels = screen.load()

	for i in range(0, 1000):
		#print('ShowImage i : ' + str(i))
		screen_pixels[i/224, i%224] = cpu.RAM[0x2400+i]

	print('Drawing Image')
	screen.show()
	return;
	

def RunIndef8080(cpu):
	while 1:
		Step8080(cpu)

def Run8080(cpu, a):

	s = int(a.get())
	t = s
	
	for i in range(0, s):
		Step8080(cpu)
		t = t - 1
		a.delete(0, tk.END)
		a.insert(0, str(t))

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
	flagS.set('Sign : ' + str(bool(cpu.statS)))
	flagZ.set('Zero : ' + str(bool(cpu.statZ)))
	flagAC.set('AC : ' + str(bool(cpu.statAC)))
	flagP.set('Prty : ' + str(bool(cpu.statP)))
	flagC.set('Crry : ' + str(bool(cpu.statC)))
	
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

ScreenFrame = tk.Frame(mainWindow)
ScreenFrame.pack(side=tk.BOTTOM)

#Create the display
#screen = Image.new("RGB", (224, 256), "#FFFFFF")
#screen_pixels = screen.load()
#screen.show()

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

flagS = tk.StringVar()
flagZ = tk.StringVar()
flagAC = tk.StringVar()
flagP = tk.StringVar()
flagC = tk.StringVar()


regALabel=tk.Label(RegFrame,textvariable=regA)
regBLabel=tk.Label(RegFrame,textvariable=regB)
regCLabel=tk.Label(RegFrame,textvariable=regC)
regPCLabel=tk.Label(RegFrame,textvariable=regPC)
regSPLabel=tk.Label(RegFrame,textvariable=regSP)
regDLabel=tk.Label(RegFrame,textvariable=regD)
regELabel=tk.Label(RegFrame,textvariable=regE)
regHLabel=tk.Label(RegFrame,textvariable=regH)
regLLabel=tk.Label(RegFrame,textvariable=regL)

flagSLabel = tk.Label(RegFrame,textvariable=flagS)
flagZLabel = tk.Label(RegFrame,textvariable=flagZ)
flagACLabel = tk.Label(RegFrame,textvariable=flagAC)
flagPLabel = tk.Label(RegFrame,textvariable=flagP)
flagCLabel = tk.Label(RegFrame,textvariable=flagC)

regALabel.pack()
regBLabel.pack()
regCLabel.pack()
regDLabel.pack()
regELabel.pack()
regHLabel.pack()
regLLabel.pack()
regPCLabel.pack()
regSPLabel.pack()

flagSLabel.pack()
flagZLabel.pack()
flagACLabel.pack()
flagPLabel.pack()
flagCLabel.pack()

#Create user entry box
StepEntry = tk.Entry(ButtonFrame, width=8)
StepEntry.pack()

#Create Buttons
step_button=tk.Button(ButtonFrame,text="Step",command=lambda : Step8080(cpu)).pack()
run_button=tk.Button(ButtonFrame,text="Run n",command=lambda : Run8080(cpu, StepEntry)).pack()
run_indef_button=tk.Button(ButtonFrame,text="Run!",command=lambda : RunIndef8080(cpu)).pack()
show_image=tk.Button(ButtonFrame,text="Show Image",command=lambda : ShowImage(cpu)).pack()

#Static text box
pcPlus = ''
UpcommingInst=tk.Text(ButtonFrame, height=10, width=5)
UpcommingInst.pack()
UpcommingInst.insert(tk.END, pcPlus)

tk.mainloop()
