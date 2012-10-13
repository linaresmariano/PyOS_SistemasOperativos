'''
Created on 21/09/2012

@author: MarianoLinares
'''

class CPU:

    def __init__(self, aKernel):
        self.currentPCB = None
        self.kernel = aKernel
        self.idle = True
    
    # Execute next instruction in currentPCB
    def tick(self):
        print("CPU idle: " + str(self.idle))
        
        if self.kernel.thisIsTheEnd(): self.kernel.shutDown()
        
        # If is in UserMode and self is not idle, execute next instr        
        if (not self.kernel.modeKernel) and (not self.idle):

            inst = self.currentPCB.getInstruction()
            
            # If is to CPU, execute
            if inst.isCPUInstruction():
                self.currentPCB.increasePC()
                
                # TODO: Log to action
                print("Intruction " + str(self.currentPCB.pc)
                  + " of " + str(len(self.currentPCB.program.instructions))
                  + " of " + str(self.currentPCB.program.name)
                  + ". Process ID: " + str(self.currentPCB.id) + " executed")
                
                if self.currentPCB.isEnded():
                    self.kernel.haltEND()
                    
            # If is to IO, dispatch interruption
            # TODO: IO instructions, hardware and interruptions 
        '''else:
            self.kernel.iOInstructionInterruption()'''
    
    def reset(self):
        self.setCurrentPCB(None)
        self.setIdle(True)
        
    def contextSwitch(self, aPCB):
        self.setCurrentPCB(aPCB)
        self.setIdle(False)
        
    def setCurrentPCB(self, newPCB):
        self.currentPCB = newPCB
        
    def getCurrentPCB(self):
        return self.currentPCB
        
    def setIdle(self, idle):
        self.idle = idle
        
        
        