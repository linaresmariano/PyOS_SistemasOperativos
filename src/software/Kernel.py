'''
Created on 21/09/2012

@author: MarianoLinares
'''

from hardware.CPU import CPU
from hardware.IO import IO
from hardware.Clock import Clock
from software.Scheduler import FIFO, RR, PRIO
from software.PCB import PCB
#from software.Timer import Timer

class Kernel:

    def __init__(self, cpu, mmu, hdd):
        # Internal state
        self.name = "Infra-Lalinhox"
        self.version = "v0.2"
        self.nextPCBID = 1
        self.modeKernel = False
        
        # Hardware
        self.cpu = cpu
        self.cpu.setKernel(self)
        
        # Memory manager
        self.mmu = mmu
        self.mmu.setKernel(self)
        
        self.hdd = hdd
        
        self.io = IO(self, 1)
        
        # Software
        #self.scheduler = FIFO(self)
        self.scheduler = RR(self, 3)
        #self.scheduler = PRIO(self)
        
        # Timer/Clock
        #self.timer = Timer([])
        self.clock = Clock(0.2, [self.cpu, self.scheduler])  # Start clock
        
        print("===============================================")
        print("       Welcome to " + self.name + " " + self.version)
        print("===============================================")
        
    def executeProgram(self, aProgram):
        
        # Build new PCB
        newPCB = PCB(self.nextPCBID, aProgram.getPath(), aProgram.length())
        self.scheduler.addPCB(newPCB)
        self.nextPCBID += 1

        # If cpu is idle, switch now
        if self.cpu.isIdle():
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
        return self.cpu.isIdle() and self.io.isIdle() and (not self.scheduler.readyQueue)
    
    # Shut down the OS
    def shutDown(self):
        self.clock.stop()
        self.io.stop()
        print("System shut down")
        
    def isModeKernel(self):
        return self.modeKernel
        
        

