'''
Created on 21/09/2012

@author: MarianoLinares
'''

class Timer:

    def __init__(self, listen, scheduler):
        self.listeners = listen
        self.quantum = 0
        self.scheduler = scheduler
        
    def tick(self):
        # Increment quantum
        self.setQuantum(self.getQuantum() + 1)
        
        self.scheduler.seeQuantum(self.quantum)

        # Dispatch ticks for all listeners
        for li in self.listeners:
            li.execute()
        
    def setQuantum(self, quant):
        self.quantum = quant
        
    def getQuantum(self):
        return self.quantum
        
    def restartQuantum(self):
        self.setQuantum(0)
        
    