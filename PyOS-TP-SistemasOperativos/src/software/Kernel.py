'''
Created on 21/09/2012

@author: MarianoLinares
'''

from hardware.CPU import CPU
from hardware.IO import IO
from hardware.Clock import Clock
from software.Scheduler import FIFO, RR, PRIO
from software.PCB import PCB
from software.Program import Program, Instruction
#from software.Timer import Timer

class Kernel:

    def __init__(self):
        # Internal state
        self.name = "Infra"
        self.version = "v0.1"
        self.nextPCBID = 1
        self.modeKernel = False
        
        # Hardware
        self.cpu = CPU(self)
        self.io = IO(self)
        
        # Software
        self.scheduler = FIFO(self)
        #self.scheduler = RR(self, 3)
        #self.scheduler = PRIO(self)
        
        # Timer/Clock
        #self.timer = Timer([])
        self.clock = Clock(0.2, [self.cpu, self.io, self.scheduler])  # Start clock
        
        print("====================================")
        print("       Welcome to " + self.name + " " + self.version)
        print("====================================")
        
    def executeProgram(self, aProgram):
        
        # Build new PCB
        newPCB = PCB(self.nextPCBID, aProgram)
        self.scheduler.addPCB(newPCB)
        self.nextPCBID += 1

        # If cpu is idle, switch now
        if self.cpu.idle:
            # Execute new PCB
            self.scheduler.contextSwitch()
            
    # TODO: IRQ (interrupt manager)
    def haltEND(self):
        print("haltEND")
        # 1. Turn to Kernel MODE
        self.turnToKernelMode()
        # 2. Restart quantum timer
        # TODO: see if restartQuantum occurs
        self.scheduler.restartQuantum()
        # 3. Handle old pcb
        # Delete finished pcb
        self.cpu.reset()
        # 4. Context switch with new pcb
        self.scheduler.contextSwitch()
        # 5. Turn to User MODE
        self.turnToUserMode()
        
    def TIMEoutHALT(self):
        print("time out")
        # 1. Turn to Kernel MODE
        self.turnToKernelMode()
        # 2. Restart quantum timer
        self.scheduler.restartQuantum()
        # 3. Handle old pcb
        # nothing
        # 4. Context switch with new pcb
        self.scheduler.contextSwitch()
        # 5. Turn to User MODE
        self.turnToUserMode()
        
    def CPUioHALT(self):
        print("Instruction to IO")
        # 1. Turn to Kernel MODE
        self.turnToKernelMode()
        # 2. Restart quantum timer
        self.scheduler.restartQuantum()
        # 3. Handle old pcb
        # Delegate to IO current PCB in CPU
        self.scheduler.sendToIO(self.cpu.getCurrentPCB())
        self.cpu.reset()
        # 4. Context switch with new pcb
        self.scheduler.contextSwitch()
        # 5. Turn to User MODE
        self.turnToUserMode()
    
    def IOfinHALT(self):
        print("IO fin Halt")
        # 1. Turn to Kernel MODE
        self.turnToKernelMode()
        # 2. Restart quantum timer
        #self.scheduler.restartQuantum()
        # 3. Handle old pcb
        self.io.reset()
        # 4. Context switch with new pcb
        #self.scheduler.contextSwitch()
        # 5. Turn to User MODE
        self.turnToUserMode()
        
    def IOcpuHALT(self):
        print("IO to CPU instr")
        # 1. Turn to Kernel MODE
        self.turnToKernelMode()
        # 2. Restart quantum timer
        self.scheduler.restartQuantum()
        # 3. Handle old pcb
        # Delegate to Scheduler current PCB in IO and PCB in CPU
        self.scheduler.addPCB(self.io.getCurrentPCB())
        # 4. Context switch with new pcb
        self.scheduler.contextSwitch()
        # 5. Turn to User MODE
        self.turnToUserMode()
          
        
    def turnToKernelMode(self):
        self.modeKernel = True

    def turnToUserMode(self):
        self.modeKernel = False
    
    # Returns true if all queues are empty
    def thisIsTheEnd(self):
        return self.cpu.idle and self.io.isIdle() and (not self.scheduler.readyQueue)
    
    # Shut down the OS
    def shutDown(self):
        self.clock.stop()
        print("System shut down")


#==================================
#       ''' Main execute '''
#==================================

ic = Instruction(True)
ii = Instruction(False)

# Sudoku
p1 = Program("Sudoku")
p1.setInstructions([ii,ic,ii,ic,ii,ic,ii])
print(p1.name + ": " + str(len(p1.instructions)) + " instructions.")

# TicTacToe
p2 = Program("TicTacToe")
p2.setInstructions([ii,ii,ii,ic,ii,ic,ii])
print(p2.name + ": " + str(len(p2.instructions)) + " instructions.")

# Mines
p3 = Program("Mines")
p3.setInstructions([ic,ii,ii,ic,ii,ic,ii])
print(p3.name + ": " + str(len(p3.instructions)) + " instructions.")

# Kernel
k = Kernel()
k.executeProgram(p1)
k.executeProgram(p2)
k.executeProgram(p3)
