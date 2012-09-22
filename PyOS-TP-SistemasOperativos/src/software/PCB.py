'''
Created on 21/09/2012

@author: MarianoLinares
'''

class PCB:

    def __init__(self, kernel, aProgram):
        self.id = kernel.nextPCBID
        self.kernel = kernel
        self.state = "ready"
        self.pc = 0
        self.program = aProgram

    # Return next instruction and increment PC register
    def getInstruction(self):
        retInst = self.program.getInstruction(self.pc)
    
        self.pc += 1
        if self.pc == len(self.program.instructions):
            self.kernel.haltEND()
            return
            
        return retInst