'''
Created on 21/09/2012

@author: MarianoLinares
'''

class CPU:
    '''
    classdocs
    '''


    def __init__(self, aKernel):
        self.currentPCB = None
        self.kernel = aKernel
        self.idle = True
    
    # Execute next instruction in currentPCB
    def execute(self):
        print("CPU idle: " + str(self.idle))
        
        # If is in UserMode and self is not idle, execute next instr
        if not self.kernel.modeKernel and not self.idle:
            # TODO: see if it's to CPU
            self.currentPCB.getInstruction()
            
            print("Intruction " + str(self.currentPCB.pc)
                  + " of " + str(len(self.currentPCB.program.instructions))
                  + " of " + str(self.currentPCB.program.name)
                  + ". Process ID: " + str(self.currentPCB.id) + " executed")
        
    def setCurrent(self, newPCB):
        self.currentPCB = newPCB