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
        print("CPU idle: " + str(self.isIdle()))
        
        if self.kernel.thisIsTheEnd(): self.kernel.shutDown()
        
        # If is in UserMode and self is not idle, execute next instr        
        if (not self.kernel.isModeKernel()) and (not self.isIdle()):

            inst = self.currentPCB.getInstruction()
            
            # If is to CPU, execute
            if inst.isCPUInstruction():
                self.currentPCB.increasePC()
                
                # TODO: Log of actions
                print("Intruction " + str(self.currentPCB.pc)
                  + " of " + str(len(self.currentPCB.program.instructions))
                  + " of " + str(self.currentPCB.program.name)
                  + ". Process ID: " + str(self.currentPCB.getId()) + " executed in CPU")
                
                if self.currentPCB.isEnded():
                    self.kernel.haltEND()
                    
            # If is to IO, dispatch interruption 
            else:
                self.kernel.CPUioHALT()
    
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
    
    def isIdle(self):
        return bool(self.idle)
        
    def setIdle(self, idle):
        self.idle = bool(idle)
        
        
        