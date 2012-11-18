'''
Created on 15/11/2012

@author: mariano
'''

import unittest
from hardware.Memory import Memory

class TestMemory(unittest.TestCase):

    def setUp(self):
        self.m = Memory(10)

    def testCreateMemory(self):
        self.assertEquals(len(self.m.clusters), 10)
        
        self.m2 = Memory(20)
        self.assertEquals(len(self.m2.clusters), 20)

    def testWrite(self):
        # En el cluster 8 no hay datos
        self.assertIsNone(self.m.getClusters()[8]["data"])
        # Escribir datos en el cluster 8
        self.m.write(8, "lala")
        # En el cluster 8 estan los datos que escribimos
        self.assertEquals(self.m.getClusters()[8]["data"], "lala")
        
    def testRead(self):
        # En el cluster 8 no hay datos
        self.assertIsNone(self.m.getClusters()[8]["data"])
        # Testear que el metodo funciona
        self.assertIsNone(self.m.read(8))
        
        # Escribir en el cluster 8
        self.m.write(8, "lala")
        # En el cluster 8 podemos leer los datos que escribimos
        self.assertEquals(self.m.read(8), "lala")
        
    def testSetInUse(self):
        # El cluster 8 no esta en uso
        self.assertFalse(self.m.getClusters()[8]["inUse"])
        # Testear que el metodo funciona para True
        self.m.setInUse(8, True)
        self.assertTrue(self.m.getClusters()[8]["inUse"])
        
        # Testear que el metodo funciona para False
        self.m.setInUse(8, False)
        self.assertFalse(self.m.getClusters()[8]["inUse"])

if __name__ == "__main__":
    unittest.main()