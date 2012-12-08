'''
Created on 07/12/2012

@author: leandro
'''


class Page:
    ''' 
    Represent a Page of in a dictionary page_number: Page
    It's got the base, limit & swapped attributes
    Encourage the user of method access instead of direct attribute access.
    Example: 
    Use:
        page.swapped()
    Instead of:
        page.swapped
    '''
    def __init__(self, base, limit, swapped=False):
        self.base = base
        self.limit = limit
        self.swapped = swapped
        
    def swap(self):
        '''
        Change to True the swapped flag of page
        '''
        self.swapped = True
        
    def swapped(self):
        '''
        Return the swapped flag state (True/False)
        '''
        return self.swapped
    
    def unswap(self):
        '''
        Change to False the swapped flag of page
        '''
        self.swapped = False
        
    def limit(self):
        '''
        If the page is swapped, then a SwappedPageException 
        is raised, unless returns the limit of the page
        '''
        return self.get_attr('limit')
    
    def base(self):
        '''
        If the page is swapped, then a SwappedPageException 
        is raised, unless returns the base of the page
        in memory
        '''
        return self.get_attr('base')
    
    def set_base(self, base):
        '''
        Sets the limit of page on memory
        '''
        self.base = base
        
    def set_limit(self, limit):
        '''
        Sets the base of page on memory
        '''
        self.limit = limit

class TableUnit:
    '''
    Represents a Unit of table page, that has 
    blocked & pages attributes, in a PCB: TableUnit hash
    '''
    def __init__(self):
        self.blocked = False
        self.pages = {}
    
    def addPage(self, page_number, page_base, page_limit, swapped):
        '''
        Add a page on "page_number" index, with 
        its page_base, page_limit and swapped attributes
        '''
        self.pages[page_number] = Page(page_base, page_limit, swapped)
        
    def swapped(self, page_number):
        '''
        Return the swapped state of a page on
        "page_number" position
        '''
        return self.page(page_number).swapped()
    
    def swap(self, page_number):
        '''
        Swaps a page in "page_number" position
        '''
        self.page(page_number).swap()
        
    def unswap(self, page_number):
        '''
        "Unswaps" a page in "page_number" position
        '''
        self.page(page_number).unswap()
        
    def page(self, page_number):
        '''
        Returns a page in a "page_number" position
        '''
        self.pages[page_number]
        
    def limit(self, page_number):
        '''
        Returns the limit of a page in "page_number" position
        '''
        return self.page(page_number).limit()
        
    def base(self, page_number):
        '''
        Returns the base of a page in "page_number" position
        '''
        return self.page(page_number).base()
    
    def set_limit(self, page_number, limit):
        '''
        Sets the limit of a page in "page_number" position
        '''
        self.page(page_number).set_limit(limit)
        
    def set_base(self, page_number, base):
        '''
        Sets the base of a page in "page_number" position
        '''
        self.page(page_number).set_base(base)
        
class PageTable:
    '''
    Represents a MMU page table. It's got a hash PCB: TableUnit.
    Full tree representation:
    
    PageTable 
    {
        table = { PCB: TableUnit }
    }
    
    TableUnit
    {
        blocked = boolean
        pages = { Integer: Page }
    }
    
    Page
    {
        base = Integer
        limit = Integer
        swapped = boolean
    }
    
    '''
    def __init__(self):
        self.table = {}
        
    # Public interface
        
    def addPCB(self, aPCB):
        '''
        Create a new empty TableUnit, for specific PCB.
        If you try to create a new TableUnit, the old one 
        is substituted for the new.
        '''
        new_table_unit = TableUnit()
        self.table[aPCB] = new_table_unit
        
    def removePCB(self, aPCB):
        '''
        Removes the TableUnit for a Specific PCB.
        '''
        self.delPCB(aPCB)
        
    def addPage(self, aPCB, page_number, base, limit, swapped=False):
        '''
        Add a new page for a specific PCB, with its page_number,
        base, limit & swapped attributes.
        '''
        self.table[aPCB].addPage(page_number, base, limit, swapped)
        
    # Protected interface
        
    def delPCB(self, aPCB):
        '''
        Protected method to delete the TableUnit for a Specific PCB.
        '''
        del self.table[aPCB]
        
    def limit(self, aPCB, page_number):
        '''
        Protected method to get the limit of a specific PCB &
        page_number.
        '''
        return self.table[aPCB].limit(page_number)
    
    def base(self, aPCB, page_number):
        '''
        Protected method to get the base of a specific PCB &
        page_number
        '''
        return self.table[aPCB].base(page_number)
    
    def swap(self, aPCB, page_number):
        '''
        Protected method to set like swapped a page of a 
        specific PCB & page_number
        '''
        self.table[aPCB].swap(page_number)
        
    def swapped(self, aPCB, page_number):
        '''
        Protected method to get the swapped flag of a specific PCB &
        page_number
        '''
        return self.table[aPCB].swapped(page_number)
    
    def unswap(self, aPCB, page_number):
        '''
        Protected method to set like no swapped a page of a 
        specific PCB & page_number
        '''
        self.table[aPCB].unswap(page_number)
        
    def page(self, aPCB, page_number):
        '''
        Protected method to get the page of a specific PCB &
        page_number
        '''
        return self.table[aPCB].page(page_number)        
        
# Exceptions

class SwappedPageException(Exception):
    def __str__(self):
        return "Swapped page Exception"
        
        

