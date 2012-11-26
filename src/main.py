# coding: UTF-8
'''
Created on 20.11.2012

@author: Sho
'''
import struct
import os
import os.path as path
import StringIO

from misc import getFNum, getFNumStr, strInHex
import Command

#Глобальные константы
VHgamePath = u'D:/аниме/хентай/bestiality^monster^tentacles/!VH/my try/\
VHゲーム０１_121005_translated'
targetFile = path.join(VHgamePath, u'Map0545.lmu')

reprLen = 120
    

class MBlock(object):
    
    def __init__(self, fileObj, Map, size = 0):
        self.data = self.read(fileObj, size)
        self.Map = Map
        
    def read(self, fileObj, size):
        return fileObj.read(size)
    
    def __repr__(self, depth = 0):
        return strInHex(self.data[:reprLen])
    
class MString(MBlock):
     
    def __repr__(self, depth = 0):
        return self.data.decode(encoding='shift_jis_2004')
    
class MEnum(MBlock):
    
    def __repr__(self, depth = 0):
        b = struct.unpack('B', self.data[0])[0]
        try:
            return self.Map[b]
        except:
            return strInHex(self.data[:reprLen])
        
class MFlag(MBlock):
     
    def __repr__(self, depth = 0):
        return repr(bool(struct.unpack('B', self.data[0])[0]))
    
class MNum(MBlock):
    
    def __repr__(self, depth = 0):
        return repr(getFNumStr(self.data))

class MBitMap(MBlock):
    
    def __repr__(self, depth = 0):
        return bin(getFNumStr(self.data))        


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
    
    def __init__(self, fileObj, Map, size = 0):
        self.Map = Map
        self.blockDict = self.read(fileObj, Map)
       
    def read(self, fileObj, Map):
        bd = {}
        while True:
            ID = fileObj.read(1)
            if ID == '\x00': break            
            #Определяется
            size = getFNum(fileObj)
            b = MStruct.getType(ID, Map)(fileObj, MStruct.getAnsMap(ID, Map), size)
            Name = MStruct.IDtoName(ID, Map)
            bd[ID] = b
            setattr(self, Name, b) 
            
        return bd
    
    def __repr__(self, depth = 0):
        s = '\n'
        for id, b in sorted(self.blockDict.items()):
            id = MStruct.IDtoNameRepr(id, self.Map)
            s += '    ' * depth + id + ': ' + b.__repr__(depth + 1) + '\n' 
        return s
      

class MList(object):
    
    #MList   <= (Type, {})            
    def __init__(self, fileObj, Map, size = 0):
        self.elemList = self.read(fileObj, Map)
    
    #Fix!    
    def read(self, fileObj, Map):
        el = [0] * 1000
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
                s += '    ' * depth + '[' + str(i) + ']: ' + e.__repr__(depth + 1) 
        return s

class MEventCommands(object):
    CommandModule = Command
    CommandMetaClass = CommandModule.CommandHandler
    EndHandler = CommandModule.Empty
    HandlersDict = {}
    
    @staticmethod
    def installHandlersDict():
        CM = MEventCommands.CommandModule
        CMC = MEventCommands.CommandMetaClass
        HD = MEventCommands.HandlersDict
        for e in dir(CM):
            name = eval(CM.__name__ + '.' + e)
            if isinstance(name, type):
                if issubclass(name, CMC) and name != CMC:
                    HD[name.CCode] = name

    def __init__(self, fileObj, Map, size = 0):
        self.CommandList, self.UnsolvedData = self.read(fileObj, Map, size)
        
    
    def read(self, fileObj, Map, size):
        start = fileObj.tell() 
        CL = list()
        UD = ''
        while True:
            CCode = getFNum(fileObj)           
            if self.HandlersDict.has_key(CCode):
                h = self.HandlersDict[CCode]()
                h.read(fileObj)
                CL.append(h)
                if isinstance(h, self.EndHandler): break
            else:
                readbytes = fileObj.tell() - start
                UD = fileObj.read(size - readbytes)
                break
        
        return CL, UD
                
            
    def __repr__(self, depth = 0):
        s = '\n'
        for e in self.CommandList:
            s += e.__repr__(depth + 1)
        
        s += strInHex(self.UnsolvedData)
        return s        
        
    
MEventCommands.installHandlersDict()
        


#MMap    <= (Type, {})
#MStruct <= {'ID': (Type, 'Name', {})}
#MBlock  <= ()
#MEnum <= ('Meaning 0', 'Meaning 1', 'Meaning 2')
#MList   <= (Type, {})

#Map.Events[1].Name
#Map.Events[1].Pages[2].CodeBlock

EventCommands = ()

EventConditions = {'\x01': (MBitMap,'BitMap',()), #От младшего к старшему : Switch1 .. Timer
                   '\x02': (MNum,'Switch1',()), #default: 1
                   '\x03': (MNum,'Switch2',()), #default: 1
                   '\x04': (MNum,'Variable',()), #default: 1
                   '\x05': (MNum,'Operand',()), #default: 0  !Fix: Может быть отрицательным, еще не поддерживается
                   '\x06': (MNum,'Item',()), #default: 1
                   '\x07': (MNum,'Hero',()), 
                   '\x08': (MNum,'Timer',()), #default: 0 Хранится в секундах
                  }

