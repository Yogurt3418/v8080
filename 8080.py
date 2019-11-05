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
                        bytelen = 1
                        cycles = 10
                        decPnt(self, '0x09 : DAD B')
                        return

#print hex address of cpu with the corresponding code
def decPnt(cpu, str):
	print(hex(cpu.address) + '; ' + str)
	return
	
def main():
	cpu = v8080()
	cpu.decode()


main()
