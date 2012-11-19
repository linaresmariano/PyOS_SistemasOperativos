'''
Created on 18/11/2012

@author: mariano
'''
import unittest
from mockito import *
from hardware.HDD import HDD, InvalidPath
from software.Program import Program

class TestHDD(unittest.TestCase):
    
    def setUp(self):
        # Testing
        self.hdd = HDD()
        
        # Mock program 1
        self.p1 = mock(Program)
        when(self.p1).getPath().thenReturn("path1")
        
        # Mock program 2
        self.p2 = mock(Program)
        when(self.p2).getPath().thenReturn("path2")

    def testReadProgram(self):
        #=============================
        #   Without programs in HDD
        #=============================
        self.assertRaises(InvalidPath, self.hdd.readProgram, "path1")
        
        #==========================
        #     With one program
        #==========================
        self.hdd.append(self.p1)
        
        # Invalid path
        self.assertRaises(InvalidPath, self.hdd.readProgram, "path1dsa")
        # Path of "p1"
        self.assertEquals(self.hdd.readProgram("path1"), self.p1)
        
        #===========================
        #     With two programs
        #===========================
        self.hdd.append(self.p2)
        # Invalid path
        self.assertRaises(InvalidPath, self.hdd.readProgram, "pdsh1sa")
        # Path of "p1"
        self.assertEquals(self.hdd.readProgram("path1"), self.p1)
        # Path of "p2"
        self.assertEquals(self.hdd.readProgram("path2"), self.p2)
        
        
    def testLenProgram(self):
        self.hdd.append(self.p1)
        self.hdd.append(self.p2)

        # Length of p1
        when(self.p1).length().thenReturn(10)
        self.assertEquals(self.hdd.lenProgram(self.p1.getPath()), 10)
        
        # Length of p2
        when(self.p2).length().thenReturn(20)
        self.assertEquals(self.hdd.lenProgram(self.p1.getPath()), 10)
        self.assertEquals(self.hdd.lenProgram(self.p2.getPath()), 20)


if __name__ == "__main__":
    unittest.main()