'''
Created on 21/09/2012

@author: MarianoLinares
'''

import time
import threading


class Clock:
    
    '''
    @args: interval is the time of a executing burst
    '''
    def __init__(self, interval, listeners):
        self.tick = 0
        self.listeners = listeners
        self.interval = interval
        self.run = True
        
        # Initial tick dispatch
        self.t = threading.Timer(self.interval, self.dispatchTick)
        self.t.start()
        
    def dispatchTick(self):
        # Re-Dispatch infinity ticks
        while self.run:
            
            self.tick += 1
    
            # Actions of Tick
            print("Tick: " + str(self.tick))
            
            # Dispatch ticks for all listeners
            for li in self.listeners:
                li.tick()

            # Wait for next tick
            time.sleep(self.interval)
        
    def stop(self):
        self.run = False
        

