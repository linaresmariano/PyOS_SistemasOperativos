'''
Created on 21/09/2012

@author: MarianoLinares
'''

# Models a Program with their name and instructions
class Program:
    def __init__(self, name, path):
        self.name = name
        self.instructions = []
        self.path = path
        
    def length(self):
        return len(self.getInstructions())
    
    def getPath(self):
        return self.path
        
    def addInstruction(self, instr):
        self.instructions.append(instr)
    
    def setInstructions(self, instrs):
        self.instructions = instrs
        
    def getInstructions(self):
        return self.instructions
        
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
        