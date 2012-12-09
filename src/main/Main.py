'''
Created on 13/11/2012

@author: mariano
'''

from software.Program import Program, Instruction
from software.Kernel import Kernel
from software.MMU import PMMU
from software.Scheduler import RR
from hardware.CPU import CPU
from hardware.HDD import HDD
from hardware.IO import IO

#==================================
#       ''' Main execute '''
#==================================



ic = Instruction(True)
ii = Instruction(False)

# Sudoku
p1 = Program("Sudoku", "game/Sudoku")
p1.setInstructions([ic,ic,ic,ii,ii,ic,ic])
print(p1.name + ": " + str(p1.length()) + " instructions.")

# TicTacToe
p2 = Program("TicTacToe", "game/TTT")
p2.setInstructions([ic,ic,ic,ic,ic,ic,ic])
print(p2.name + ": " + str(p2.length()) + " instructions.")

# Mines
p3 = Program("Mines", "game/Mines")
p3.setInstructions([ic,ic,ic,ic,ic,ic,ic])
print(p3.name + ": " + str(p3.length()) + " instructions.")


#========================
#   Hardware Computer
#========================
mmu = PMMU()
cpu = CPU(mmu)
hdd = HDD()
io = IO(1)

#=======================
#    Software Kernel
#=======================

# Planificador
scheduler = RR(3)

# Kernel
kernel = Kernel(cpu, mmu, hdd, scheduler, io)


# Ejecutar programas
kernel.executeProgram(p1)
hdd.append(p1)
kernel.executeProgram(p2)
hdd.append(p2)
kernel.executeProgram(p3)
hdd.append(p3)





