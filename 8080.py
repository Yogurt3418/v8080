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
		self.regSP = 0
		self.regPC = 0
		
		self.statS = 0
		self.statZ = 0
		self.statAC = 0
		self.statP = 0
		self.statC = 0


	def decode(self):

		byteLen = 1
		cycles = 1
		
		d = self.data

		########
		# 0x0X #
		########
		if((d & ~0x0F) == 0):
			if d == 0x00:
				cycles = 7
				decPnt(self, '0x00 : NOP')
				return
			if d == 0x01:
				byteLen = 3
				cycles = 10
				decPnt(self, '0x01 : LXI B, d16')
				return
			if d == 0x02:
				cycles = 7
				decPnt(self, '0x02 : STAX B')
				return
			if d == 0x03:
				cycles = 5
				decPnt(self, '0x03 : INX B')
				return
			if d == 0x04:
				cycles = 5
				decPnt(self, '0x04 : INR B')
				return
			if d == 0x05:
				cycles = 5
				decPnt(self, '0x05 : DCR B')
				return
			if d == 0x06:
				byteLen = 2
				cycles = 7
				decPnt(self, '0x06 : MVI B, d8')
				return
			if d == 0x07:
				byteLen = 1
				cycles = 4
				decPnt(self, '0x07 : RLC')
				return
			if d == 0x08:
				byteLen = 1
				cycles = 4
				decPnt(self, '0x08 : NOP')
				return
			if d == 0x09:
				byteLen = 1
				cycles = 10
				decPnt(self, '0x09 : DAD B')
				return
			if d == 0x0A:
				byteLen = 1
				cycles = 7
				decPnt(self, '0x0A : LDAX B')
				return
			if d == 0x0B:
				cycles = 5
				decPnt(self, '0x0B : DCX B')
				return
			if d == 0x0C:
				cycles = 5
				decPnt(self, '0x0C : INR C')
				return
			if d == 0x0D:
				cycles = 5
				decPnt(self, '0x0D : DCR C')
				return
			if d == 0x0E:
				byteLen = 2
				cycles = 7
				decPnt(self, '0x0E : MVI C, d8')
				return
			if d == 0x0F:
				cycles = 4
				decPnt(self, '0x0F : RRC')
				return

		########
		# 0x1X #
		########
		if((d & ~0x1F) == 0):
			if d == 0x10:
				cycles = 4
				decPnt(self, '0x10 : NOP')
				return
			if d == 0x11:
				byteLen = 3
				cycles = 10
				decPnt(self, '0x11 : LXI D, d16')
				return
			if d == 0x12:
				cycles = 7
				decPnt(self, '0x12 : STAX D')
				return
			if d == 0x13:
				cycles = 5
				decPnt(self, '0x13 : INX D')
				return
			if d == 0x14:
				cycles = 5
				decPnt(self, '0x14 : INR D')
				return
			if d == 0x15:
				cycles = 5
				decPnt(self, '0x15 : DCR D')
				return
			if d == 0x16:
				byteLen = 2
				cycles = 7
				decPnt(self, '0x16 : MVI D, d8')
				return
			if d == 0x17:
				cycles = 4
				decPnt(self, '0x17 : RAL')
				return
			if d == 0x18:
				cycles = 4
				decPnt(self, '0x18 : NOP')
				return
			if d == 0x19:
				byteLen = 1
				cycles = 10
				decPnt(self, '0x19 : DAD D')
				return
			if d == 0x1A:
				byteLen = 1
				cycles = 7
				decPnt(self, '0x1A : LDAX D')
				return
			if d == 0x1B:
				cycles = 5
				decPnt(self, '0x1B : DCX D')
				return
			if d == 0x1C:
				cycles = 5
				decPnt(self, '0x1C : INR E')
				return
			if d == 0x1D:
				cycles = 5
				decPnt(self, '0x1D : DCR E')
				return
			if d == 0x1E:
				byteLen = 2
				cycles = 7
				decPnt(self, '0x1E : MVI E, d8')
				return
			if d == 0x1F:
				cycles = 4
				decPnt(self, '0x1F : RAR')
				return

		########
		# 0x2X #
		########
		if((d & ~0x2F) == 0):
			if d == 0x20:
				cycles = 4
				decPnt(self, '0x20 : NOP')
				return
			if d == 0x21:
				byteLen = 3
				cycles = 10
				decPnt(self, '0x21 : LXI H, d16')
				return
			if d == 0x22:
				byteLen = 3
				cycles = 16
				decPnt(self, '0x22 : SHLD a16')
				return
			if d == 0x23:
				cycles = 5
				decPnt(self, '0x23 : INX H')
				return
			if d == 0x24:
				cycles = 5
				decPnt(self, '0x24 : INR H')
				return
			if d == 0x25:
				cycles = 5
				decPnt(self, '0x25 : DCR H')
				return
			if d == 0x26:
				byteLen = 2
				cycles = 7
				decPnt(self, '0x26 : MVI H, d8')
				return
			if d == 0x27:
				cycles = 4
				decPnt(self, '0x27 : DAA')
				return
			if d == 0x28:
				cycles = 4
				decPnt(self, '0x28 : NOP')
				return
			if d == 0x29:
				byteLen = 1
				cycles = 10
				decPnt(self, '0x19 : DAD H')
				return
			if d == 0x2A:
				byteLen = 3
				cycles = 16
				decPnt(self, '0x2A : LHLD a16')
				return
			if d == 0x2B:
				cycles = 5
				decPnt(self, '0x2B : DCX H')
				return
			if d == 0x2C:
				cycles = 5
				decPnt(self, '0x2C : INR L')
				return
			if d == 0x2D:
				cycles = 5
				decPnt(self, '0x2D : DCR L')
				return
			if d == 0x2E:
				byteLen = 2
				cycles = 7
				decPnt(self, '0x1E : MVI L, d8')
				return
			if d == 0x2F:
				cycles = 4
				decPnt(self, '0x1F : CMA')
				return
		
		

#print hex address of cpu with the corresponding code
def decPnt(cpu, str):
	print(hex(cpu.address) + '; ' + str)
	return
	
def main():
	cpu = v8080()
	cpu.decode()


main()
