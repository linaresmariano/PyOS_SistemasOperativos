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
        
        return inst        
    
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
        Take a PCB and create its pages on page table.
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
        #Si hay más instrucciones que espacio total de la memoria, Se lanza una excepcion
        if (len(instrs) > len(self.getMemory().size())):
            raise ProgramTooLongException()
        
        table = self.getPagetable()
        #El metodo 'getBaseFor(instrs)' debe ser el Primer, mejor o peor ajuste
        base = self.getBaseFor(instrs)
        
        #Settea la unica pagina de la tabla. (PCB, numero_de_pagina,base,limit,Sswapped)
        table.setPage(aPCB, 0, base, len(instrs), False)
        self.writeOnMemory(instrs, base)
        
    def getBaseFor(self,instrs):
        '''
        Este metodo usa 'getBaseByEstrategy(instruciones)' en parte para devolver una
        posible Base segun la estrategia de 'fit'.
        '''
        '''
        < === Desde aca === >
        '''
        # should return a tuple (base,length) of the each free place
        all_empty_free_places = self.getEmptyClusters()
        
        #Tomo solo los espacion que sean mayores o iguales a el espacio necesario
        #  por el largo de las instrucciones
        all_empty_free_places = [ list for list in all_empty_free_places if list[1] >= len(instrs) ]
        
        if not all_empty_free_places:
            the_first = all_empty_free_places[0] # Tomo el primer espacio valido (first fit)
        
            #Ordeno la lista, de menor a mayor
            sorted_lists = sorted(all_empty_free_places , key = lambda list: list[1])
            #Tomo el mejor ajuste(el primero ya que es el menor)
            the_best = sorted_lists.pop(0)
            #Tomo el peor, ya que el ultimo es el más grande
            the_worst = sorted_lists.pop()
        
            #Seleccionar cual! Yo retorno el primero
            return the_first
        '''
        
        Es cosa de un medoto 'self.getBaseByEstrategy()'
        Que debe retornar la base segun la estrategia.
        Si no hubiera, retorna nil.
        
        < === Hasta aca === >
        '''
        #descomentar este codigo despues de implementar 'self.getBaseByEstrategy(instruciones)':
        
#        base = self.getBaseFor(instrs)
#        if base:
#            return base 
        
         
        #Si no hay un bloque que se pueda usar, miro cuanto es la suma de los espacios vacio.
        # Si esa suma (free_place_size) es mayor o igual al largo de las instrucciones, entonces
        # compacto y tomo la primera base libre
        free_place_size = self.allFreePlace() #Retorna la cantidad total de espacio libre
        
        #Compacto y retorno la primera base
        if (free_place_size >= len(instrs)): 
            self.compact()
            return self.firstFreePlace()
        
        #Empizo a swappear otros procesos hasta que el espacio sea suficiente
        
        # 'all_free_place' = todo el espacio libre hasta ahora (igual a  a 'free_place_size') 
        all_free_place = self.allFreePlace()
            
        #Mientras no tenga espacio para poner el Proceso, swappeo otros procesos
        while(all_free_place < len(instrs)):
            self.swapSomePCB()
            all_free_place = self.AllFreePlace()
                
        return self.allFreePlace()
    
    '''
    To Do List:
        self.getEmptyClusters()
        #Debe retornar tuplas (base,largo), donde la base es donde empiza un bloque vacio de memoria
        # y largo es cuanto espacio vacio desde esa base, mapeando toda la memoria
        
        self.allFreePlace()
        #Debe retornar la suma de todos los espacio vacios en memoria
        # hit: podria usarse el metodo anterior ;)
        
        self.firstFreePlace()
        #Debe retornar la primer base libre
        
        self.getBaseByEstrategy(instruciones)
        #Que debe retornar la base segun la estrategia.
        #Si no hubiera, retorna nil.
    
    
    '''
        
    def getLenBlock(self, aPCB):
        return self.getLenPCB(aPCB)

    def calcNumPages(self, aPCB):
        return 1
        
    def numPagesFor(self, aPCB):
        return self.calcNumPages(aPCB)
    
        
    def getLenPCB(self, aPCB):
        return self.hdd.lenProgram(aPCB.getPath())
        
# Sub-class of MMU

