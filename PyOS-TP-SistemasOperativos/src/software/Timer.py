'''
Created on 21/09/2012

@author: MarianoLinares
'''

class Timer:

    def __init__(self, listen):
        self.listeners = listen
        self.quantum = 0
        
    def tick(self):
        # Dispatch ticks for all listeners
        for li in self.listeners:
            li.execute()
                
        self.quantum += 1
        print("quantum: " + str(self.quantum))
        
    def setQuantum(self, quant):
        self.quantum = quant
        
    