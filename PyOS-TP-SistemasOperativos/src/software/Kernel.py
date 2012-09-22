'''
Created on 21/09/2012

@author: MarianoLinares
'''

from hardware.CPU import CPU
from hardware.Clock import Clock
from software.Scheduler import FIFO
from software.PCB import PCB
from software.Program import Program
from software.Program import Instruction

class Kernel:

    def __init__(self):
        # Internal state
        self.name = "Infra"
        self.version = "0.1"
        self.nextPCBID = 1
        self.modeKernel = False
        # Hardware
        self.cpu = CPU(self)
        #self.clock = Clock(1, [])
        # Software 
        self.scheduler = FIFO()
        print(self.name + " " + self.version + " started.")
        
        #Start clock
        self.clock = Clock(1, [self.cpu])
        
    def executeProgram(self, aProgram):
        # Build new PCB
        newPCB = PCB(self, aProgram)
        self.nextPCBID += 1
        
        # if cpu is idle
        if self.cpu.idle:
            # Execute new PCB
            self.cpu.setCurrent(newPCB)
            self.cpu.idle = False
        else:
            # Add in the scheduler a new PCB ready to execute
            self.scheduler.addPCB(newPCB)
            
    # TODO: IRQ (interrupt manager)
    def haltEND(self):
        self.modeKernel = True
        self.cpu.idle = True
        
        print("Running program ends")
        #self.dispatcher(self.scheduler.nextPCB())



#==================================
#       ''' Main execute '''
#==================================

i = Instruction("cpu")

# Sudoku
p1 = Program("Sudoku")
p1.setInstructions([i, i, i, i, i, i, i])
print(p1.name + ": " + str(len(p1.instructions)) + " instructions.")

# TicTacToe
p2 = Program("TicTacToe")
p2.setInstructions([i, i, i, i, i, i, i])
print(p2.name + ": " + str(len(p2.instructions)) + " instructions.")

# Kernel
k = Kernel()
k.executeProgram(p1)
k.executeProgram(p2)

#k.cpu.currentPCB = PCB(k, )