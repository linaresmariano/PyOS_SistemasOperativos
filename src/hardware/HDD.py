'''
Created on 17/11/2012

@author: mariano
'''

class HDD(list):

    def readProgram(self, path):
        '''
        @raise InvalidPath: raised when path is invalid
        @param path: the path of the program that we want to read
        @return: the program with path "path"
        '''
        for p in self:
            if p.getPath() == path:
                return p

        raise InvalidPath()
  
  
    def lenProgram(self, path):
        '''
        @precondition: "path" is a valid path 
        '''
        for p in self:
            if p.getPath() == path:
                return p.length()


class InvalidPath(Exception):
    def __str__(self):
        return 'InvalidPath'
