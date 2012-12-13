'''
Created on 08/12/2012

@author: leandro
'''

from page_table import SwappedPageException

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
        page = pc / self.getLenBlock(aPCB)
        desp = pc % self.getLenBlock(aPCB)
        try:
            base = self.getPageTable().getBase(aPCB, page)
        except SwappedPageException:
            self.unswap(aPCB, page)
            return self.fetchInstruction(aPCB, pc)
        inst = self.getMemory().read(base + desp)
        
        return inst        
    
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
        
        # create a new empty entry for a PCB, with its number of pages
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
    
    def writeOnMemory(self, page, free_page_number):
        '''
        Write all instructions on 'page' from 'free_page_number'.
        If there are any data, this is overwrited.
        '''
        count = 0
        for inst in page:
            index = free_page_number + count
            self.getMemory().write(index, inst)
            self.getMemory().setInUse(index, True)
            count += 1
            
    def swapSomePCB(self):
        '''
        swap some pcb (should be like 'banquero') and return this free page
        '''
        # Obtiene todos los PCBs
        all_process = self.getPageTable().getTable().keys()
         
        # (1) Si no esta bloqueado, obtiene la unidad de tabla del proceso.
        # (2) Luego recorre sus paginas hasta obtener una q no este swapeada
        # (3) le saca la base, el limite y la setea como swapeada.
        # (4) toma las instruciones de memoria y las swapea
        # (5) retorna la base
        for process in all_process:
            if not self.getPageTable().isBlocked(process):  # (1)
                table_unit = self.getPageTable().getTable()[process]
                no_swapped_pages_number = [ page_number for page_number in table_unit.getPages().keys()  # (2) 
                                           if not table_unit.isSwapped(page_number) ]
                if len(no_swapped_pages_number) == 0:
                    continue
                page_number = no_swapped_pages_number[0]  # Supone que al menos una estara libre
                page = table_unit.getPages()[page_number]
                base = page.getBase()  # (3)
                limit = page.getLimit()  # (3)
                table_unit.swap(page_number)  # (3)
                instrs = [ self.getMemory().read(base + ints_index) for ints_index in range(limit) ]  # (4) 
                self.getHDD().swapPageToPCB(process, page_number, instrs)  # (4) 
                for ints_index in range(limit):
                    self.getMemory().setInUse(base + ints_index,False)  
                return base  # (5)
            
        raise Exception("Maybe this is a bug") 
    
        
        
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
        # self.page(instrs)Divide un conunto de instruciones en conjuntos mas chicos de tamanho de pagina
        # Ej.: con una lista de 30 instruciones, si la pagina tiene tamanho 10, este metodo
        #  generara una lista con 3 listas de instruciones: [Instruciones * 30] => [ [Inst* 10],[Inst* 10],[Inst* 10] ]
        paged_instrs = self.pagimate(insts)
        
        # Mapea toda la memoria, buscando todos las bases libre
        free_memory_pages_bases = self.getFreeMemoryPagesBases()
        
        # Se hace una copia, para luego saber el index de la pagina
        virtual_paged_instrs = paged_instrs[:]
        
        # Por cada pagina libre, se le asigna un bloque de las instrucciones
        for free_page_base in free_memory_pages_bases:
            # Obtengo el primer bloque de instrucciones
            page = virtual_paged_instrs.pop(0)
            # Seteo la pagina de la Page table
            self.getPageTable().setPage(aPCB , paged_instrs.index(page) , free_page_base , len(page), False)
            self.writeOnMemory(page, free_page_base)
            
            # si no tengo mas bloques q asignar, se sale del loop
            if(not virtual_paged_instrs):
                break
            
        # Si quedo algo sin asignar, lo swapeo a disco
        for to_swapped_pages in virtual_paged_instrs:
            self.getHDD().swapPageToPCB(aPCB, paged_instrs.index(to_swapped_pages), to_swapped_pages)
        
    def getLenBlock(self, aPCB=None):
        '''
        Return the size of a page
        '''
        return self.lenBlock
    
    def calcNumPages(self, aPCB):
        '''
        return the number of pages needed to specific PCB
        '''
        return (self.getLenPCB(aPCB) / self.getLenBlock()) + 1
        
    def numPagesFor(self, aPCB):
        return self.calcNumPages(aPCB)
            
    def pagimate(self, instrs):
        '''
        Divide un conjunto de instruciones en bloques del tamanho de pagina
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
        # Obtengo todas las unidades de tabla
        all_table_units = self.getPageTable().getAllTableUnits()
        # Ahora todas las paginas de esas Unidades de tabla
        all_tables_unit_pages = []
        for table_unit in all_table_units:
            all_tables_unit_pages.extend(table_unit.getAllPages())
        # De esas paginas, me quedo con las Bases las que ocupadas (no estan swapeadas a disco)
        base_ocupied_pages = [ page.getBase() for page in all_tables_unit_pages if not page.isSwapped() ]
        
        # Tomo todas las bases de la memoria
        all_base_memory_pages = self.getMemoryPagesBases()
        
        # Me quedo con todas las bases de la memoria que no esten entre las bases que estan ocupadas
        # Algo asi como: lista_de_bases_totales - lista_de_bases_ocupadas = lista_de_bases_libres
        free_pages = [x for x in all_base_memory_pages if not (x in base_ocupied_pages)]
        return free_pages
    
    def getMemoryPagesBases(self):
        '''
        return all bases to a specific memory size
        '''
        memory_size = self.getMemory().size()
        # Cantidad de paginas en memoria
        canti_pages = memory_size / self.getLenBlock()
        
        # retora una lista de todas las bases de memoria
        # por cada cada numero en el rango 1..cantidad_de_paginas, multiplicado por 
        # el tamanho del pagina.
        return [ page * self.getLenBlock() for page in range(canti_pages) ]
         
    
    def unswap(self, aPCB, page_number):
        '''
        Load in memory the page that is in HDD.
        '''
        # Si hay una pagina libre, la retorna, sino swapea algun proceso y retorna
        # la base que quedo libre.
        # Debe actualizar la tabla respecto a ese proceso que se saco de memoria
        free_memory_page = self.getForcedFreePage()
        
        # Obtiene las instruciones a cargar en memoria
        instrs = self.getHDD().getSwappedPage(aPCB, page_number)
        # Settea la pagina del PCB 
        self.getPageTable().setPage(aPCB, page_number, free_memory_page, len(instrs), False)
        self.writeOnMemory(instrs, free_memory_page)
        
    def getForcedFreePage(self):
        '''
        if there is any free page on memory, return it. unless,
        swap some page of some pcb and returns its memory page.
        '''
        free_bases = self.getFreeMemoryPagesBases()
        if not free_bases:
            # Swapea algun PCb y acualiza la tabla
            self.swapSomePCB()
            free_bases = self.getFreeMemoryPagesBases()
            
        return free_bases[0] 
    
    
# Fits    
    
class Fit():
    def __init__(self):
        self.mmu = None
    
    def getFreePlaceBases(self):
        '''
        Return (base,lenght) tuples of all free place in memory
        '''
        mmu = self.mmu
        return mmu.getFreePlaceBases()
    
    def availableFreePlaceBases(self, instrs):
        '''
        Return all tuples (base,lenght) where 'lenght' is more than instrs lenght
        '''
        free_place_bases = self.getFreePlaceBases()  # Should return (base,lenght) tuples
        available_free_place_bases = [ free_place_base for free_place_base in free_place_bases 
                                      if free_place_base[1] >= len(instrs) ]
        return available_free_place_bases
        
    def getBaseFor(self, instrs):
        '''
        Get all availables (base,lenght) tuple for length of instrs, 
         and return the base where the length if more than another 
        
        '''
        tuples = self.availableFreePlaceBases(instrs)
        if tuples:
            return self.correctBaseFromTuples(tuples)
        else:
            return None  
        
    def setMMU(self,mmu):
        self.mmu = mmu  
        

class AsignacionContinua(MMU):
    def __init__(self, memory, hdd, page_table, fit):
        MMU.__init__(self, memory, hdd, page_table)
        self.fit = fit
        self.fit.setMMU(self)
        
    def load(self, aPCB, instrs):
        # Si hay mas instrucciones que espacio total de la memoria, Se lanza una excepcion
        if (len(instrs) > self.getMemory().size()):
            raise ProgramTooLongException()
        
        table = self.getPageTable()
        # El metodo 'getBaseFor(instrs)' debe usar el Primer, mejor o peor ajuste (Fit())
        # o compactar si sirve, o en ultimo caso empezar a swapear procesos hasta tener 
        # lugar suficiente.
        base = self.getBaseFor(instrs)
        
        # Settea la unica pagina de la tabla. (PCB, numero_de_pagina,base,limit,Sswapped)
        table.setPage(aPCB, 0, base, len(instrs), False)
        self.writeOnMemory(instrs, base)
        
    def getBaseByEstrategy(self, instrs):
        return self.getFit().getBaseFor(instrs)
        
    def getBaseFor(self, instrs):
        '''
        Este metodo usa 'getBaseByEstrategy(instruciones)' en parte para devolver una
        posible Base segun la estrategia de 'fit'.
        '''        
        base = self.getBaseByEstrategy(instrs)
        if base:
            return base 
        
        # Si no hay un bloque que se pueda usar, miro cuanto es la suma de los espacios vacio.
        # Si esa suma (free_place_size) es mayor o igual al largo de las instrucciones, entonces
        # compacto y tomo la primera base libre
        free_place_size = self.allFreePlace()  # Retorna la cantidad total de espacio libre
        
        # Compacto y retorno la primera base
        if (free_place_size >= len(instrs)): 
            self.compact()
            return self.firstFreePlace()
        
        # Empizo a swappear otros procesos hasta que el espacio sea suficiente
        
        # 'all_free_place' = todo el espacio libre hasta ahora (igual a  a 'free_place_size') 
        all_free_place = self.allFreePlace()
            
        # Mientras no tenga espacio para poner el Proceso, swappeo otros procesos
        while(all_free_place < len(instrs)):
            base = self.swapSomePCB()
            all_free_place = self.allFreePlace()
                
        return base
    
    def getFreePlaceBases(self):
        '''
        Return all (base,lenght) tuples where base is the begin 
          of a unused block of memory and lenght is the lenght of this block
        '''
        tuples = []
        tuple = [0, 0]  # (base,length) tuples
        contando = False
        memory = self.getMemory()
        
        # Si estoy contando y el cluster sobre el q estoy (index) esta en uso, 
        #  dejo de contar y agrego la tupla al conjunto.
        # Si estoy contando y el cluster sobre el q estoy no esta en uso,
        #  sumo 1 al tamanho del bloque libre (segundo elemento de la tupla)
        # Si no estoy contando y el cluster sobre el que estoy no esta en uso;
        #  seteo la base (index), pongo el lenght en 1 y comienzo a contat
        for index in range(memory.size()):
            if contando:
                if (memory.inUse(index)):
                    tuples.append(tuple)
                    tuple = [0, 0]
                    contando = False
                else:
                    tuple[1] = tuple[1] + 1
            elif (not memory.inUse(index)):
                contando = True
                tuple[0] = index
                tuple[1] = 1
                
        if contando:
            tuples.append(tuple)
        return tuples            
    
    def compact(self):
        memory = self.getMemory()
        tengo_una_base_libre = False # Si ya encontre una base libre y estoy esperando encontrar un bloque para mover
        begin_base = 0 # donde empieza esa base libre 
        for index in range(memory.size()):
            if tengo_una_base_libre:
                #Si estoy contando y el cluster sobre el que estoy esta en uso
                if(memory.inUse(index)):
                    pass 
                    #Aca es que pasa cuando venia contando los espacion vacios y me encuentro con una instrucion
                    # deberia obtener el PCB en esa base, mover todas sus instruccion (base_del_PBC - begin_base)
                    # hacia arriba. setear la pagina de ese PCB en la PageTable.
                    # setear los clusters de memoria libres como en 'no uso'
            else:
                # Si no estoy contando y el cluster sobre el que estoy esta libre
                if(not memory.inUse(index)):
                    contando = True
                    begin_base = index
                    
    
    def allFreePlace(self):
        '''
        Return all free place in memory
        '''
        tuples = self.getFreePlaceBases()
        # reduce(funcion_de_dos_parametro, lista_a_reducir) = inject
        suma = reduce(lambda x, y: x[1] + y[1], tuples, [0,0])
        return suma
    
    def firstFreePlace(self):
        '''
        Return the first free cluster (called too 'base')
        '''
        for index in range(self.getMemory().size()):
            if not self.getMemory().inUse(index):
                return index
        
    def getLenBlock(self, aPCB):
        return self.getLenPCB(aPCB)

    def calcNumPages(self, aPCB):
        return 1
        
    def numPagesFor(self, aPCB):
        return self.calcNumPages(aPCB)
    
        
    def getLenPCB(self, aPCB):
        return self.hdd.lenProgram(aPCB.getPath())
    
    def getFit(self):
        return self.fit
    
    def setFit(self, fit):
        self.fit = fit
        
# Sub-class of MMU

'''
To Do List:
    test it!

'''
    
class WorstFit(Fit):
    def __init__(self):
        Fit.__init__(self)

    def correctBaseFromTuples(self, tuples):
        '''
        Ordena de menor a mayor y retorna la base de la tupla 
          con el 'lenght' mas grande
        '''
        sorted_tuples = sorted(tuples, key=lambda tuple: tuple[1])
        if not sorted_tuples:
            return []
        return sorted_tuples.pop(0)[0]
    
class BestFir(Fit):
    def __init__(self):
        Fit.__init_(self)
        
    def correctBaseFromTuples(self, tuples):
        '''
        Ordena de menor a mayor y retorna la base de la tupla
          con el menor 'lenght'
        '''
        sorted_tuples = sorted(tuples, key=lambda tuple: tuple[1])
        return sorted_tuples.pop(0)[0]
    
class FirstFit(Fit):
    def __init__(self):
        Fit.__init__(self)
        
    def correctBaseFromTuples(self, tuples):
        '''
        Select the base form the first tuple
        '''
        return tuples.pop(0)[0]
    
        
# Exceptions

class AbstractMethodException(Exception):
    def __str__(self):
        return "This method must be implemented on sub-class"

class ProgramTooLongException(Exception):
    def __str__(self):
        return "This program is too long to be executed"
