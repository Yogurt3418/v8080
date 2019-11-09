class v8080:
	def __init__(self):
		self.address = 0
		self.data = 0
		self.reset = 0
		self.hold = 0
		self.wait = 0
		self.int = 0
		self.inte = 0
		self.hlda = 0
		self.wr = 0
		self.clock_1 = 0
		self.clock_2 = 0
		self.dbin = 0
		self.sync = 0
		
		self.regA = 0
		self.regB = 0
		self.regC = 0
		self.regD = 0
		self.regH = 0
		self.regL = 0
		self.regSPL = 0
		self.regSPH = 0
		self.regPC = 0
		
		self.statS = False
		self.statZ = False
		self.statAC = False
		self.statP = False
		self.statC = False

		#4K Ram, basing this off the space invaders cabinet
		self.RAM = [None] * 0x3FFF
		#8K Rom
		#self.ROM = [None] * 8 * 1024
		
	

	def inx(self, a, b):
		
		c = (a<<8) | b
		c+=1
		a = c & 0xFF00
		b = c & 0xFF
		
		return a, b

	def inr(self, a):
		
		a = a + 1
		if(a > 0xFF):
			a = 0
			self.statAC = True
		if(a == 0):
			self.statZ = True
		if(a & 0x80):
			self.statS = True
		if(findParity(a)):
			self.statP = True
		return a

	def dcr(self, a):
		
		a = a - 1
		if(a < 0):
			a = 255
			self.statAC = True
		if(a == 0):
			self.statZ = True
		if(a & 0x80):
			self.statS = True
		if(findParity(a)):
			self.statP = True
		return a

	def rlc(self, a):
		return (a << 1)|(a >> (7))

	def rrc(self, a):
		return (a >> 1)|(a << (7))

	def dad(self, a, b):
		x = (self.regH<<8) | self.regL
		y = (a<<8) | b
		x+=y
		if(x>(1<<16)):
			self.statC = True
			
		return (x&0xFF00), (x&0xFF)

	def dcx(self, a, b):
		c = (a<<8) | b
		c-=1
		a = c & 0xFF00
		b = c & 0xFF
		
		return a, b

	def decode(self):

		byteLen = 1
		cycles = 1

		#this may need to be changed later
		d = self.RAM[self.regPC]

		########
		# 0x0X #
		########
		if((d & ~0x0F) == 0):
			if d == 0x00:
				cycles = 7
				decPnt(self, '0x00 : NOP')
				
			if d == 0x01:
				byteLen = 3
				cycles = 10
				self.regC = self.RAM[self.regPC+1]
				self.regB = self.RAM[self.regPC+2]
				decPnt(self, '0x01 : LXI B, d16')
				
			if d == 0x02:
				cycles = 7
				self.RAM[(self.regB<<8)|self.regC] = self.regA
				decPnt(self, '0x02 : STAX B')
				
			if d == 0x03:
				cycles = 5
				self.regB, self.regC = self.inx(self.regB, self.regC)
				decPnt(self, '0x03 : INX B')
				
			if d == 0x04:
				cycles = 5
				self.regB = self.inr(self.regB)
				decPnt(self, '0x04 : INR')
			
			if d == 0x05:
				cycles = 5
				self.regB = self.dcr(self.regB)
				decPnt(self, '0x05 : DCR B')
				
			if d == 0x06:
				byteLen = 2
				cycles = 7
				self.regB = self.RAM[self.regPC+1]
				decPnt(self, '0x06 : MVI B, d8')
				
			if d == 0x07:
				byteLen = 1
				cycles = 4
				self.regA = self.rlc(self.regA)
				decPnt(self, '0x07 : RLC')
				
			if d == 0x08:
				byteLen = 1
				cycles = 4
				decPnt(self, '0x08 : NOP')
				
			if d == 0x09:
				byteLen = 1
				cycles = 10
				self.regH, self.regL = self.dad(self.regB, self.regC)
				decPnt(self, '0x09 : DAD B')
				
			if d == 0x0A:
				byteLen = 1
				cycles = 7
				self.regA = self.RAM[(self.regB<<8)|self.regC]
				decPnt(self, '0x0A : LDAX B')
				
			if d == 0x0B:
				cycles = 5
				self.regB, self.regC = self.dcx(self.regB, self.regC)
				decPnt(self, '0x0B : DCX B')
				
			if d == 0x0C:
				cycles = 5
				self.regC = self.inr(self.regC)
				decPnt(self, '0x0C : INR C')
				
			if d == 0x0D:
				cycles = 5
				self.regC = self.dcr(self.regC)
				decPnt(self, '0x0D : DCR C')
				
			if d == 0x0E:
				byteLen = 2
				cycles = 7
				self.regC = self.RAM[self.regPC+1]
				decPnt(self, '0x0E : MVI C, d8')
				
			if d == 0x0F:
				cycles = 4
				self.regA = self.rrc(self.regA)
				decPnt(self, '0x0F : RRC')
				

		########
		# 0x1X #
		########
		if((d & ~0x1F) == 0):
			if d == 0x10:
				cycles = 4
				decPnt(self, '0x10 : NOP')
				
			if d == 0x11:
				byteLen = 3
				cycles = 10
				self.regE = self.RAM[self.regPC+1]
				self.regD = self.RAM[self.regPC+2]
				decPnt(self, '0x11 : LXI D, d16')
				
			if d == 0x12:
				cycles = 7
				self.RAM[(self.regD<<8)|(self.regE)] = self.regA
				decPnt(self, '0x12 : STAX D')
				
			if d == 0x13:
				cycles = 5
				self.regD, self.regE = self.inx(self.regD, self.regE)
				decPnt(self, '0x13 : INX D')
				
			if d == 0x14:
				cycles = 5
				self.regD = self.inr(self.regD)
				decPnt(self, '0x14 : INR D')
				
			if d == 0x15:
				cycles = 5
				self.regD = self.dcr(self.regD)
				decPnt(self, '0x15 : DCR D')
				
			if d == 0x16:
				byteLen = 2
				cycles = 7
				self.regD = self.RAM[self.regPC+1]
				decPnt(self, '0x16 : MVI D, d8')
				
			if d == 0x17:
				cycles = 4
				##TODO
				decPnt(self, '0x17 : RAL')
				
			if d == 0x18:
				cycles = 4
				decPnt(self, '0x18 : NOP')
				
			if d == 0x19:
				byteLen = 1
				cycles = 10
				self.regH, self.regL = self.dad(self.regD, self.regE)
				decPnt(self, '0x19 : DAD D')
				
			if d == 0x1A:
				byteLen = 1
				cycles = 7
				self.regA = self.RAM[(self.regD<<8)|self.regE]
				decPnt(self, '0x1A : LDAX D')
				
			if d == 0x1B:
				cycles = 5
				self.regD, self.regE = self.dcx(self.regD, self.regE)
				decPnt(self, '0x1B : DCX D')
				
			if d == 0x1C:
				cycles = 5
				self.regE = self.inr(self.regE)
				decPnt(self, '0x1C : INR E')
				
			if d == 0x1D:
				cycles = 5
				self.regE = self.dcr(self.regE)
				decPnt(self, '0x1D : DCR E')
				
			if d == 0x1E:
				byteLen = 2
				cycles = 7
				self.regE = self.RAM[self.regPC+1]
				decPnt(self, '0x1E : MVI E, d8')
				
			if d == 0x1F:
				cycles = 4
				self.regA = self.rar(self.regA)
				decPnt(self, '0x1F : RAR')
				

		########
		# 0x2X #
		########
		if((d & ~0x2F) == 0):
			if d == 0x20:
				cycles = 4
				decPnt(self, '0x20 : NOP')
				
			if d == 0x21:
				byteLen = 3
				cycles = 10
				self.regL = self.RAM[self.regPC+1]
				self.regH = self.RAM[self.regPC+2]
				decPnt(self, '0x21 : LXI H, d16')
				
			if d == 0x22:
				byteLen = 3
				cycles = 16
				self.RAM[self.RAM[self.regPC+1]] = self.regL
				self.RAM[self.RAM[self.regPC+2]] = self.regH
				decPnt(self, '0x22 : SHLD a16')
				
			if d == 0x23:
				cycles = 5
				self.regH, self.regL = self.inx(self.regH, self.regL)
				decPnt(self, '0x23 : INX H')
				
			if d == 0x24:
				cycles = 5
				self.regH = self.inr(self.regH)
				decPnt(self, '0x24 : INR H')
				
			if d == 0x25:
				cycles = 5
				self.regH = self.dcr(self.regH)
				decPnt(self, '0x25 : DCR H')
				
			if d == 0x26:
				byteLen = 2
				cycles = 7
				self.regH = self.RAM[self.regPC+1]
				decPnt(self, '0x26 : MVI H, d8')
				
			if d == 0x27:
				cycles = 4
				##TODO? 
				decPnt(self, '0x27 : DAA')
				
			if d == 0x28:
				cycles = 4
				decPnt(self, '0x28 : NOP')
				
			if d == 0x29:
				byteLen = 1
				cycles = 10
				self.regH, self.regL = self.dad(self.regH, self.regL)
				decPnt(self, '0x29 : DAD H')
				
			if d == 0x2A:
				byteLen = 3
				cycles = 16
				self.regL = self.RAM[self.regPC+1]
				self.regH = self.RAM[self.regPC+2]
				decPnt(self, '0x2A : LHLD a16')
				
			if d == 0x2B:
				cycles = 5
				self.regH, self.regL = self.dcx(self.regH, self.regL)
				decPnt(self, '0x2B : DCX H')
				
			if d == 0x2C:
				cycles = 5
				self.regL = self.inr(self.regL)
				decPnt(self, '0x2C : INR L')
				
			if d == 0x2D:
				cycles = 5
				self.regL = self.dcr(self.regL)
				decPnt(self, '0x2D : DCR L')
				
			if d == 0x2E:
				byteLen = 2
				cycles = 7
				self.regL = self.RAM[self.regPC+1]
				decPnt(self, '0x2E : MVI L, d8')
				
			if d == 0x2F:
				cycles = 4
				#TODO NOT A
				decPnt(self, '0x2F : CMA')
				

		########
		# 0x3X #
		########
		if((d & ~0x3F) == 0):
			if d == 0x30:
				cycles = 4
				decPnt(self, '0x30 : NOP')
				
			if d == 0x31:
				byteLen = 3
				cycles = 10
				self.regSPL = self.RAM[self.regPC+1]
				self.regSPH = self.RAM[self.regPC+2]
				decPnt(self, '0x31 : LXI SP, d16')
				
			if d == 0x32:
				byteLen = 3
				cycles = 13
				self.RAM[(self.regPC+1)<<8 | self.regPC+2] = self.regA
				decPnt(self, '0x32 : STA a16')
				
			if d == 0x33:
				cycles = 5
				self.regSPH, self.regSPL = self.inx(self.regSPH, self.regSPL)
				decPnt(self, '0x33 : INX SP')
				
			if d == 0x34:
				cycles = 10
				self.regH, self.regL = self.inr(self.regH, self.regL)
				decPnt(self, '0x34 : INR M')
				
			if d == 0x35:
				cycles = 10
				self.regH, self.regL = self.dcr(self.regH, self.regL)
				decPnt(self, '0x35 : DCR M')
				
			if d == 0x36:
				byteLen = 2
				cycles = 10
				self.regL = self.RAM[self.regPC+1]
				decPnt(self, '0x36 : MVI M, d8')
				
			if d == 0x37:
				cycles = 4
				self.statC = True
				decPnt(self, '0x37 : STC')
				
			if d == 0x38:
				cycles = 4
				decPnt(self, '0x38 : NOP')
				
			if d == 0x39:
				byteLen = 1
				cycles = 10
				self.regH, self.regL = self.dad(self.regSPH, self.regSPL)
				decPnt(self, '0x39 : DAD SP')
				
			if d == 0x3A:
				byteLen = 3
				cycles = 13
				self.regA = self.RAM[(self.RAM[self.regPC+1]<<8) | self.RAM[self.regPC+2]]
				decPnt(self, '0x3A : LDA a16')
				
			if d == 0x3B:
				cycles = 5
				self.regSPH, self.regSPL = self.dcx(self.regSPH, self.regSPL)
				decPnt(self, '0x3B : DCX SP')
				
			if d == 0x3C:
				cycles = 5
				self.regA = self.inr(self.regA)
				decPnt(self, '0x3C : INR A')
				
			if d == 0x3D:
				cycles = 5
				self.regA = self.dcr(self.regA)
				decPnt(self, '0x3D : DCR A')
				
			if d == 0x3E:
				byteLen = 2
				cycles = 7
				self.regA = self.RAM[self.regPC+1]
				decPnt(self, '0x3E : MVI A, d8')
				
			if d == 0x3F:
				cycles = 4
				##TODO
				decPnt(self, '0x3F : CMC')

			self.regPC+=byteLen
			
			
		

#print hex address of cpu with the corresponding code
def decPnt(cpu, str):
	print(hex(cpu.address) + '; ' + str)
	return

#https://www.geeksforgeeks.org/finding-the-parity-of-a-number-efficiently/
def findParity(x):
	y = x ^ (x >> 1); 
	y = y ^ (y >> 2) 
	y = y ^ (y >> 4) 
	y = y ^ (y >> 8) 
	y = y ^ (y >> 16)

	if (y & 1): 
		return 1 
	return 0; 
	
def main():
	cpu = v8080()
	cpu.RAM = [0x01, 0x55, 0xAA, 0x0C]
	print(str(cpu.regB) + ' : reg B, ' + str(cpu.regC) + ' : reg C')
	cpu.decode()
	print(str(cpu.regB) + ' : reg B, ' + str(cpu.regC) + ' : reg C')
	cpu.decode()
	print(str(cpu.regB) + ' : reg B, ' + str(cpu.regC) + ' : reg C')

main()
