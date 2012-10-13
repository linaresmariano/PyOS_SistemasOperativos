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
    def execute(self):
        print("CPU idle: " + str(self.idle))
        
        # If is in UserMode and self is not idle, execute next instr        
        if (not self.kernel.modeKernel) and (not self.idle):
            
            if (not self.currentPCB.isEnded()):
                inst = self.currentPCB.getInstruction()
                
                if inst.isCPUInstruction():
                    self.currentPCB.increasePC()
                    
                    # TODO: Log to action
                    print("Intruction " + str(self.currentPCB.pc)
                      + " of " + str(len(self.currentPCB.program.instructions))
                      + " of " + str(self.currentPCB.program.name)
                      + ". Process ID: " + str(self.currentPCB.id) + " executed")
                    
                '''else:
                    self.kernel.iOInstructionInterruption()'''
            else:
                self.kernel.haltEND()
            


        '''
        
        if not self.kernel.modeKernel and not self.idle:
            
            print(str(self.currentPCB.pc))
            
            # TODO: see if it's to CPU
            self.currentPCB.executeInstruction()
            
            
            
            print("Intruction " + str(self.currentPCB.pc)
                  + " of " + str(len(self.currentPCB.program.instructions))
                  + " of " + str(self.currentPCB.program.name)
                  + ". Process ID: " + str(self.currentPCB.id) + " executed")'''
    
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
        
        
        