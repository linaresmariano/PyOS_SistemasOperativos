'''
Created on 18/11/2012

@author: mariano
'''
import unittest
from software.PageTable import PageTable

class TestPageTable(unittest.TestCase):
    def setUp(self):
        # PageTable to test
        self.pt = PageTable()
        
    def testAppendInfoPCB(self):
        # With new PageTable, it's empty
        self.assertFalse(self.pt, "PageTable is not Empty")
        
        # Appending first id
        self.pt.appendInfoPCB(1)
        self.assertEquals(len(self.pt), 1)
        self.assertTrue(self.pt.containsId(1), "ID 1 is not included")
        
        # Appending second id
        self.pt.appendInfoPCB(2)
        self.assertEquals(len(self.pt), 2)
        self.assertTrue(self.pt.containsId(1), "ID 1 is not included")
        self.assertTrue(self.pt.containsId(2), "ID 2 is not included")

    def testLockPCB(self):
        # With new id, it's unblocked
        self.pt.appendInfoPCB(1)
        self.assertFalse(self.pt.isLocked(1))
        # Locking pcb
        self.pt.lockPCB(1)
        self.assertTrue(self.pt.isLocked(1))
    

if __name__ == "__main__":
    unittest.main()