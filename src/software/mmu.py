'''
Created on 08/12/2012

@author: leandro
'''

from page_table import PageTable

class MMU:
    def __init__(self):
        self.page_table = PageTable()
        
    def getInstruction(self, aPCBId):
        pass
    
    def load(self, aPCB):
        pass
    
    def fetchInstruction(self, aPCBId, pc):
        pass
    
    def calculateDM(self,aPCBId, index):
        pass
    
    def swap(self):
        pass
    
    def addPCB(self,aPath):
        pass
    
    def kill(self,aPCBId):
        pass
        
