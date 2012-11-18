'''
Created on 15/11/2012

@author: mariano
'''

class Memory():
    '''
    # Cluster (bool, data)
            0 - bool -> cluster in use
            1 - data -> data (instruction)
    '''
    def __init__(self, size):
        cluster = {"inUse": False, "data": None}
        self.clusters = [cluster] * size

    def read(self, index):
        return self.getClusters()[index]["data"]
    
    def write(self, index, value):
        self.getClusters()[index]["data"] = value
        
    def setInUse(self, index, inUse):
        self.getClusters()[index]["inUse"] = inUse

    def getClusters(self):
        return self.clusters