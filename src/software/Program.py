'''
Created on 21/09/2012

@author: MarianoLinares
'''

# Models a Program with their name and instructions
class Program:
    def __init__(self, name):
        self.name = name
        self.instructions = []
        
    def __len__(self):
        return len(self.getInstructions())
        
    def addInstruction(self, instr):
        self.instructions.append(instr)
    
    def setInstructions(self, instrs):
        self.instructions = instrs
        
    def getInstruction(self, i):
        return self.instructions[i]


# Models a Instruction, which may be to CPU or I/O      
class Instruction:
    def __init__(self, toCPU):
        self.toCPU = toCPU
    
    def isCPUInstruction(self):
        return self.toCPU
    
    def isIOInstruction(self):
        return not self.toCPU
        