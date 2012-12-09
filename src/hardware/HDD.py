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
            
    def swap_to_pcb(self,aPCB,page_number,intrs):
        mock_prog = MockProgramToSwap(aPCB,page_number,intrs)
        self.append(mock_prog)
        
    def get_swapped_page(self,pcb,page_number):
        elm = None
        for elem in self:
            if elem.getPath() == pcb:
                elm = pcb
        if elm == None:
            raise NoSwappedPageException()
        return elm.getPageNumbers()[page_number]
        
class MockProgramToSwap():
    def __init__(self,aPCB,page_number,instrs):
        self.mock_path = aPCB
        self.page_numbers = {}
        
    def getPath(self):
        return self.mock_path
        
    def getPageNumbers(self):
        return self.page_numbers
    

class InvalidPath(Exception):
    def __str__(self):
        return 'InvalidPath'

class NoSwappedPageException(Exception):
    def __str__(self):
        return "No Swapped Page"