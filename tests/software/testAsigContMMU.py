'''
Created on 17/11/2012

@author: mariano
'''
import unittest
from mockito import *
from software.MMU import AsigCont
from software.PageTable import PageTable
from software.PCB import PCB
from hardware.HDD import HDD
from hardware.Memory import Memory

class TestAsigCont(unittest.TestCase):

    def setUp(self):
        # Mock a pcb
        self.pcb1 = mock(PCB)
        when(self.pcb1.getPath()).thenReturn("la")
        
        # Mock a HDD
        self.hdd = mock(HDD)
        when(self.hdd.lenProgram("la")).thenReturn(14)
        
        self.page = mock(PageTable)
        self.memory = mock(Memory)
        
        self.strategy = AsigCont(self.memory, self.hdd, self.page)
        

    def testFetchInstruction(self):
        self.strategy.fetchInstruction(self.pcb1, 9)
        #self.estrategy.fetchInstruction(self.pcb1, 10)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()