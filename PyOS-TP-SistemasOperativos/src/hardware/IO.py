'''
Created on 06/10/2012

@author: MarianoLinares
'''

class IO:
    def __init__(self, aKernel):
        self.kernel = aKernel
        self.readyQueue = []
        self.currentPCB = None
    
    def addPCB(self, aPCB):
        self.readyQueue.append(aPCB)

    def tick(self):

        if not self.currentPCB and self.readyQueue:
            self.currentPCB = self.readyQueue[0]
            del self.readyQueue[0]
        
        # If is in UserMode and self is not idle, execute next instr   
        if (not self.kernel.modeKernel) and self.currentPCB:
            
            inst = self.currentPCB.getInstruction()

            # If is to CPU, execute
            if inst.isIOInstruction():
                # Increments PC (execute intruction)
                self.currentPCB.increasePC()

                # TODO: Log of actions
                print("Intruction " + str(self.currentPCB.pc)
                  + " of " + str(len(self.currentPCB.program.instructions))
                  + " of " + str(self.currentPCB.program.name)
                  + ". Process ID: " + str(self.currentPCB.id) + " executed in IO")

                if self.currentPCB.isEnded():
                    self.kernel.IOfinHALT()
                
            # If is to IO, dispatch interruption 
            else:
                self.kernel.IOcpuHALT()
                
                
    def getCurrentPCB(self):
        ret = self.currentPCB
        self.reset()
        return ret
    
    def reset(self):
        self.currentPCB = None
        
    def isIdle(self):
        return not (self.currentPCB or self.readyQueue)

            
            
            
            