EventPage =  (MStruct, {'\x02': (MStruct,'EventConditions', EventConditions),
                        '\x15': (MString,'TilePath',()),
                        '\x16': (MBlock,'TileNum',()), #default: 0x00 #See TileNum.png
                        '\x17': (MEnum,'FaceDirection',('Up','Right','Down','Left')),
                        '\x18': (MEnum,'Pattern',('LEFT','MIDDLE', 'RIGHT')), #default: 0x01
                        '\x19': (MFlag,'Transp.',()),
                        '\x1f': (MEnum,'MovementType',('StayStill','RandomMovement', "CycleUp-Down",
                                                       "CycleLeft-Right-Down",'StepTowardHero',
                                                       'StepAwayFromHero', "ByItsRoute")),                        
                        '\x20': (MBlock,'Frequency',()), #default: 0x03
                        '\x21': (MEnum,'EventStartCondition',('PushKey', 'OnHeroTouch', 'OnTouch',
                                                              'AutoStart', 'ParallelProcess')),
                        '\x22': (MEnum,'Position',('BelowHero','SameLevelAsHero', 'OverHero')),
                        '\x23': (MFlag,'AllowEventOverLap',()),
                        '\x24': (MEnum,'AnimationType',('Common/WithoutStepping', 'Common/WithStepping',
                                                        'WithoutStepping', 'FixedDirection', 'FixedGraphic',
                                                        'TurnRight')),
                        '\x25': (MEnum,'Speed',('','x8Slower', 'x4Slower', 'x2Slower', 'Normal', #default: 0x03
                                                'x2Faster', 'x4Faster')),
                        '\x33': (MBlock,'CommandsLenght',()),
                        '\x34': (MEventCommands,'EventCommands',()),
                       }
             )

Event = (MStruct, {'\x01': (MString,'Name',()),
                   '\x02': (MNum,'X',()), #default: 0x00
                   '\x03': (MNum,'Y',()), #default: 0x00
                   '\x05': (MList,'Pages',EventPage),

                  }
         )


MapMap =  (MStruct, {'\x01': (MBlock,'ChipSet',()), #default: 0x01
                     '\x02': (MNum,'X',()), #default: 20
                     '\x03': (MNum,'Y',()), #default: 15
                     '\x0b': (MEnum,'ScrollType',('None', 'VerticalLoop', 'HorizontalLoop', 'BothLoop')),                     
                     '\x1f': (MFlag,'UseParralaxBackground',()), #default: 0x00
                     '\x20': (MString,'BackgroundPath',()),
                     '\x21': (MFlag,'HorizontalPan',()), #default: 0x00 
                     '\x22': (MFlag,'VerticalPan',()), #default: 0x00
                     '\x23': (MFlag,'HorizontalAutoScroll',()), #default: 0x00 
                     '\x24': (MNum,'HorizontalSpeed',()),
                     '\x25': (MNum,'VerticalAutoScroll',()), #default: 0x00 
                     '\x26': (MBlock,'VerticalSpeed',()),   
                     '\x47': (MBlock,'LoTaleSet',()),
                     '\x48': (MBlock,'UpTaleSet',()),
                     '\x51': (MList,'Events', Event), #default: Empty
                     '\x5b': (MNum,'SaveCount',())
                    }
           )
               


if __name__ == '__main__':
    def replacer(S):
        S = S.replace('ce 7e 00 03 61 62 63 00', 'ShowMessage:abc,d=0')
        S = S.replace('ce 7e 01 03 61 62 63 00', 'ShowMessage:abc,d=1')
        S = S.replace('03 61 61 61', 'aaa')
        S = S.replace('03 62 62 62', 'bbb')
        
        S = S.replace('cf 1c 00 07 61 61 61 2f 62 62 62 01 02', 'Case[aaa/bbb],d=0')
        S = S.replace('cf 1c 01 07 61 61 61 2f 62 62 62 01 02', 'Case[aaa/bbb],d=1')
        
        S = S.replace('0a 01 00 00', 'EmptyInCase,d=1')
        S = S.replace('0a 02 00 00', 'EmptyInCase,d=2')
        
        S = S.replace('81 9d 2c 00 aaa 01 00', 'Case: aaa,d=0')
        S = S.replace('81 9d 2c 01 aaa 01 00', 'Case: aaa,d=1')
        S = S.replace('81 9d 2c 00 bbb 01 01', 'Case: bbb,d=0')
        S = S.replace('81 9d 2c 01 bbb 01 01', 'Case: bbb,d=1')
                    
        S = S.replace('81 9d 2d 00 00 00', 'EndCase,d=0')
        S = S.replace('81 9d 2d 01 00 00', 'EndCase,d=1')
        
        S = S.replace('00 00 00 00', 'Empty')           
        return S
    
    f = open(targetFile, 'rb')
    signature = f.read(11)
    Map = MStruct(f, MapMap[1])
    ShowString = '{:<30}: {}'
    s1 = ShowString.format('2xshowMessage\'abc\'+end', Map.Events[3].Pages[1].EventCommands)
    s2 = ShowString.format('Case', Map.Events[3].Pages[2].EventCommands)
    s3 = ShowString.format('Empty Case', Map.Events[3].Pages[3].EventCommands)
    s1 = replacer(s1)
    s2 = replacer(s2)
    print Map.Events[3].Pages[2].EventCommands
    #s3 = replacer(s3)
#    print s1
#    print s2
#    print s3


