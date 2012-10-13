'''
Created on 21/09/2012

@author: MarianoLinares
'''

class PCB:

    def __init__(self, PCBID, aProgram):
        self.id = PCBID
        self.state = "ready"
        self.pc = 0
        self.program = aProgram
        
    def getInstruction(self):
        return self.program.getInstruction(self.pc)
    
    def increasePC(self):
        self.pc += 1
        
    def isEnded(self):
        # Returns 'true' if PC of currentPCB is higher than length of pcb instructions
        return len(self.program.instructions) <= self.pc