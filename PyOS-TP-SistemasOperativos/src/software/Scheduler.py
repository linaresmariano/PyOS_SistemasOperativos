'''
Created on 21/09/2012

@author: MarianoLinares
'''

from software.PCB import PriorityPCB

class Scheduler:

    #Dispatcher operations
    def contextSwitch(self):
        
        # Save the old PCB
        if not self.cpu.idle:
            oldPCB = self.cpu.getCurrentPCB()
            self.addPCB(oldPCB)

        # Reset cpu
        self.cpu.reset()
        
        # Select and switch the new PCB 
        if self.isThereAReadyProcess():
            newPCB = self.getNextPCB()
            self.cpu.contextSwitch(newPCB)

    # Add a PCB in the readyQueue       
    def addPCB(self, aPCB):
        self.readyQueue.append(aPCB)
        
    def isThereAReadyProcess(self):
        return bool(self.readyQueue)
    
    # Used in RR strategy
    def tick(self):
        pass
    
    def restartQuantum(self):
        pass


class FIFO(Scheduler):
    def __init__(self, aKernel):
        self.cpu = aKernel.cpu
        self.readyQueue = []

    # Prec: readyQueue has at least one element 
    def getNextPCB(self):
        if self.readyQueue:
            ret = self.readyQueue[0]
            del self.readyQueue[0]
            return ret

class RR(FIFO):
    def __init__(self, aKernel, quantum):
        self.kernel = aKernel
        self.cpu = aKernel.cpu
        self.readyQueue = []
        self.quantum = quantum
        self.partial = 0

    def tick(self):
        self.partial += 1
        if(self.quantum == self.partial):
            self.kernel.TIMEoutHALT()
            
    def restartQuantum(self):
        self.partial = 0
    

class PRIO(Scheduler):
    def __init__(self, aKernel):
        self.cpu = aKernel.cpu
        self.readyQueue = []

    def addPCB(self, aPCB):
        self.readyQueue.append(PriorityPCB(aPCB))

    # Returns the highest priority process. Partial operation, must be a ready process
    def getNextPCB(self):
        retPCB = self.readyQueue[0]
        for i in self.readyQueue:
            if i.isLower(retPCB):
                retPCB = i
        
        self.readyQueue.remove(retPCB)
        
        return retPCB.pcb
        
        
