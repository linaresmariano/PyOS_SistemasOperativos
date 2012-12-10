'''
Created on 08/12/2012

@author: leandro
'''

from page_table import PageTable, SwappedPageException

class MMU:        
    
    def setKernel(self, kernel):
        self.kernel = kernel
        
    def __init__(self, memory, hdd, page_table):
        self.memory = memory
        self.hdd = hdd
        self.page_table = page_table
        
    # Public interface
    
    
#    def fetchInstruction(self, aPCBId, pc):
#        page = pc / self.getLenBlock(aPCBId)
#        desp = pc % self.getLenBlock(aPCBId)
#        try:
#            base = self.getPageTable().baseByPCBId(aPCBId, page)
#        except SwappedPageException:
#            self.unswap(aPCBId, page)
#            return self.fetchInstruction(aPCBId, pc)
#        inst = self.getMemory().read(base + desp)
#        
#        return inst
    
    def fetchInstruction(self, aPCB):
        pcb = aPCB
        pc = pcb.getPc()
        page = pc / self.getLenBlock()
        desp = pc % self.getLenBlock()
        try:
            base = self.getPageTable().getBase(aPCB, page)
        except SwappedPageException:
            self.unswap(aPCB, page)
            return self.fetchInstruction(aPCB, pc)
        inst = self.getMemory().read(base + desp)
        