'''
To Do List:
    test it!

'''

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
        #self.page(instrs)Divide un conunto de instruciones en conjuntos mas chicos de tamaño de pagina
        # Ej.: con una lista de 30 instruciones, si la pagina tiene tamaño 10, este metodo
        #  generará una lista con 3 listas de instruciones: [Instruciones * 30] => [ [Inst* 10],[Inst* 10],[Inst* 10] ]
        paged_instrs = self.page(insts)
        
        #Mapea toda la memoria, buscando todos las bases libre
        free_memory_pages_bases = self.getFreeMemoryPagesBases()
        
        #Se hace una copia, para luego saber el index de la pagina
        virtual_paged_instrs = paged_instrs[:]
        
        #Por cada pagina libre, se le asigna un bloque de las instrucciones
        for free_page_base in free_memory_pages_bases:
            #Obtengo el primer bloque de instrucciones
            page = virtual_paged_instrs.pop(0)
            #Seteo la pagina de la Page table
            self.getPageTable().setPage(aPCB , paged_instrs.index(page) , free_page_base , len(page), False)
            self.writeOnMemory(page, free_page_base)
            
            #si no tengo más bloques q asignar, se sale del loop
            if(not virtual_paged_instrs):
                break
            
        #Si quedo algo sin asignar, lo swapeo a disco
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
        
    def numPagesFor(self, aPCB):
        return self.calcNumPages(aPCB)
            
    def page(self, instrs):
        '''
        Divide un conjunto de instruciones en bloques del tamaño de pagina
        '''
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
        #Obtengo todas las unidades de tabla
        all_table_units = self.getPageTable().getTable().values()
        #Ahora todas las paginas de esas Unidades de tabla
        all_tables_unit_pages = []
        for table_unit in all_table_units:
            all_tables_unit_pages.extend(table_unit.getPages().values())
        #De esas paginas, me quedo con las Bases las que ocupadas (no estan swapeadas a disco)
        base_ocupied_pages = [ page.getBase() for page in all_tables_unit_pages if not page.isSwapped() ]
        
        #Tomo todas las bases de la memoria
        all_base_memory_pages = self.getMemoryPagesBases()
        
        #Me quedo con todas las bases de la memoria que no esten entre las bases que estan ocupadas
        # Algo asi como: lista_de_bases_totales - lista_de_bases_ocupadas = lista_de_bases_libres
        free_pages = [x for x in all_base_memory_pages if not (x in base_ocupied_pages)]
        return free_pages
    
    def getMemoryPagesBases(self):
        '''
        return all bases to a specific memory size
        '''
        memory_size = self.getMemory().size()
        #Cantidad de paginas en memoria
        canti_pages = memory_size / self.getLenBlock()
        
        #retora una lista de todas las bases de memoria
        # por cada cada numero en el rango 1..cantidad_de_paginas, multiplicado por 
        # el tamaño del pagina.
        return [ page * self.getLenBlock() for page in range(canti_pages) ]
         
    
    def unswap(self, aPCB, page_number):
        '''
        Load in memory the page that is in HDD.
        '''
        #Si hay una pagina libre, la retorna, sino swapea algun proceso y retorna
        # la base que quedo libre.
        # Debe actualizar la tabla respecto a ese proceso que se saco de memoria
        free_memory_page = self.getForcedFreePage()
        
        #Obtiene las instruciones a cargar en memoria
        instrs = self.getHDD().getSwappedPage(aPCB, page_number)
        #Settea la pagina del PCB 
        self.getPageTable().setPage(aPCB, page_number, free_memory_page, len(instrs), False)
        self.writeOnMemory(instrs, free_memory_page)
        
    def getForcedFreePage(self):
        '''
        if there is any free page on memory, return it. unless,
        swap some page of some pcb and returns its memory page.
        '''
        free_bases = self.getFreeMemoryPagesBases()
        if not free_bases:
            #Swapea algun PCb y acualiza la tabla
            self.swapSomePCB()
            free_bases = self.getFreeMemoryPagesBases()
            
        return free_bases[0] 
    
    def swapSomePCB(self):
        '''
        swap some pcb (should be like 'banquero') and return this free page
        '''
        #Obtiene todos los PCBs
        all_process = self.getPageTable().keys()
         
        # (1) Si no está bloqueado, obtiene la unidad de tabla del proceso.
        # (2) Luego recorre sus paginas hasta obtener una q no esté swapeada
        # (3) le saca la base, el limite y la setea como swapeada.
        # (4) toma las instruciones de memoria y las swapea
        # retorna la base
        for process in all_process:
            if not self.getPageTable().isBlocked(process): # (1)
                table_unit = self.getPageTable().getTable()[process]
                no_swapped_pages_number = [ page_number for page_number in table_unit.getPages().keys() # (2) 
                                           if not table_unit.isSwapped(page_number) ]
                page_number = no_swapped_pages_number[0] #Supone que al menos una estará libre
                page = table_unit.getPages()[page_number]
                base = page.getBase() # (3)
                limit = page.getLimit() # (3)
                table_unit.swap(page_number) # (3)
                instrs = [ self.getMemory().read(base + ints_index) for ints_index in range(limit) ]# (4) 
                self.getHDD().swapPageToPCB(process, page_number, instrs)# (4) 
                return base# (5)
            
        raise Exception("Maybe this is a bug")        
    
# Exceptions

class AbstractMethodException(Exception):
    def __str__(self):
        return "This method must be implemented on sub-class"

class ProgramTooLongException(Exception):
    def __str__(self):
        return "This program is too long to be executed"
