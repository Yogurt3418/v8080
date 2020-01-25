import time

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
		self.regE = 0
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
		self.RAM = 0
		#8K Rom
		#self.ROM = [None] * 8 * 1024
		
	def regDump(self):
		print('****CPU REGs****')
		print('REG A   : ' + str(hex(self.regA)))
		print('REG B   : ' + str(hex(self.regB)))
		print('REG C   : ' + str(hex(self.regC)))
		print('REG D   : ' + str(hex(self.regD)))
		print('REG E   : ' + str(hex(self.regE)))
		print('REG H   : ' + str(hex(self.regH)))
		print('REG L   : ' + str(hex(self.regL)))
		print('REG SPL : ' + str(hex(self.regSPL)))
		print('REG SPH : ' + str(hex(self.regSPH)))
		print('REG PC  : ' + str(hex(self.regPC)))
		print('****CPU FLAGS****')
		print('FLAG S  : ' + str(self.statS))
		print('FLAG Z  : ' + str(self.statZ))
		print('FLAG AC : ' + str(self.statAC))
		print('FLAG P  : ' + str(self.statP))
		print('FLAG C  : ' + str(self.statC))
		print('****END CPU STATS****')
		return

	def setFlagsZSP(self, a):
		if(a == 0):
			self.statZ = True
		else:
			self.statZ = False
			
		if((a & 0x80) != 0):
			self.statS = True
		else:
			self.statS = False
			
		if(findParity(a)):
			self.statP = True
		else:
			self.statP = False

		return

	def inx(self, a, b):
		
		c = (a<<8) | b
		c+=1
		a = (c & 0xFF00)>>8
		b = c & 0xFF
		
		return a, b

	def inr(self, a):
		
		a = a + 1
		if(a > 0xFF):
			a = 0
			#self.statAC = True

		self.setFlagsZSP(a)
			
		return a

	def dcr(self, a):
		
		a = a - 1
		if(a < 0):
			a = 255
			#self.statAC = True
		
		self.setFlagsZSP(a)
			
		return a

	def rlc(self, a):
		return (a << 1)|(a >> (7))

	def rrc(self, a):
		return (a >> 1)|(a << (7))

	def rar(self, a):
		b = (a<<7)|(int(self.statC))
		self.statC = bool((a&0x80)>>7)
		return b

	def orr(self, a):
		self.regA = self.regA | a
		

	def dad(self, a, b):
		x = (self.regH<<8) | self.regL
		y = (a<<8) | b
		x+=y
		if(x>=(1<<16)):
			self.statC = True
			x = 0
			
		return (x&0xFF00)>>8, (x&0xFF)

	def dcx(self, a, b):
		c = (a<<8) | b
		
		if( c == 0 ):
			c = 0xFFFF
		else:
			c = c - 1
			
		a = (c & 0xFF00)>>8
		b = c & 0xFF
		
		return a, b

	##I have yet to really test these so IDK if they work right
	def add(self, v):
		v = self.regA + v
		if(v>256):
			self.statC = True
			v = v & 0xFF
			
		self.setFlagsZSP(v)
		
		#TODO: Set AC Flag?
		self.regA = v

	def adc(self, v):
		v = self.regA + v + (int)(self.statC)
		if(v>256):
			self.statC = True
			v = v & 0xFF

		self.setFlagsZSP(v)
		#TODO: Set AC Flag?
		self.regA = v

	def sub(self, v):
		v = self.regA - v
		if(v<0):
			self.statC = True
			v = v & 0xFF
			
		self.setFlagsZSP(v)
		#TODO: Set AC Flag?
		self.regA = v

	def sbb(self, v):
		v = self.regA - v - (int)(self.statC)
		if(v<0):
			self.statC = True
			v = v & 0xFF

		self.setFlagsZSP(v)
		#TODO: Set AC Flag?
		self.regA = v

	def ana(self, v):
		v = self.regA & v
		if(v>256):
			self.statC = True

		self.setFlagsZSP(v)
		#TODO: Set AC Flag?
		self.regA = v

	def xra(self, v):
		v = self.regA ^ v
		if(v>256):
			self.statC = True

		self.setFlagsZSP(v)
		#TODO: Set AC Flag?
		self.regA = v

	def ora(self, v):
		self.regA = self.regA | v
		if(self.regA>256):
			self.regA = self.regA & 0xFF
			self.statC = True

		self.setFlagsZSP(self.regA)
		#TODO: Set AC Flag?
		return

	def cmp(self, v):
		v = self.regA - v
		if(v<0):
			self.statC = True

		self.setFlagsZSP(v)
		#TODO: Set AC Flag?
		return 

	def pop(self):
		##this is going to need some testing
		#self.regDump()
		a = self.RAM[(self.regSPH<<8)|(self.regSPL)]
		b = self.RAM[(self.regSPH<<8)|(self.regSPL)+1]
		c = (self.regSPH<<8) | self.regSPL
		c = c + 2
		self.regSPL = c & 0x00FF
		self.regSPH = (c & 0xFF00)>>8
		return a, b

	def push(self, a, b):
		##so is this
		self.RAM[(self.regSPH<<8)|(self.regSPL)-2] = a
		self.RAM[(self.regSPH<<8)|(self.regSPL)-1] = b
		c = (self.regSPH<<8) | self.regSPL
		c = c - 2
		self.regSPL = c & 0x00FF
		self.regSPH = (c & 0xFF00)>>8
		return

	def call(self):
		##this needs more testing!
		c = (self.regSPH<<8) | self.regSPL
		self.RAM[c-1] = ((self.regPC+3) & 0xFF00)>>8
		self.RAM[c-2] = (self.regPC+3) & 0xFF
		c = c - 2
		self.regPC = (self.RAM[self.regPC+2]<<8)|(self.RAM[self.regPC+1])
		self.regSPL = c & 0x00FF
		self.regSPH = (c & 0xFF00)>>8
		return

	def ret(self):
		c = (self.regSPH<<8) | self.regSPL
		self.regPC = self.RAM[c] | (self.RAM[c+1]<<8)
		c = c + 2
		self.regSPL = c & 0x00FF
		self.regSPH = (c & 0xFF00)>>8

	def rst(self, a):
		self.RAM[((self.regSPH<<8)|(self.regSPL))-1] = (self.regPC & 0xFF00)>>8
		self.RAM[((self.regSPH<<8)|(self.regSPL))-2] = self.regPC & 0x00FF
		self.regPC = a*8
		return

	def xthl(self):
		a = self.regH
		b = self.regL
		self.regL = self.RAM[(self.regSPH<<8)|(self.regSPL)]
		self.regH = self.RAM[((self.regSPH<<8)|(self.regSPL))+1]
		self.RAM[(self.regSPH<<8)|(self.regSPL)] = b
		self.RAM[((self.regSPH<<8)|(self.regSPL))+1] = a
		return

	def xchg(self):
		a = self.regH
		b = self.regL
		self.regH = self.regD
		self.regL = self.regE
		self.regD = a
		self.regE = b
		return


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
				self.RAM[(((self.regPC+1)<<8) | (self.regPC+2))] = self.regA
				decPnt(self, '0x32 : STA a16')
				
			if d == 0x33:
				cycles = 5
				self.regSPH, self.regSPL = self.inx(self.regSPH, self.regSPL)
				decPnt(self, '0x33 : INX SP')
				
			if d == 0x34:
				cycles = 10
				self.RAM[(self.regH<<8) | self.regL] = self.inr(self.RAM[(self.regH<<8) | self.regL])
				decPnt(self, '0x34 : INR M')
				
			if d == 0x35:
				cycles = 10
				self.RAM[(self.regH<<8) | self.regL] = self.dcr(self.RAM[(self.regH<<8) | self.regL])
				decPnt(self, '0x35 : DCR M')
				
			if d == 0x36:
				byteLen = 2
				cycles = 10
				self.RAM[(self.regH<<8) | self.regL] = self.RAM[self.regPC+1]
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

		#TODO, FIX INR AND DCR? 0x34??
		########
		# 0x4X #
		########
		if((d & ~0x4F) == 0):
			if d == 0x40:
				cycles = 5
				self.regB = self.regB
				decPnt(self, '0x40 : MOV B, B')
				
			if d == 0x41:
				cycles = 5
				self.regB = self.regC
				decPnt(self, '0x41 : MOV B, C')
				
			if d == 0x42:
				cycles = 5
				self.regB = self.regD
				decPnt(self, '0x42 : MOV B, D')
				
			if d == 0x43:
				cycles = 5
				self.regB = self.regE
				decPnt(self, '0x43 : MOV B, E')
				
			if d == 0x44:
				cycles = 5
				self.regB = self.regH
				decPnt(self, '0x44 : MOV B, H')
				
			if d == 0x45:
				cycles = 5
				self.regB = self.regL
				decPnt(self, '0x45 : MOV B, L')
				
			if d == 0x46:
				cycles = 7
				self.regB = self.RAM[(self.regH<<8) | self.regL]
				decPnt(self, '0x46 : MOV B, M')
				
			if d == 0x47:
				cycles = 5
				self.regB = self.regA
				decPnt(self, '0x47 : MOV B, A')
				
			if d == 0x48:
				cycles = 5
				self.regC = self.regB
				decPnt(self, '0x48 : MOV C, B')
				
			if d == 0x49:
				cycles = 5
				self.regC = self.regC
				decPnt(self, '0x49 : MOV C, C')
				
			if d == 0x4A:
				cycles = 5
				self.regC = self.regD
				decPnt(self, '0x4A : MOV C, D')
				
			if d == 0x4B:
				cycles = 5
				self.regC = self.regE
				decPnt(self, '0x4B : MOV C, E')
				
			if d == 0x4C:
				cycles = 5
				self.regC = self.regH
				decPnt(self, '0x4C : MOV C, H')
				
			if d == 0x4D:
				cycles = 5
				self.regC = self.regL
				decPnt(self, '0x4D : MOV C, L')
				
			if d == 0x4E:
				cycles = 7
				self.regC = self.RAM[(self.regH<<8) | self.regL]
				decPnt(self, '0x4E : MOV C, M')
				
			if d == 0x4F:
				cycles = 5
				self.regC = self.regA
				decPnt(self, '0x4F : MOV C, A')


		########
		# 0x5X #
		########
		if((d & ~0x5F) == 0):
			if d == 0x50:
				cycles = 5
				self.regD = self.regB
				decPnt(self, '0x50 : MOV D, B')
				
			if d == 0x51:
				cycles = 5
				self.regD = self.regC
				decPnt(self, '0x51 : MOV D, C')
				
			if d == 0x52:
				cycles = 5
				self.regD = self.regD
				decPnt(self, '0x52 : MOV D, D')
				
			if d == 0x53:
				cycles = 5
				self.regD = self.regE
				decPnt(self, '0x53 : MOV D, E')
				
			if d == 0x54:
				cycles = 5
				self.regD = self.regH
				decPnt(self, '0x54 : MOV D, H')
				
			if d == 0x55:
				cycles = 5
				self.regD = self.regL
				decPnt(self, '0x55 : MOV D, L')
				
			if d == 0x56:
				cycles = 7
				self.regD = self.RAM[(self.regH<<8) | self.regL]
				decPnt(self, '0x56 : MOV D, M')
				
			if d == 0x57:
				cycles = 5
				self.regD = self.regA
				decPnt(self, '0x57 : MOV D, A')
				
			if d == 0x58:
				cycles = 5
				self.regE = self.regB
				decPnt(self, '0x58 : MOV E, B')
				
			if d == 0x59:
				cycles = 5
				self.regE = self.regC
				decPnt(self, '0x59 : MOV E, C')
				
			if d == 0x5A:
				cycles = 5
				self.regE = self.regD
				decPnt(self, '0x5A : MOV E, D')
				
			if d == 0x5B:
				cycles = 5
				self.regE = self.regE
				decPnt(self, '0x5B : MOV E, E')
				
			if d == 0x5C:
				cycles = 5
				self.regE = self.regH
				decPnt(self, '0x5C : MOV E, H')
				
			if d == 0x5D:
				cycles = 5
				self.regE = self.regL
				decPnt(self, '0x5D : MOV E, L')
				
			if d == 0x5E:
				cycles = 7
				self.regE = self.RAM[(self.regH<<8) | self.regL]
				decPnt(self, '0x5E : MOV E, M')
				
			if d == 0x5F:
				cycles = 5
				self.regE = self.regA
				decPnt(self, '0x5F : MOV E, A')


		########
		# 0x6X #
		########
		if((d & ~0x6F) == 0):
			if d == 0x60:
				cycles = 5
				self.regH = self.regB
				decPnt(self, '0x60 : MOV H, B')
				
			if d == 0x61:
				cycles = 5
				self.regH = self.regC
				decPnt(self, '0x61 : MOV H, C')
				
			if d == 0x62:
				cycles = 5
				self.regH = self.regD
				decPnt(self, '0x62 : MOV H, D')
				
			if d == 0x63:
				cycles = 5
				self.regH = self.regE
				decPnt(self, '0x63 : MOV H, E')
				
			if d == 0x64:
				cycles = 5
				self.regH = self.regH
				decPnt(self, '0x64 : MOV H, H')
				
			if d == 0x65:
				cycles = 5
				self.regH = self.regL
				decPnt(self, '0x65 : MOV H, L')
				
			if d == 0x66:
				cycles = 7
				self.regH = self.RAM[(self.regH<<8) | self.regL]
				decPnt(self, '0x66 : MOV H, M')
				
			if d == 0x67:
				cycles = 5
				self.regH = self.regA
				decPnt(self, '0x67 : MOV H, A')
				
			if d == 0x68:
				cycles = 5
				self.regL = self.regB
				decPnt(self, '0x68 : MOV L, B')
				
			if d == 0x69:
				cycles = 5
				self.regL = self.regC
				decPnt(self, '0x69 : MOV L, C')
				
			if d == 0x6A:
				cycles = 5
				self.regL = self.regD
				decPnt(self, '0x6A : MOV L, D')
				
			if d == 0x6B:
				cycles = 5
				self.regL = self.regE
				decPnt(self, '0x6B : MOV L, E')
				
			if d == 0x6C:
				cycles = 5
				self.regL = self.regH
				decPnt(self, '0x6C : MOV L, H')
				
			if d == 0x6D:
				cycles = 5
				self.regL = self.regL
				decPnt(self, '0x6D : MOV L, L')
				
			if d == 0x6E:
				cycles = 7
				self.regL = self.RAM[(self.regH<<8) | self.regL]
				decPnt(self, '0x6E : MOV L, M')
				
			if d == 0x6F:
				cycles = 5
				self.regL = self.regA
				decPnt(self, '0x6F : MOV L, A')


		########
		# 0x7X #
		########
		if((d & ~0x7F) == 0):
			if d == 0x70:
				cycles = 7
				self.RAM[(self.regH<<8) | self.regL] = self.regB
				decPnt(self, '0x70 : MOV M, B')
				
			if d == 0x71:
				cycles = 7
				self.RAM[(self.regH<<8) | self.regL] = self.regC
				decPnt(self, '0x71 : MOV M, C')
				
			if d == 0x72:
				cycles = 7
				self.RAM[(self.regH<<8) | self.regL] = self.regD
				decPnt(self, '0x72 : MOV M, D')
				
			if d == 0x73:
				cycles = 7
				self.RAM[(self.regH<<8) | self.regL] = self.regE
				decPnt(self, '0x73 : MOV M, E')
				
			if d == 0x74:
				cycles = 7
				self.RAM[(self.regH<<8) | self.regL] = self.regH
				decPnt(self, '0x74 : MOV M, H')
				
			if d == 0x75:
				cycles = 7
				self.RAM[(self.regH<<8) | self.regL] = self.regL
				decPnt(self, '0x75 : MOV M, L')
				
			if d == 0x76:
				cycles = 7
				##Do something?
				decPnt(self, '0x76 : HLT')
				
			if d == 0x77:
				cycles = 5
				#self.regDump()
				self.RAM[(self.regH<<8) | self.regL] = self.regA
				decPnt(self, '0x77 : MOV M, A')
				
			if d == 0x78:
				cycles = 5
				self.regA = self.regB
				decPnt(self, '0x78 : MOV A, B')
				
			if d == 0x79:
				cycles = 5
				self.regA = self.regC
				decPnt(self, '0x79 : MOV A, C')
				
			if d == 0x7A:
				cycles = 5
				self.regA = self.regD
				decPnt(self, '0x7A : MOV A, D')
				
			if d == 0x7B:
				cycles = 5
				self.regA = self.regE
				decPnt(self, '0x7B : MOV A, E')
				
			if d == 0x7C:
				cycles = 5
				self.regA = self.regH
				decPnt(self, '0x7C : MOV A, H')
				
			if d == 0x7D:
				cycles = 5
				self.regA = self.regL
				decPnt(self, '0x7D : MOV A, L')
				
			if d == 0x7E:
				cycles = 7
				self.regA = self.RAM[(self.regH<<8) | self.regL]
				decPnt(self, '0x7E : MOV A, M')
				
			if d == 0x7F:
				cycles = 5
				self.regA = self.regA
				decPnt(self, '0xAF : MOV A, A')


		########
		# 0x8X #
		########
		if((d & ~0x8F) == 0):
			if d == 0x80:
				cycles = 4
				self.regA = self.add(self.regB)
				decPnt(self, '0x80 : ADD B')
				
			if d == 0x81:
				cycles = 4
				self.regA = self.add(self.regC)
				decPnt(self, '0x81 : ADD C')
				
			if d == 0x82:
				cycles = 4
				self.regA = self.add(self.regD)
				decPnt(self, '0x82 : ADD D')
				
			if d == 0x83:
				cycles = 4
				self.regA = self.add(self.regE)
				decPnt(self, '0x83 : ADD E')
				
			if d == 0x84:
				cycles = 4
				self.regA = self.add(self.regH)
				decPnt(self, '0x84 : ADD H')
				
			if d == 0x85:
				cycles = 4
				self.regA = self.add(self.regL)
				decPnt(self, '0x85 : ADD L')
				
			if d == 0x86:
				cycles = 4
				self.regA = self.add(self.RAM[(self.regH<<8) | self.regL])
				decPnt(self, '0x86 : ADD M')
				
			if d == 0x87:
				cycles = 4
				self.regA = self.add(self.regA)
				decPnt(self, '0x87 : ADD A')
				
			if d == 0x88:
				cycles = 4
				self.regA = self.adc(self.regB)
				decPnt(self, '0x88 : ADC B')
				
			if d == 0x89:
				cycles = 4
				self.regA = self.adc(self.regC)
				decPnt(self, '0x89 : ADC C')
				
			if d == 0x8A:
				cycles = 4
				self.regA = self.adc(self.regD)
				decPnt(self, '0x8A : ADC D')
				
			if d == 0x8B:
				cycles = 4
				self.regA = self.adc(self.regE)
				decPnt(self, '0x8B : ADC E')
				
			if d == 0x8C:
				cycles = 4
				self.regA = self.adc(self.regH)
				decPnt(self, '0x8C : ADC H')
				
			if d == 0x8D:
				cycles = 4
				self.regA = self.adc(self.regL)
				decPnt(self, '0x8D : ADC L')
				
			if d == 0x8E:
				cycles = 7
				self.regA = self.adc(self.RAM[(self.regH<<8) | self.regL])
				decPnt(self, '0x8E : ADC M')
				
			if d == 0x8F:
				cycles = 4
				self.regA = self.adc(self.regA)
				decPnt(self, '0x8F : ADC A')


		########
		# 0x9X #
		########
		if((d & ~0x9F) == 0):
			if d == 0x90:
				cycles = 4
				self.regA = self.sub(self.regB)
				decPnt(self, '0x90 : SUB B')
				
			if d == 0x91:
				cycles = 4
				self.regA = self.sub(self.regC)
				decPnt(self, '0x91 : SUB C')
				
			if d == 0x92:
				cycles = 4
				self.regA = self.sub(self.regD)
				decPnt(self, '0x92 : SUB D')
				
			if d == 0x93:
				cycles = 4
				self.regA = self.sub(self.regE)
				decPnt(self, '0x93 : SUB E')
				
			if d == 0x94:
				cycles = 4
				self.regA = self.sub(self.regH)
				decPnt(self, '0x94 : SUB H')
				
			if d == 0x95:
				cycles = 4
				self.regA = self.sub(self.regL)
				decPnt(self, '0x95 : SUB L')
				
			if d == 0x96:
				cycles = 7
				self.regA = self.sub(self.RAM[(self.regH<<8) | self.regL])
				decPnt(self, '0x96 : SUB M')
				
			if d == 0x97:
				cycles = 4
				#this is 0, right?
				self.regA = self.sub(self.regA)
				decPnt(self, '0x97 : SUB A')
				
			if d == 0x98:
				cycles = 4
				self.regA = self.sbb(self.regB)
				decPnt(self, '0x98 : SBB B')
				
			if d == 0x99:
				cycles = 4
				self.regA = self.sbb(self.regC)
				decPnt(self, '0x99 : SBB C')
				
			if d == 0x9A:
				cycles = 4
				self.regA = self.sbb(self.regD)
				decPnt(self, '0x9A : SBB D')
				
			if d == 0x9B:
				cycles = 4
				self.regA = self.sbb(self.regE)
				decPnt(self, '0x9B : SBB E')
				
			if d == 0x9C:
				cycles = 4
				self.regA = self.sbb(self.regH)
				decPnt(self, '0x9C : SBB H')
				
			if d == 0x9D:
				cycles = 4
				self.regA = self.sbb(self.regL)
				decPnt(self, '0x9D : SBB L')
				
			if d == 0x9E:
				cycles = 7
				self.regA = self.sbb(self.RAM[(self.regH<<8) | self.regL])
				decPnt(self, '0x9E : SBB M')
				
			if d == 0x9F:
				cycles = 4
				self.regA = self.sbb(self.regA)
				decPnt(self, '0x9F : SBB A')


		########
		# 0xAX #
		########
		if((d & ~0xAF) == 0):
			if d == 0xA0:
				cycles = 4
				self.regA = self.ana(self.regB)
				decPnt(self, '0xA0 : ANA B')
				
			if d == 0xA1:
				cycles = 4
				self.regA = self.ana(self.regC)
				decPnt(self, '0xA1 : ANA C')
				
			if d == 0xA2:
				cycles = 4
				self.regA = self.ana(self.regD)
				decPnt(self, '0xA2 : ANA D')
				
			if d == 0xA3:
				cycles = 4
				self.regA = self.ana(self.regE)
				decPnt(self, '0xA3 : ANA E')
				
			if d == 0xA4:
				cycles = 4
				self.regA = self.ana(self.regH)
				decPnt(self, '0xA4 : ANA H')
				
			if d == 0xA5:
				cycles = 4
				self.regA = self.ana(self.regL)
				decPnt(self, '0xA5 : ANA L')
				
			if d == 0xA6:
				cycles = 7
				self.regA = self.ana(self.RAM[(self.regH<<8) | self.regL])
				decPnt(self, '0xA6 : ANA M')
				
			if d == 0xA7:
				cycles = 4
				self.regA = self.ana(self.regA)
				decPnt(self, '0xA7 : ANA A')
				
			if d == 0xA8:
				cycles = 4
				self.regA = self.xra(self.regB)
				decPnt(self, '0xA8 : XRA B')
				
			if d == 0xA9:
				cycles = 4
				self.regA = self.xra(self.regC)
				decPnt(self, '0xA9 : XRA C')
				
			if d == 0xAA:
				cycles = 4
				self.regA = self.xra(self.regD)
				decPnt(self, '0xAA : XRA D')
				
			if d == 0xAB:
				cycles = 4
				self.regA = self.xra(self.regE)
				decPnt(self, '0xAB : XRA E')
				
			if d == 0xAC:
				cycles = 4
				self.regA = self.xra(self.regH)
				decPnt(self, '0xAC : XRA H')
				
			if d == 0xAD:
				cycles = 4
				self.regA = self.xra(self.regL)
				decPnt(self, '0xAD : XRA L')
				
			if d == 0xAE:
				cycles = 7
				self.regA = self.xra(self.RAM[(self.regH<<8) | self.regL])
				decPnt(self, '0xAE : XRA M')
				
			if d == 0xAF:
				cycles = 4
				self.regA = 0
				decPnt(self, '0xAF : XRA A')


		########
		# 0xBX #
		########
		if((d & ~0xBF) == 0):
			if d == 0xB0:
				cycles = 4
				self.ora(self.regB)
				decPnt(self, '0xB0 : ORA B')
				
			if d == 0xB1:
				cycles = 4
				self.ora(self.regC)
				decPnt(self, '0xB1 : ORA C')
				
			if d == 0xB2:
				cycles = 4
				self.ora(self.regD)
				decPnt(self, '0xB2 : ORA D')
				
			if d == 0xB3:
				cycles = 4
				self.ora(self.regE)
				decPnt(self, '0xB3 : ORA E')
				
			if d == 0xB4:
				cycles = 4
				self.ora(self.regH)
				decPnt(self, '0xB4 : ORA H')
				
			if d == 0xB5:
				cycles = 4
				self.ora(self.regL)
				decPnt(self, '0xB5 : ORA L')
				
			if d == 0xB6:
				cycles = 7
				self.ora(self.RAM[(self.regH<<8) | self.regL])
				decPnt(self, '0xB6 : ORA M')
				
			if d == 0xB7:
				cycles = 4
				self.ora(self.regA)
				decPnt(self, '0xB7 : ORA A')
				
			if d == 0xB8:
				cycles = 4
				self.cmp(self.regB)
				decPnt(self, '0xB8 : CMP B')
				
			if d == 0xB9:
				cycles = 4
				self.cmp(self.regC)
				decPnt(self, '0xB9 : CMP C')
				
			if d == 0xBA:
				cycles = 4
				self.cmp(self.regD)
				decPnt(self, '0xBA : CMP D')
				
			if d == 0xBB:
				cycles = 4
				self.cmp(self.regE)
				decPnt(self, '0xBB : CMP E')
				
			if d == 0xBC:
				cycles = 4
				self.cmp(self.regH)
				decPnt(self, '0xBC : CMP H')
				
			if d == 0xBD:
				cycles = 4
				self.cmp(self.regL)
				decPnt(self, '0xBD : CMP L')
				
			if d == 0xBE:
				cycles = 7
				self.cmp(self.RAM[(self.regH<<8) | self.regL])
				decPnt(self, '0xBE : CMP M')
				
			if d == 0xBF:
				cycles = 4
				self.cmp(self.regA)
				decPnt(self, '0xBF : CMP A')


		########
		# 0xCX #
		########
		if((d & ~0xCF) == 0):
			if d == 0xC0:
				cycles = 11
				if(~self.statZ):
					self.ret()
				decPnt(self, '0xC0 : RNZ')
				
			if d == 0xC1:
				cycles = 10
				self.regC, self.regB = self.pop()
				decPnt(self, '0xC1 : POP B')
				
			if d == 0xC2:
				cycles = 10
				byteLen = 3
				if(self.statZ == 0):
					self.regPC = (self.RAM[self.regPC+2]<<8) | (self.RAM[self.regPC+1])
					byteLen = 0
				decPnt(self, '0xC2 : JNZ')
				
			if d == 0xC3:
				cycles = 10
				byteLen = 0
				self.regPC = (self.RAM[self.regPC+2]<<8) | (self.RAM[self.regPC+1])
				decPnt(self, '0xC3 : JMP')
				
			if d == 0xC4:
				cycles = 17
				byteLen = 3
				if(~self.statZ):
					self.call()
					byteLen = 0
				decPnt(self, '0xC4 : CNZ')
				
			if d == 0xC5:
				cycles = 11
				self.push(self.regC, self.regB)
				decPnt(self, '0xC5 : PUSH B')
				
			if d == 0xC6:
				cycles = 7
				byteLen = 2
				self.add(self.RAM[self.regPC+1])
				decPnt(self, '0xC6 : ADI')
				
			if d == 0xC7:
				cycles = 11
				self.rst(0)
				byteLen = 0
				decPnt(self, '0xC7 : RST 0')
				
			if d == 0xC8:
				cycles = 11
				if(self.statZ):
					self.ret()
					byteLen = 0
				decPnt(self, '0xC8 : RZ')
				
			if d == 0xC9:
				cycles = 11
				self.ret()
				byteLen = 0
				decPnt(self, '0xC9 : RET')
				
			if d == 0xCA:
				cycles = 10
				byteLen = 3
				if(self.statZ):
					self.regPC = (self.RAM[self.regPC+2]<<8) | (self.RAM[self.regPC+1])
					byteLen = 0
				decPnt(self, '0xCA : JZ')
				
			if d == 0xCB:
				#another Jump, this shouldn't occur
				decPnt(self, '0xCB : JMP; IGNORED, DNE')
				
			if d == 0xCC:
				cycles = 17
				byteLen = 3
				if(self.statZ):
					self.call()
					byteLen = 0
				decPnt(self, '0xCC : CZ')
				
			if d == 0xCD:
				cycles = 17
				self.call()
				byteLen = 0
				decPnt(self, '0xCD : CALL')
				
			if d == 0xCE:
				cycles = 7
				byteLen = 2
				self.adc(self.RAM[self.regPC+1])
				decPnt(self, '0xCE : ADC ')
				
			if d == 0xCF:
				cycles = 11
				self.rst(1)
				decPnt(self, '0xCF : RST 1')


		########
		# 0xDX #
		########
		if((d & ~0xDF) == 0):
			if d == 0xD0:
				cycles = 11
				if(~self.statC):
					self.ret()
				decPnt(self, '0xD0 : RNC')
				
			if d == 0xD1:
				cycles = 10
				self.regE, self.regD = self.pop()
				decPnt(self, '0xD1 : POP D')
				
			if d == 0xD2:
				cycles = 10
				byteLen = 3
				if(~self.statC):
					self.regPC = (self.RAM[self.regPC+2]<<8) | (self.RAM[self.regPC+1])
					byteLen = 0
				decPnt(self, '0xD2 : JNC')
				
			if d == 0xD3:
				cycles = 10
				byteLen = 2
				#Write A to output port
				decPnt(self, '0xD3 : OUT')
				
			if d == 0xD4:
				cycles = 17
				byteLen = 3
				if(~self.statC):
					self.call()
					byteLen = 0
				decPnt(self, '0xD4 : CNC')
				
			if d == 0xD5:
				cycles = 11
				self.push(self.regE, self.regD)
				decPnt(self, '0xD5 : PUSH D')
				
			if d == 0xD6:
				cycles = 7
				byteLen = 2
				self.sub(self.RAM[self.regPC+1])
				decPnt(self, '0xD6 : SUI')
				
			if d == 0xD7:
				cycles = 11
				self.rst(2)
				byteLen = 0
				decPnt(self, '0xD7 : RST 2')
				
			if d == 0xD8:
				cycles = 11
				if(self.statC):
					self.ret()
					byteLen = 0
				decPnt(self, '0xD8 : RZ')
				
			if d == 0xD9:
				cycles = 11
				self.ret()
				byteLen = 0
				decPnt(self, '0xD9 : RET')
				
			if d == 0xDA:
				cycles = 10
				byteLen = 3
				if(self.statC):
					self.regPC = (self.RAM[self.regPC+2]<<8) | (self.RAM[self.regPC+1])
					byteLen = 0
				decPnt(self, '0xDA : JC')
				
			if d == 0xDB:
				#Read input on port A
				byteLen = 2
				cycles = 10
				decPnt(self, '0xDB : IN; DNE')
				
			if d == 0xDC:
				cycles = 17
				byteLen = 3
				if(self.statC):
					self.call()
					byteLen = 0
				decPnt(self, '0xDC : CZ')
				
			if d == 0xDD:
				cycles = 17
				self.call()
				decPnt(self, '0xDD : CALL')
				
			if d == 0xDE:
				cycles = 7
				byteLen = 2
				self.sbc(self.RAM[self.regPC+1])
				decPnt(self, '0xDE : SBI')
				
			if d == 0xDF:
				cycles = 11
				self.rst(3)
				decPnt(self, '0xDF : RST 1')


		########
		# 0xEX #
		########
		if((d & ~0xEF) == 0):
			if d == 0xE0:
				cycles = 11
				if(self.statP):
					self.ret()
				decPnt(self, '0xE0 : RPO')
				
			if d == 0xE1:
				cycles = 10
				self.regL, self.regH = self.pop()
				decPnt(self, '0xE1 : POP H')
				
			if d == 0xE2:
				cycles = 10
				byteLen = 3
				if(self.statC):
					self.regPC = (self.RAM[self.regPC+2]<<8) | (self.RAM[self.regPC+1])
					byteLen = 0
				decPnt(self, '0xE2 : JPO')
				
			if d == 0xE3:
				cycles = 18
				byteLen = 1
				self.xthl()
				decPnt(self, '0xE3 : XTHL')
				
			if d == 0xE4:
				cycles = 17
				byteLen = 3
				if(self.statP):
					self.call()
					byteLen = 0
				decPnt(self, '0xE4 : CPO')
				
			if d == 0xE5:
				cycles = 11
				self.push(self.regL, self.regH)
				decPnt(self, '0xE5 : PUSH H')
				
			if d == 0xE6:
				cycles = 7
				byteLen = 2
				self.ana(self.RAM[self.regPC+1])
				decPnt(self, '0xE6 : ANI')
				
			if d == 0xE7:
				cycles = 11
				self.rst(4)
				byteLen = 0
				decPnt(self, '0xE7 : RST 4')
				
			if d == 0xE8:
				cycles = 11
				if(~self.statP):
					self.ret()
					byteLen = 0
				decPnt(self, '0xE8 : RPE')
				
			if d == 0xE9:
				cycles = 11
				self.regPC = (self.regH<<8)|(self.regL)
				decPnt(self, '0xE9 : PCHL')
				
			if d == 0xEA:
				cycles = 10
				byteLen = 3
				if(~self.statP):
					self.regPC = (self.RAM[self.regPC+2]<<8) | (self.RAM[self.regPC+1])
					byteLen = 0
				decPnt(self, '0xEA : JPE')
				
			if d == 0xEB:
				#Read input on port A
				byteLen = 1
				cycles = 5
				self.xchg()
				decPnt(self, '0xEB : XCHG')
				
			if d == 0xEC:
				cycles = 17
				byteLen = 3
				if(~self.statP):
					self.call()
					byteLen = 0
				decPnt(self, '0xEC : CZ')
				
			if d == 0xED:
				cycles = 17
				self.call()
				decPnt(self, '0xED : CALL')
				
			if d == 0xEE:
				cycles = 7
				byteLen = 2
				self.xra(self.RAM[self.regPC+1])
				decPnt(self, '0xEE : SBI')
				
			if d == 0xEF:
				cycles = 11
				self.rst(5)
				decPnt(self, '0xEF : RST 5')


		########
		# 0xFX #
		########
		if((d & ~0xFF) == 0):
			if d == 0xF0:
				cycles = 11
				if(~self.statS):
					self.ret()
				decPnt(self, '0xF0 : RP')
				
			if d == 0xF1:
				cycles = 10
				##TODO POP PSW
				decPnt(self, '0xF1 : POP PSW')
				
			if d == 0xF2:
				cycles = 10
				byteLen = 3
				if(~self.statS):
					self.regPC = (self.RAM[self.regPC+2]<<8) | (self.RAM[self.regPC+1])
					byteLen = 0
				decPnt(self, '0xF2 : JP')
				
			if d == 0xF3:
				cycles = 4
				byteLen = 1
				##???
				decPnt(self, '0xF3 : DI; DNE')
				
			if d == 0xF4:
				cycles = 17
				byteLen = 3
				if(~self.statS):
					self.call()
					byteLen = 0
				decPnt(self, '0xF4 : CP')
				
			if d == 0xF5:
				cycles = 11
				##TODO PUSH PSW
				decPnt(self, '0xF5 : PUSH PSW  *unimplemented*')
				
			if d == 0xF6:
				cycles = 7
				byteLen = 2
				self.orr(self.RAM[self.regPC+1])
				decPnt(self, '0xF6 : ORI')
				
			if d == 0xF7:
				cycles = 11
				self.rst(6)
				byteLen = 0
				decPnt(self, '0xF7 : RST 6')
				
			if d == 0xF8:
				cycles = 11
				if(self.statS):
					self.ret()
					byteLen = 0
				decPnt(self, '0xF8 : RM')
				
			if d == 0xF9:
				cycles = 5
				self.regSPH = self.regH
				self.regSPL = self.regL
				decPnt(self, '0xF9 : SPHL')
				
			if d == 0xFA:
				cycles = 10
				byteLen = 3
				if(self.statS):
					self.regPC = (self.RAM[self.regPC+2]<<8) | (self.RAM[self.regPC+1])
					byteLen = 0
				decPnt(self, '0xFA : JM')
				
			if d == 0xFB:
				byteLen = 1
				cycles = 10
				##TODO Enable Interrupts
				decPnt(self, '0xFB : EI; DNE  *not implemented*')
				
			if d == 0xFC:
				cycles = 17
				byteLen = 3
				if(self.statS):
					self.call()
					byteLen = 0
				decPnt(self, '0xFC : CM')
				
			if d == 0xFD:
				cycles = 17
				self.call()
				decPnt(self, '0xFD : CALL')
				
			if d == 0xFE:
				cycles = 7
				byteLen = 2
				self.cmp(self.RAM[self.regPC+1])
				decPnt(self, '0xFE : CPI')
				
			if d == 0xFF:
				cycles = 11
				self.rst(7)
				decPnt(self, '0xFF : RST 7')

			self.regPC+=byteLen
			
			
		

#print hex address of cpu with the corresponding code
def decPnt(cpu, str):
	print(hex(cpu.regPC) + '; ' + str)
	return

#get parity of number
def findParity(x):
	y = x ^ (x >> 1); 
	y = y ^ (y >> 2) 
	y = y ^ (y >> 4) 
	y = y ^ (y >> 8) 
	y = y ^ (y >> 16)

	if (y & 1): 
		return 1 
	return 0; 
	
#def main():
#	cpu = v8080()
#	f = open("invaders2.asm", "rb")
#	cpu.RAM = bytearray(f.read())
#	while(1):
#		cpu.decode()
#		#cpu.regDump()
#		print('\n')
#		##time.sleep(1)
#	
#main()
