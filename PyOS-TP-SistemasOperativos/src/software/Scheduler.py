'''
Created on 21/09/2012

@author: MarianoLinares
'''

class Scheduler:

    #Dispacher operations
    def contextSwitch(self):
        #if there are any process on ready to execute, then take out the 
        #  process on the CPU and puts the selected process, else only
        #  take out the process from the CPU
        
        if not self.cpu.idle:
            # Save the old pcb
            oldPCB = self.cpu.getCurrentPCB()
            self.addPCB(oldPCB)

        self.cpu.reset()
        
        print(len(self.readyQueue))
        
        if self.isThereAReadyProcess():
            newPCB = self.getNextPCB()
            self.cpu.contextSwitch(newPCB)


class FIFO(Scheduler):
    def __init__(self, aKernel):
        self.cpu = aKernel.cpu
        self.readyQueue = []
    
    def addPCB(self, aPCB):
        self.readyQueue.append(aPCB)

    # Prec: readyQueue has at least one element 
    def getNextPCB(self):
        if self.readyQueue:
            ret = self.readyQueue[0]
            del self.readyQueue[0]
            return ret
        
    def isThereAReadyProcess(self):
        return bool(self.readyQueue)

class RR(Scheduler):
    def __init__(self, aKernel, quantum):
        self.cpu = aKernel.cpu
        self.readyQueue = []
        self.quantum = quantum
    
    def addPCB(self, aPCB):
        self.readyQueue.append(aPCB)

    # TODO: dequeue readyPCB returned
    # prec: readyQueue has at least one element 
    def getNextPCB(self):
        if self.readyQueue:
            ret = self.readyQueue[0]
            del self.readyQueue[0]
            return ret
        
    def isThereAReadyProcess(self):
        return bool(self.readyQueue)
    
    
'''
class Prioridad(Scheduler):
    def __init__(self):
        Scheduler.__init__(self)

    def addPCB(self, aPCB):
        self.readyQueue(PCBWPriority(aPCB))
  
    def nextPCB(self):
        maxPriority = self.readyQueue[0]
        for p in self.readyQueue:
            if p.priority > maxPriority.priority:
                maxPriority = p
        return maxPriority'''