# coding: UTF-8
'''
Created on 20.11.2012

@author: Sho
'''
import struct
import os
import os.path as path

#Глобальные константы
VHgamePath = u'D:/аниме/хентай/bestiality^monster^tentacles/!VH/my try/\
VHゲーム０１_121005_translated'
targetFile = path.join(VHgamePath, u'Map0545.lmu')


#Читает закодированный размер блока
#Ебанный накантос - переделать
def getSize(fileObj):
    b0 = struct.unpack('B', fileObj.read(1))[0]
    if 0b10000000 & b0:
        b1 = struct.unpack('B', fileObj.read(1))[0]
        if 0b10000000 & b1:
            b2 = struct.unpack('B', fileObj.read(1))[0]
            if 0b10000000 & b2:
                b3 = struct.unpack('B', fileObj.read(1))[0]
                return (0b01111111 & b0) * 0x80 * 0x80 * 0x80 + (0b01111111 & b1) * 0x80 * 0x80 + (0b01111111 & b2) * 0x80 + b3
            else:
                return (0b01111111 & b0) * 0x80 * 0x80 + (0b01111111 & b1) * 0x80 + b2
        else:
            return (0b01111111 & b0) * 0x80 + b1 
    else:
        return b0

def strInHex(string):
    h = ''
    for i in string:
        s = hex(ord(i))[2:]
        if len(s) == 1: s = '0' + s
        h +=  s + ' '
    return h

class MBlock(object):
    
    def __init__(self, fileObj, Map):
        self.data = self.read(fileObj)
        
    def read(self, fileObj):
        size = getSize(fileObj)
        return fileObj.read(size)
    
    def __repr__(self):
        return strInHex(self.data[:90])


class MStruct(object):

    #MStruct <= {'ID': (Type, 'Name', {})}    
    @staticmethod
    def IDtoName(ID, Map):
        if Map.has_key(ID):
            return Map[ID][1]
        else:
            return ID
    
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
    
    def __repr__(self):
        s = str()
        for id, b in sorted(self.blockDict.items()):
            id = MStruct.IDtoName(id, self.Map)
            s += id + ' : ' + repr(b) + '\n' 
        return s
      
        
    

class MList(object):
    
    #MList   <= (Type, {})            
    def __init__(self, fileObj, Map):
        self.elemList = self.read(fileObj, Map)
        
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
    
    def __repr__(self):
        s = '\n'
        for i, e in enumerate(self.elemList):
            if e:
                s += '\tElem ' + str(i) + ': ' + repr(e) + '\n' 
        return s


#MMap    <= (Type, {})
#MStruct <= {'ID': (Type, 'Name', {})}
#MBlock  <= ()
#MList   <= (Type, {})

#Map.Events[1].Name
#Map.Events[1].Page[2].CodeBlock

CodeBlock = ()

EventPage =  (MStruct, {'\x22': (MBlock,'Position',()),
                        '\x24': (MBlock,'AniType',()),
                        '\x25': (MBlock,'Speed',()),
                        '\x34': (MBlock,'CodeBlock',()),
                       }
             )

Event = (MStruct, {'\x01': (MBlock,'Name',()),
                    '\x02': (MBlock,'X',()),
                    '\x03': (MBlock,'Y',()),
                    '\x05': (MList,'Page',EventPage),

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
    print repr(Map.Events[3].Page[1].CodeBlock)
    print repr(Map.Events[3].Page[2].CodeBlock)
    print repr(Map.Events[3].Page[3].CodeBlock)
    print repr(Map.Events[3].Page[4].CodeBlock)
    print repr(Map.Events[3].Page[5].CodeBlock)
    print repr(Map.Events[3].Page[6].CodeBlock)
