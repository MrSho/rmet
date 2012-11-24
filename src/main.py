# coding: UTF-8
'''
Created on 20.11.2012

@author: Sho
'''
import struct
import os
import os.path as path

import Command

#Глобальные константы
VHgamePath = u'D:/аниме/хентай/bestiality^monster^tentacles/!VH/my try/\
VHゲーム０１_121005_translated'
targetFile = path.join(VHgamePath, u'Map0545.lmu')


#Читает закодированный размер блока   
def getSize(fileObj, sum = 0):
    b = struct.unpack('B', fileObj.read(1))[0]
    if 0b10000000 & b:
        return getSize(fileObj, sum * 0x80 + (0b01111111 & b))
    else:
        return sum * 0x80 + (0b01111111 & b)

#Возвращает шестнадцатиричное представление для
#для последовательности байтов в виде строки  
def strInHex(string):
    s = str()
    for i in string:
        c = struct.unpack('B', i)[0]
        c = hex(c).replace('0x', '')
        if len(c) == 1: c = '0' + c
        s += ' ' + c
    return s.strip()      


class MBlock(object):
    
    def __init__(self, fileObj, Map):
        self.data = self.read(fileObj)
        self.Map = Map
        
    def read(self, fileObj):
        size = getSize(fileObj)
        return fileObj.read(size)
    
    def __repr__(self, depth = 0):
        return strInHex(self.data[:90])
    
class MString(MBlock):

    #Fix! Не показывает иероглифы!      
    def __repr__(self, depth = 0):
        return self.data.decode(encoding='shift_jis_2004')
    
class MEnum(MBlock): pass


class MStruct(object):

    #MStruct <= {'ID': (Type, 'Name', {})}    
    @staticmethod
    def IDtoName(ID, Map):
        if Map.has_key(ID):
            return Map[ID][1]
        else:
            return ID
    
    @staticmethod
    def IDtoNameRepr(ID, Map):
        if Map.has_key(ID):
            return Map[ID][1]
        else:
            return strInHex(ID)
        
    @staticmethod
    def getAnsMap(ID, Map):
        if Map.has_key(ID):
            return Map[ID][2]
        else:
            return {}
        
    @staticmethod
    def getType(ID, Map):
        if Map.has_key(ID):
            return Map[ID][0]
        else:
            return MBlock
    
    def __init__(self, fileObj, Map):
        self.Map = Map
        self.blockDict = self.read(fileObj, Map)
       
    def read(self, fileObj, Map):
        bd = {}
        while True:
            ID = fileObj.read(1)
            if ID == '\x00': break            
            #Определяется
            b = MStruct.getType(ID, Map)(fileObj, MStruct.getAnsMap(ID, Map))
            Name = MStruct.IDtoName(ID, Map)
            bd[ID] = b
            setattr(self, Name, b) 
            
        return bd
    
    def __repr__(self, depth = 0):
        s = str()
        for id, b in sorted(self.blockDict.items()):
            id = MStruct.IDtoNameRepr(id, self.Map)
            s += '    ' * depth + id + ' : ' + b.__repr__(depth + 1) + '\n' 
        return s
      

class MList(object):
    
    #MList   <= (Type, {})            
    def __init__(self, fileObj, Map):
        self.elemList = self.read(fileObj, Map)
    
    #Fix!    
    def read(self, fileObj, Map):
        el = [0] * 1000
        size = getSize(fileObj)
        c = struct.unpack('B', fileObj.read(1))[0]
        for i in xrange(c):
            n = struct.unpack('B', fileObj.read(1))[0]
            el[n] = Map[0](fileObj, Map[1])
             
             
        return el
    
    def __getitem__(self, key):
        return self.elemList[key]
    
    def __repr__(self, depth = 0):
        s = '\n'
        for i, e in enumerate(self.elemList):
            if e:
                s += '    ' * depth + '[' + str(i) + ']: ' + '\n'+  e.__repr__(depth + 1) 
        return s

class MEventCommands(object):
    defaultHandler = Command.Unknown
    
    def __init__(self, fileObj, Map):
        self.CommandList = []
    
    def read(self, fileObj, Map): pass
    
    def __repr__(self, depth = 0): pass
    
   
        


#MMap    <= (Type, {})
#MStruct <= {'ID': (Type, 'Name', {})}
#MBlock  <= ()
#MList   <= (Type, {})

#Map.Events[1].Name
#Map.Events[1].Pages[2].CodeBlock

EventCommands = ()

EventPage =  (MStruct, {'\x15': (MString,'TilePath',()),
                        '\x22': (MBlock,'Position',()),
                        '\x24': (MBlock,'AniType',()),
                        '\x25': (MBlock,'Speed',()),
                        '\x34': (MBlock,'EventCommands',()),
                       }
             )

Event = (MStruct, {'\x01': (MString,'Name',()),
                    '\x02': (MBlock,'X',()),
                    '\x03': (MBlock,'Y',()),
                    '\x05': (MList,'Pages',EventPage),

                  }
         )


MapMap =  (MStruct, {'\x01': (MBlock,'ChipSet',()),
                     '\x0b': (MBlock,'ScrollType',()),
                     '\x47': (MBlock,'LoTaleSet',()),
                     '\x48': (MBlock,'UpTaleSet',()),
                     '\x51': (MList,'Events', Event),
                     '\x5b': (MBlock,'SaveCount',())
                    }
           )
               


if __name__ == '__main__':
    f = open(targetFile, 'rb')
    signature = f.read(11)
    Map = MStruct(f, MapMap[1])
    print repr(Map)