#        return inst        
    
    def swap(self):
        '''
        Que hace
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
        
    def writeOnMemory(self, page, free_page_number):
        '''
        Write all instructions on 'page' from 'free_page_number'.
        If there are any data, this is overwrited.
        '''
        count = 0
        for inst in page:
            self.getMemory().write(free_page_number + count, inst)
            count += 1
        
        
        
class AsignacionContinua(MMU):
    def __init__(self, memory, hdd, page_table):
        MMU.__init__(self, memory, hdd, page_table)
        
    def load(self, aPCB, instrs):
        if (len(instrs) > len(self.getMemory().size())):
            raise ProgramTooLongException()
        table = self.getPagetable()
        table.addPCB(aPCB, self.numPagesFor(aPCB))
        base = self.getBaseFor(instrs)
        table.setPage(self, aPCB, 0, base, len(instrs), False)
        self.writeOnMemory(instrs, base)
        
    def getBaseFor(self,instrs):
        all_empty_cluster_lists = self.getEmptyClusters() # return a tuple (base,length) of the each free place
        all_empty_cluster_lists = [ list for list in all_empty_cluster_lists if list[1] >= len(instrs) ]
        
        the_first = all_empty_cluster_lists[0]
        sorted_lists = sorted(all_empty_cluster_lists , key = lambda list: list[1])
        the_best = sorted_lists.pop()
        the_worst = sorted_lists.pop(0)
        
        #Seleccionar cual!
        if the_first:
            return the_first
        elif the_worst:
            return the_worst
        elif the_best:
            return the_best
         
        #Si el espacio despues de compactar es suficiente, copacta y retorta la base que quedó
        place = self.placeAfterCompact()
        if (place >= len(instrs)):
            self.compact()
            return self.fisrtFreeClusterList()
        all_free_place = 0
        for place in self.getEmptyClusters():
            all_free_place += place[1]
            
        #Swappea procesos hasta tener el espacio suficiente
        while(all_free_place < len(instrs)):
            self.swapSomePCB()
            all_free_place = 0
            for place in self.getEmptyClusters():
                all_free_place += place[1]
                
        return self.fisrtFreeClusterList()
        
    def getLenBlock(self, aPCB):
        return self.getLenPCB(aPCB)

    def calcNumPages(self, aPCB):
        return 1
        
    def numPagesFor(self, aPCB):
        return self.calcNumPages(aPCB)
    
        
    def getLenPCB(self, aPCB):
        return self.hdd.lenProgram(aPCB.getPath())
        
# Sub-class of MMU

class Paginacion(MMU):
    def __init__(self, lenBlock, memory, hdd, page_table):
        MMU.__init__(self, memory, hdd, page_table)
        self.lenBlock = lenBlock
        
    def load(self, aPCB, insts):
        '''
        Try to associate a page of a process to a page in memory.
        If there is not place, the rest process pages are swapped.
        Precondition: have called addPCB() method of Table()
        '''
        paged_instrs = self.paginate(insts)
        free_memory_pages_bases = self.getFreeMemoryPagesBases()
        
        virtual_paged_instrs = paged_instrs[:]
        
        for free_page_base in free_memory_pages_bases:
            page = virtual_paged_instrs.pop(0)
            self.getPageTable().setPage(aPCB , paged_instrs.index(page) , free_page_base , len(page), False)
            self.writeOnMemory(page, free_page_base)
            if(not virtual_paged_instrs):
                break
            
        for to_swapped_pages in virtual_paged_instrs:
            self.getHDD().swapPageToPCB(aPCB, paged_instrs.index(to_swapped_pages), to_swapped_pages)
        
    def getLenBlock(self):
        '''
        Return the size of a page
        '''
        return self.lenBlock
    
    def calcNumPages(self, aPCB):
        '''
        return the number of pages needed to specific PCB
        '''
        return self.getLenPCB(aPCB) / self.getLenBlock() + 1
        
<<<<<<< HEAD
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
=======
    def numPagesFor(self, aPCB):
        return self.calcNumPages(aPCB)
>>>>>>> branch 'master' of git@github.com:infradosis/PyOS_SistemasOperativos.git
            
<<<<<<< HEAD
        for to_swapped_pages in virtual_paged_instrs:
            # Falta indicar que numero de pagina es y las instrucciones
            self.getHDD().swap_to_pcb(aPCB)
            
    def page(self, instrs):
=======
    def paginate(self, instrs):
        '''
        Make a list of instructions to a list of list of instructions, 
        the length each list of instructions is the length of a page. 
        '''
>>>>>>> branch 'master' of git@github.com:infradosis/PyOS_SistemasOperativos.git
        paged_instrs = []
        temp_page = []
        for instr in instrs:
            temp_page.append(instr)
            if(len(temp_page) == self.getLenBlock()):
                paged_instrs.append(temp_page)
                temp_page = []
                
        if(len(temp_page) > 0):
            paged_instrs.append(temp_page)        
        
        return paged_instrs
    
    def getFreeMemoryPagesBases(self):
        '''
        Return the free pages on memory
        '''
        all_table_units = self.getPageTable().getTable().values()
        all_tables_unit_pages = []
        for table_unit in all_table_units:
            all_tables_unit_pages.extend(table_unit.getPages().values())
            
        base_ocupied_pages = [ page.getBase() for page in all_tables_unit_pages if not page.isSwapped() ]
        all_base_memory_pages = self.getMemoryPagesBases()
        free_pages = [x for x in all_base_memory_pages if not (x in base_ocupied_pages)]
        return free_pages
    
    def getMemoryPagesBases(self):
        '''
        return all bases to a specific memory size
        '''
        memory_size = self.getMemory().size()
        pages = memory_size / self.getLenBlock()
        return [ page * self.getLenBlock() for page in range(pages) ]
         
    
    def unswap(self, aPCB, page_number):
        '''
        Load in memory the page that is in HDD.
        '''
        instrs = self.getHDD().getSwappedPage(aPCB, page_number)
        free_memory_page = self.getForcedFreePage()
        self.getPageTable().setPage(aPCB, page_number, free_memory_page, len(instrs), False)
        self.writeOnMemory(instrs, free_memory_page)
        
    def getForcedFreePage(self):
        '''
        if there is any free page on memory, return it. unless,
        swap some page of some pcb and returns its memory page.
        '''
        free_bases = self.getFreeMemoryPagesBases()
        if not free_bases:
            self.swapSomePCB()
            free_bases = self.getFreeMemoryPagesBases()
            
        return free_bases[0] 
    
    def swapSomePCB(self):
        '''
        swap some pcb (should be like 'banquero') and return this free page
        '''
        all_process = self.getPageTable().keys()
         
        
        for process in all_process:
            if not self.getPageTable().isBlocked(process):
                table_unit = self.getPageTable().getTable()[process]
                no_swapped_pages_number = [ page_number for page_number in table_unit.getPages().keys() if not table_unit.isSwapped(page_number) ]
                page_number = no_swapped_pages_number[0]
                page = table_unit.getPages()[page_number]
                base = page.getBase()
                limit = page.getLimit()
                table_unit.swap(page_number)
                instrs = [ self.getMemory().read(base + ints_index) for ints_index in range(limit) ]
                self.getHDD().swapPageToPCB(process, page_number, instrs)
                return base
            
        raise Exception("Maybe this is a bug")        
    
# Exceptions

class AbstractMethodException(Exception):
    def __str__(self):
        return "This method must be implemented on sub-class"

class ProgramTooLongException(Exception):
    def __str__(self):
        return "This program is too long to be executed"
