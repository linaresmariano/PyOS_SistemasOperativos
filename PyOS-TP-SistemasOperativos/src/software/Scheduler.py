'''
Created on 21/09/2012

@author: MarianoLinares
'''

class FIFO:
    def __init__(self):
        self.readyQueue = [] 
    
    def addPCB(self, aPCB):
        self.readyQueue.append(aPCB)

    # TODO: dequeue readyPCB returned
    # prec: readyQueue has at least one element 
    def nextPCB(self):
        if self.readyQueue:
            ret = self.readyQueue[0]
            del self.readyQueue[0]
            return 

        return False

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