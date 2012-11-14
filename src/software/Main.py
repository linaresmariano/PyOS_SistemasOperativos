'''
Created on 13/11/2012

@author: mariano
'''

from software.Program import Program, Instruction
from software.Kernel import Kernel

#==================================
#       ''' Main execute '''
#==================================

ic = Instruction(True)
ii = Instruction(False)

# Sudoku
p1 = Program("Sudoku")
p1.setInstructions([ic,ic,ic,ii,ii,ic,ic])
print(p1.name + ": " + str(len(p1.instructions)) + " instructions.")

# TicTacToe
p2 = Program("TicTacToe")
p2.setInstructions([ic,ic,ic,ic,ic,ic,ic])
print(p2.name + ": " + str(len(p2.instructions)) + " instructions.")

# Mines
p3 = Program("Mines")
p3.setInstructions([ic,ic,ic,ic,ic,ic,ic])
print(p3.name + ": " + str(len(p3.instructions)) + " instructions.")

# Kernel
k = Kernel()
k.executeProgram(p1)
k.executeProgram(p2)
k.executeProgram(p3)

'''
if __name__ == '__main__':
    pass'''