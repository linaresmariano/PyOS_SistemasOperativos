'''
Created on 17/11/2012

@author: mariano
'''

class HDD(object):
    
    def __init__(self):
        self.programs = []

    '''
    @raise InvalidPath: raised when path is invalid
    @param path: the path of the program that we want read
    @return: return the program with path "path"
    '''
    def readProgram(self, path):
        for p in self.getPrograms():
            if p.getPath() == path:
                return p

        raise InvalidPath()
  
  
    '''
    @precondition: "path" is a valid path 
    '''
    def lenProgram(self, path):
        for p in self.getPrograms():
            if p.getPath() == path:
                return len(p)



class InvalidPath(Exception):
    def __str__(self):
        return 'InvalidPath'