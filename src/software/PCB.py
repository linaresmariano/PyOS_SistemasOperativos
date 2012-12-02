'''
Created on 21/09/2012

@author: MarianoLinares
'''

class PCB:

    def __init__(self, PCBID, pathProgram, length):
        self.id = PCBID
        self.state = "ready"
        self.pc = 0
        self.path = pathProgram
        self.length = length
    
    def increasePC(self):
        self.pc += 1
        
    def isEnded(self):
        # Returns 'true' if PC of currentPCB is higher than length of pcb instructions
        return self.length <= self.pc
    
    def getId(self):
        return self.id
    
    def getPath(self):
        return self.path
    
    def getPc(self):
        return self.pc



class PriorityPCB:

    def __init__(self, aPCB):
        self.pcb = aPCB
        # While less instructions, more priority
        self.priority = aPCB.length
    
    def isLower(self, aPCBWP):
        return self.priority < aPCBWP.priority
        
    def toGrowOld(self):
        self.priority -= 10




