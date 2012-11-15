'''
Created on 13/11/2012

@author: mariano
'''

import unittest
from mockito import *
from hardware.IO import IO
from software.Kernel import Kernel
from software.PCB import PCB

class TestIO(unittest.TestCase):
    
    def setUp(self):
        self.kernel = mock(Kernel)
        when(self.kernel).isModeKernel().thenReturn(False)
        self.pcb1 = mock(PCB)
        when(self.pcb1).getId().thenReturn(1)
        self.pcb2 = mock(PCB)
        when(self.pcb2).getId().thenReturn(2)
        self.io = IO(self.kernel, 1)
        
    def tearDown(self):
        self.io.stop()
        
    def testReset(self):
        # Se crea vacio
        self.assertIsNone(self.io.currentPCB, "currentPCB not None")
        
        # Al agregar un pcb y resetear debe quedar vacio
        self.io.addPCB(self.pcb1)
        self.io.reset()
        self.assertIsNone(self.io.currentPCB, "currentPCB not None")
       
    def testTickWHENnotModeKernel(self):
        #==========================
        # Con IO vacio no pasa nada
        #==========================
        self.io.tick()
        self.assertIsNone(self.io.currentPCB)
        self.assertEquals(len(self.io.readyQueue), 0)
        
        #==========================================================
        # Con un elemento en la queue, current None, not modeKernel
        #==========================================================
        self.io.readyQueue.append(self.pcb1)
        self.assertIsNone(self.io.currentPCB, "currentPCB not None")
        self.assertEquals(len(self.io.readyQueue), 1)
        
        when(self.pcb1).isEnded().thenReturn(False)
        
        self.io.tick()
        
        self.assertIs(self.io.currentPCB, self.pcb1)
        self.assertEquals(len(self.io.readyQueue), 0)
        
        # Verify interaction with the currentPCB
        verify(self.pcb1).isEnded()
        verify(self.pcb1).increasePC()
        verifyNoMoreInteractions(self.pcb1)
       
        verify(self.kernel).IOcpuHALT()
        
    def testTickWHENModeKernel(self):
        #==========================
        # Con IO vacio no pasa nada
        #==========================
        self.io.tick()
        self.assertIsNone(self.io.currentPCB)
        self.assertEquals(len(self.io.readyQueue), 0)
        
        #========================================================
        # Con un elemento en la queue y current None, modeKernel
        #========================================================
        self.io.readyQueue.append(self.pcb1)
        self.assertIsNone(self.io.currentPCB, "currentPCB not None")
        self.assertEquals(len(self.io.readyQueue), 1)
        
        when(self.pcb1).isEnded().thenReturn(False)
        when(self.kernel).isModeKernel().thenReturn(True)
        
        self.io.tick()
        
        self.assertIs(self.io.currentPCB, self.pcb1)
        self.assertEquals(len(self.io.readyQueue), 0)
        
        # Verify interaction with the currentPCB
        verifyZeroInteractions(self.pcb1)
        
    def testTickWHENcurrentPCBIsToEnd(self):
        #==========================================================
        # Con un elemento en la queue, current None, not modeKernel
        #==========================================================
        self.io.readyQueue.append(self.pcb1)
        self.assertIsNone(self.io.currentPCB, "currentPCB not None")
        self.assertEquals(len(self.io.readyQueue), 1)
        
        when(self.pcb1).isEnded().thenReturn(True)
        
        self.io.tick()
        
        self.assertIs(self.io.currentPCB, self.pcb1)
        self.assertEquals(len(self.io.readyQueue), 0)
        
        # Verify interaction with the currentPCB
        verify(self.pcb1).isEnded()
        verify(self.pcb1).increasePC()
        verifyNoMoreInteractions(self.pcb1)
       
        # Verify interaction with the kernel
        verify(self.kernel).IOfinHALT()
        
    def testIsIdle(self):
        # Se crea vacio
        self.assertTrue(self.io.isIdle())
        
        # Al agregar un pcb y resetear debe quedar vacio
        self.io.addPCB(self.pcb1)
        self.io.tick()
        self.assertFalse(self.io.isIdle())

if __name__ == '__main__':
    unittest.main()