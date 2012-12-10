'''
Created on 16/11/2012

@author: mariano
'''

# Pseudo MMU
class PMMU:
    def setKernel(self, aKernel):
        self.kernel = aKernel

    # Busca la instruccion directo a disco
    def fetchInstruction(self, pcb):
        path = pcb.getPath()
        prog = self.kernel.hdd.readProgram(path)

        return prog.getInstruction(pcb.getPc())


# Abstract
class MMU:
    def __init__(self, memory, hdd, pageTable):
        self.memory = memory
        self.hdd = hdd
        self.pageTable = pageTable
        
    def getPageTable(self):
        return self.pageTable
    
    def getMemory(self):
        return self.memory
        
    def fetchInstruction(self, idPCB, pc):
        page = pc / self.getLenBlock(idPCB)
        desp = pc % self.getLenBlock(idPCB)
        base = self.getPageTable().getBase(idPCB, page)
        
        inst = self.getMemory().read(base + desp)
        
        return inst
    
    def getLenPCB(self, aPCB):
        return self.hdd.lenProgram(aPCB.getPath())
    
    # Abstract
    def addPCB(self, aPCB):
        program = self.getHDD().readProgram(aPCB.getPath())
        instrs = program.getInstructions()
        
        # Create new row in PageTable to new PCB
        self.getPageTable().addPCB(aPCB, self.calcNumPages())
        
        # Load pages
        self.load(aPCB, instrs)
        '''nroPages = self.getLenPCB(aPCB) 
        for x in range(0, self.calcNumPages(aPCB)):
            self.getPageTable().addPage(aPCB, x, 0, self.calcLenBlock(aPCB)'''
    
class Paginacion(MMU):
    def __init__(self, lenBlock):
        self.lenBlock = lenBlock
        
    def getLenBlock(self, aPCB):
        return self.lenBlock
    
    def calcNumPages(self, aPCB):
        self.getLenPCB(aPCB) / self.getLenBlock(aPCB)


class AsigCont(MMU):
    
    def getLenBlock(self, aPCB):
        return self.getLenPCB(aPCB)

    def calcNumPages(self, aPCB):
        return 1
    
    
    
    
