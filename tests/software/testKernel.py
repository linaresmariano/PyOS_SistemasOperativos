'''
Created on 12/12/2012

@author: mariano
'''
import unittest
from mockito import *
from hardware.CPU import CPU
from hardware.HDD import HDD
from hardware.IO import IO
from software.mmu import MMU
from software.Scheduler import Scheduler
from software.Kernel import Kernel

from software.Program import Program
from software.PCB import PCB


class Test(unittest.TestCase):

    def setUp(self):
        self.cpu = mock(CPU)
        self.mmu = mock(MMU)
        self.hdd = mock(HDD)
        self.scheduler = mock(Scheduler)
        self.io = mock(IO)
        self.kernel = Kernel(self.cpu, self.mmu, self.hdd, self.scheduler, self.io)

    def tearDown(self):
        self.kernel.shutDown()
        self.kernel = None

    # When CPU is Busy, the program wait
    def testExecuteProgramWhenCPUisBUSY(self):
        
        program = mock(Program)
        
        # mock CPU is idle
        when(self.cpu).isIdle().thenReturn(False)
        
        # kernel execute mock program
        self.kernel.executeProgram(program)
        
        # El pcb se agrega al scheduler y al mmu
        verify(self.scheduler).addPCB(any(PCB))
        verify(self.mmu).addPCB(any(PCB))

    # When CPU is IDLE, program runs in cpu
    def testExecuteProgramWhenCPUisIDLE(self):
        
        program = mock(Program)
        
        # mock CPU is idle
        when(self.cpu).isIdle().thenReturn(True)
        
        # kernel execute mock program
        self.kernel.executeProgram(program)
        
        # El pcb se agrega al scheduler y al mmu
        verify(self.scheduler).addPCB(any(PCB))
        verify(self.mmu).addPCB(any(PCB))
        
        verify(self.scheduler).contextSwitch()
        
        


        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testExecuteProgram']
    unittest.main()