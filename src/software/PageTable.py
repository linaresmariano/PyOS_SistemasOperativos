'''
Created on 18/11/2012

@author: mariano
'''

'''
Asocia pcbs a sus paginas en memoria con un diccionario
@invariant: Siempre se piden datos de IDs existentes
'''

class PageTable(list):
    ''' @param idd: ID del pcb para la nueva fila en la tabla
    Add a new ROW unblocked 
    '''
    def appendInfoPCB(self, idd):
        self.append({"id": idd, "blocked": False, "pages": []})

    ''' @param idd: ID de la fila a borrar
    Remove ROW 
    '''
    def removeInfoPCB(self, idd):
        for row in self:
            if row["id"] == idd:
                self.remove(row)
                
    def getElementWithId(self, idd):
        for row in self:
            if row["id"] == idd:
                return row
            
    def containsId(self, idd):
        for row in self:
            if row["id"] == idd:
                return True
        return False

 
    def addPage(self, idd, nroPage, base, limit):
        ''' @param idd: ID de la fila a agregar pagina
        @param nroPage: numero de la nueva pagina
        @param base: base de la nueva pagina
        @param limit: limite de la nueva pagina 
        Add new page at ROW whit id "idd", not readed 
        '''
        self.getElementWithId(idd)["pages"].append({"index": nroPage, "base": base, "limit": limit, "readed": False})


    ''' @param idd: ID of row to block
    Mark the id "idd" as blocked
    '''                
    def lockPCB(self, idd):
        self.getElementWithId(idd)["blocked"] = True
                
    def isLocked(self, idd):
            return self.getElementWithId(idd)["blocked"]
    
    # Get base in page "nroPage" of the process with id "idd"
    def getBase(self, idd, nroPage):
        return self.getElementWithId(idd)["pages"][nroPage]["base"]
    
    def setBase(self, idd, nroPage, base):
        self.getElementWithId(idd)["pages"][nroPage]["base"] = base
        
    def getLimit(self, idd, nroPage):
        return self.getElementWithId(idd)["pages"][nroPage]["limit"]
    
    def getReaded(self, idd, nroPage):
        return self.getElementWithId(idd)["pages"][nroPage]["readed"]
    
    def setReaded(self, idd, nroPage, readed, base=0):
        self.self.getElementWithId(idd)["pages"][nroPage]["readed"] = readed
        self.setBase(idd, nroPage, base)

        
