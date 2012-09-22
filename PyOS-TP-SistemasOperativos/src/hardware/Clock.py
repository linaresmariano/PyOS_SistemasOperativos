'''
Created on 21/09/2012

@author: MarianoLinares
'''

#import time
import threading


class Clock:
    
    '''
    @args: lapse is the time of a executing burst
    '''
    def __init__(self, interval, listeners):
        self.tick = 0
        self.listeners = listeners
        self.interval = interval
        
        # Initial tick dispatch
        self.dispatchTick()
        
    def dispatchTick(self):
        
        self.tick += 1

        # Actions of Tick
        print("Tick: " + str(self.tick))
        
        # Dispatch ticks for all listeners
        for li in self.listeners:
            li.execute()

        # Re-Dispatch infinity ticks
        self.t = threading.Timer(self.interval, self.dispatchTick).start()

