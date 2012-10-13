'''
Created on 21/09/2012

@author: MarianoLinares
'''

from hardware.CPU import CPU
from hardware.Clock import Clock
from software.Scheduler import FIFO
from software.PCB import PCB
from software.Program import Program, Instruction

class Kernel:

    def __init__(self):
        # Internal state
        self.name = "Infra"
        self.version = "0.1"
        self.nextPCBID = 1
        self.modeKernel = False
        # Hardware
        self.cpu = CPU(self)
        self.clock = Clock(1, [self.cpu])  # Start clock
        # Software
        self.scheduler = FIFO(self)
        
        print(self.name + " " + self.version + " started.")
        
    def executeProgram(self, aProgram):
        
        # Build new PCB
        newPCB = PCB(self, aProgram)
        self.scheduler.addPCB(newPCB)
        self.nextPCBID += 1

        # if cpu is idle, switch now
        if self.cpu.idle:
            # Execute new PCB
            self.scheduler.contextSwitch()
            
    # TODO: IRQ (interrupt manager)
    def haltEND(self):
        print("haltEND")
        self.turnToKernelMode()
        self.scheduler.contextSwitch()
        self.turnToUserMode()
        
    def turnToKernelMode(self):
        self.modeKernel = True

    def turnToUserMode(self):
        self.modeKernel = False

#==================================
#       ''' Main execute '''
#==================================

instC = Instruction(True)
instI = Instruction(False)

# Sudoku
p1 = Program("Sudoku")
p1.setInstructions([instC, instC, instC, instC, instC, instC, instC])
print(p1.name + ": " + str(len(p1.instructions)) + " instructions.")

# TicTacToe
p2 = Program("TicTacToe")
p2.setInstructions([instC, instC, instC, instC, instC, instC, instC])
print(p2.name + ": " + str(len(p2.instructions)) + " instructions.")

# Mines
p3 = Program("Mines")
p3.setInstructions([instC, instC, instC, instC, instC, instC, instC])
print(p3.name + ": " + str(len(p3.instructions)) + " instructions.")

# Kernel
k = Kernel()
k.executeProgram(p1)
k.executeProgram(p2)
k.executeProgram(p3)
