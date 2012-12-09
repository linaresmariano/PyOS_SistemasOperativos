'''
Created on 17/11/2012

@author: mariano
'''

from fileSystem.FileSystem import Folder
from exceptionOS.Excepts import InvalidPath

class HDD(list):
    def __init__(self):
        self.home = Folder("home", 0)

    def readProgram(self, path):
        '''
        @raise InvalidPath: raised when path is invalid
        @param path: the path of the program that we want to read
        @return: the program with path "path"
        '''
        for p in self:
            if p.getPath() == path:
                return p

        raise InvalidPath()
  
  
    def lenProgram(self, path):
        '''
        @precondition: "path" is a valid path 
        '''
        for p in self:
            if p.getPath() == path:
                return p.length()
    '''       
    def addFolder(self, name, path):
        currentFolder = self.home
        dest = path.split("/")
        dest.remove("")
        
        first = dest[0] 
        if first == currentFolder.name:
            dest.remove(first)

            if currentFolder.depth == len(dest):
                currentFolder.addChild(Folder(name, currentFolder.depth + 1))
                return
            else:
                if currentFolder.contains(folder):
                    currentFolder = currentFolder.getChild(Folder)
                    continue
                else:
                    break
        else:
            raise InvalidPath()
'''

      
'''
hdd = HDD()
print(hdd.home)
hdd.home.addSubFolder("mariano")
print(hdd.home.childs)    
#tes = "/home/mariano/development//git/python".split("/")

'''




#print (tes)


