'''
Created on 08/12/2012

@author: leandro
'''

from page_table import PageTable

class MMU:        
    def __init__(self, memory, hdd, page_table):
        self.memory = memory
        self.hdd = hdd
        self.table = page_table
        
    # Public interface
    
    def fetchInstruction(self, aPCBId, pc):
        page = pc / self.getLenBlock(aPCBId)
        desp = pc % self.getLenBlock(aPCBId)
        base = self.getPageTable().baseByPCBId(aPCBId, page)
        
        inst = self.getMemory().read(base + desp)
        
        return inst
    
    def swap(self):
        '''
        ¿No tiene parametros? 
        ¿Que hace?
        '''
        pass
    
    def kill(self, aPCBId):
        '''
        Delete a PCB from the page table by pcb id
        '''
        self.getPageTable().kill(aPCBId)
    
    def getLenPCB(self, aPCB):
        '''
        Ask to HDD for the length of a PCB
        '''
        return self.hdd.lenProgram(aPCB.getPath())
    
    # Abstract
    def addPCB(self, aPCB):
        '''
        Take a PCB and create its page on page table.
        After this try to load its instructions on memory
        '''
        program = self.getHDD().readProgram(aPCB.getPath())
        instrs = program.getInstructions()
        
        # create a new empty entry for a PCB, with its Pages
        self.getPageTable().addPCB(aPCB, self.numPagesFor(aPCB))
        
        # try to load pages on memory
        self.load(aPCB, instrs)

    # Protected Interface
    
    
    # Private Interface
    
    def numPagesFor(self, aPCB):
        '''
        This method must be implemented on a sub-class
        '''
        raise AbstractMethodException()
    
    def load(self, aPCB, instrs):
        '''
        This method must be implemented on a sub-class
        '''
        raise AbstractMethodException()
    
    def calcNumPages(self, aPCB):
        return self.numPagesFor(aPCB)
        
    # Getters and Setters
    
    def getMemory(self):
        return self.memory
    
    def setMemory(self, value):
        self.memory = value
        
    def getHDD(self):
        return self.hdd
    
    def setHDD(self, value):
        self.hdd = value
        
    def getPageTable(self):
        return self.page_table

    def setPageTable(self, value):
        self.page_table
        
# Sub-class of MMU

class Paginacion(MMU):
    def __init__(self, lenBlock, memory, hdd, page_table):
        MMU.__init__(self, memory, hdd, page_table)
        self.lenBlock = lenBlock
        
    def getLenBlock(self):
        '''
        Return the size of a page
        '''
        return self.lenBlock
    
    def calcNumPages(self, aPCB):
        '''
        return the number of pages needed to specific PCB
        '''
        self.getLenPCB(aPCB) / self.getLenBlock(aPCB) + 1
        
    def load(self, aPCB, insts):
        '''
        
        '''
        paged_instrs = self.page(insts)
        free_memory_pages = self.getFreeMemoryPages()
        
        virtual_paged_instrs = paged_instrs[:]
        
        for free_page in free_memory_pages:
            page = virtual_paged_instrs.pop(0)
            self.getPageTable().addPage(aPCB , paged_instrs.index(page) , free_page , len(page), False)
            self.load_on_memory(page, free_page)
            if(not virtual_paged_instrs):
                break
            
        for to_swapped_pages in virtual_paged_instrs:
            # Falta indicar que numero de pagina es y las instrucciones
            self.getHDD().swap_to_pcb(aPCB)
            
    def page(self, instrs):
        paged_instrs = []
        temp_page = []
        for instr in instrs:
            temp_page.append(instr)
            if(len(temp_page) == self.getLenBlock()):
                paged_instrs.append(temp_page)
                temp_page = []
                
        return paged_instrs
    
    def getFreeMemoryPages(self):
        all_table_units = self.getPageTable().getTable().values()
        all_tables_unit_pages = []
        for table_unit in all_table_units:
            all_tables_unit_pages.extend(table_unit.getPages().values())
            
        base_ocupied_pages = [ page.getBase() for page in all_tables_unit_pages if not page.swapped() ]
        all_base_memory_pages = self.getMemoryPagesBases()
        free_pages = [x for x in all_base_memory_pages if not (x in base_ocupied_pages)]
        return free_pages
    
    def getMemoryPagesBases(self):
        memory_size = self.getMemory().size()
        pages = memory_size / self.getLenBlock()
        return [ page * self.getLenBlock() for page in range(pages) ]
        
# Exceptions

class  AbstractMethodException(Exception):
    def __str__(self):
        return "This method must be implemented on sub-class"
