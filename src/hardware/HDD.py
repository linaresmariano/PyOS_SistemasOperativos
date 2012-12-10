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
            
    def swapPageToPCB(self, aPCB, page_number, instrs):
        '''
        Create a new swapped pages process unit, to save the 
        swapped pages on HDD.
        If the unit already exist, only add the page to it.
        '''
        swapped_pages_of_process = None
        for x in self:
            if(x.getPath() == aPCB):
                swapped_pages_of_process = x
                break
        if swapped_pages_of_process:
            swapped_pages_of_process.addPage(page_number, instrs)
            return
            
        mock_prog = MockProgramToSwap(aPCB, page_number, instrs)
        self.append(mock_prog)
        
    def getSwappedPage(self, pcb, page_number):
        '''
        Return a swapped page of a pcb, by a specific page
        number. 
        '''
        elm = None
        for elem in self:
            if elem.getPath() == pcb:
                elm = pcb
        if not elm:
            raise NoSwappedPageException()
        return elm.getPageNumbers(page_number)
        
class MockProgramToSwap():
    '''
    Represent a False place where is saved the swapped page of a 
    pcb.
    '''
    def __init__(self, aPCB, page_number, instrs):
        self.mock_path = aPCB
        self.page_numbers = {}
        
    def getPath(self):
        return self.mock_path
        
    def getPageNumbers(self):
        return self.page_numbers
    
    def addPage(self, page_number, instrs):
        self.page_numbers[page_number] = instrs
        
    def getPage(self, page_number):
        return self.getPageNumbers()[page_number]
    
    def popPage(self,page_number):
        page = self.getPageNumbers()[page_number]
        del(self.getPageNumbers()[page_number])
        return page
        
    

class InvalidPath(Exception):
    def __str__(self):
        return 'InvalidPath'

class NoSwappedPageException(Exception):
    def __str__(self):
        return "No Swapped Page"
