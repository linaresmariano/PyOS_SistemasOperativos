'''
Created on 06/10/2012

@author: MarianoLinares
'''

from hardware.Clock import Clock

class IO:
    def __init__(self, time):
        self.clock = Clock(time, [self])  # Start clock
        self.kernel = None
        self.readyQueue = []
        self.currentPCB = None
    
    def setKernel(self, aKernel):
        self.kernel = aKernel

    def addPCB(self, aPCB):
        self.readyQueue.append(aPCB)

    def tick(self):

        if not self.currentPCB and self.readyQueue:
            self.currentPCB = self.readyQueue[0]
            del self.readyQueue[0]
        
        # If is in UserMode and self is not idle, execute next instr   
        if ((not self.kernel.isModeKernel()) and bool(self.currentPCB)):

            # Increments PC (execute intruction)
            self.currentPCB.increasePC()

                # TODO: Log of actions
            '''print("Intruction " + str(self.currentPCB.pc)
                  + " of " + str(len(self.currentPCB.program.instructions))
                  + " of " + str(self.currentPCB.program.name)
                  + ". Process ID: " + str(self.currentPCB.getId()) + " executed in IO")'''
            
            # If program ends of execute, notify to kernel
            if self.currentPCB.isEnded():
                self.kernel.IOfinHALT()
            else:
                # If is to CPU, dispatch interruption 
                self.kernel.IOcpuHALT()
                
                
    def getCurrentPCB(self):
        ret = self.currentPCB
        self.reset()
        return ret
    
    def reset(self):
        self.currentPCB = None
        
    def isIdle(self):
        return not (self.currentPCB or self.readyQueue)
    
    def stop(self):
        self.clock.stop()

            
            
            
            