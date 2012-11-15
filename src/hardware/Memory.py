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
        self.clusters = []
        cluster = [False, None]
        for _ in range(0, size):
            self.clusters.append(cluster)
    
    def read(self, index):
        return self.getClusters()[index][1]
    
    def write(self, index, value):
        self.getClusters()[index][1] = value
        
    def setInUse(self, index, inUse):
        self.getClusters()[index][0] = inUse
    
    def getClusters(self):
        return self.clusters