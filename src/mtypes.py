# coding: UTF-8
'''
Created on 26.11.2012

@author: Sho

К любому из объектов структуры карт или бд можно применить repr(), которая выведет
представление всех потомков в иерархическом виде.
'''
from misc import *
import command

reprLen = 120

#------Объекты-типы------
class MBlock(object):
    
    def __init__(self, file_obj, map, size=0):
        self._data = self.read(file_obj, size)
        self._map = map
        
    def read(self, file_obj, size):
        return file_obj.read(size)
    
    def __repr__(self, depth=0):
        return str_in_hex(self._data[:reprLen])

    
class MString(MBlock):
     
    def __repr__(self, depth=0):
        return self._data.decode(encoding='shift_jis_2004')

    
class MEnum(MBlock):
    
    def __repr__(self, depth=0):
        b = struct.unpack('B', self._data[0])[0]
        try:
            return self._map[b]
        except:
            return str_in_hex(self._data[:reprLen])

        
class MFlag(MBlock):
     
    def __repr__(self, depth=0):
        return repr(bool(struct.unpack('B', self._data[0])[0]))

    
class MNum(MBlock):
    
    def __repr__(self, depth=0):
        return repr(get_fnum_str(self._data))


class MBitMap(MBlock):
    
    def __repr__(self, depth=0):
        return bin(get_fnum_str(self._data))        


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
            return str_in_hex(ID)
        
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
    
    def __init__(self, file_obj, map, size=0):
        self._map = map
        self._blockDict = self.read(file_obj, map)
       
    def read(self, file_obj, map):
        bd = {}
        while True:
            ID = file_obj.read(1)
            if ID == '\x00' or ID == '': break            
            #Определяется
            size = get_fnum(file_obj)
            #print 'Reading segment id={}, size={}, offset={}'.format(str_in_hex(ID),
            #                                     str(size), str(file_obj.tell()))
            b = MStruct.getType(ID, map)(file_obj, MStruct.getAnsMap(ID, map), size)
            Name = MStruct.IDtoName(ID, map)
            bd[ID] = b
            setattr(self, Name, b) 
            
        return bd
    
    def __repr__(self, depth=0):
        s = '\n'
        for id, b in sorted(self._blockDict.items()):
            id = MStruct.IDtoNameRepr(id, self._map)
            s += '    ' * depth + id + ': ' + b.__repr__(depth + 1) + '\n' 
        return s
      

class MList(object):
    
    #MList   <= (Type, {})            
    def __init__(self, file_obj, map, size=0):
        self._elemList = self.read(file_obj, map)
    
    #Fix!    
    def read(self, file_obj, map):
        el = [0] * 5001
        c = get_fnum(file_obj)
        for i in xrange(c):
            n = get_fnum(file_obj)
            el[n] = map[0](file_obj, map[1])
                          
        return el
    
    def __getitem__(self, key):
        return self._elemList[key]
    
    def get_elist(self):
        el = list()
        for i, e in enumerate(self._elemList):
            if not isinstance(e, int):
                el.append((i, e))
        return el
    
    def key_search(self, key, match):
        'Ищет элементы в списке равные match по их полю key'
        found_match = list()
        for e in self._elemList:
            try:
                if repr(getattr(e, key)) == match:
                    found_match.append(e)
            except AttributeError: pass
        return found_match
            
    
    def __repr__(self, depth=0):
        s = '\n'
        for i, e in enumerate(self._elemList):
            if e:
                s += '    ' * depth + '[' + str(i) + ']: ' + e.__repr__(depth + 1) 
        return s


class MEventCommands(object):
    command_module = command
    command_meta_class = command_module.CommandHandler
    default_handler = command_module.Unknown
    end_handler = command_module.Empty
    handlers_dict = {}
    
    @staticmethod
    def installHandlersDict():
        CM = MEventCommands.command_module
        CMC = MEventCommands.command_meta_class
        HD = MEventCommands.handlers_dict
        for e in dir(CM):
            name = eval(CM.__name__ + '.' + e)
            if isinstance(name, type):
                if issubclass(name, CMC) and name != CMC:
                    HD[name.CCode] = name

    def __init__(self, file_obj, map, size=0):
        self._command_list, self._unsolved_data = self.read(file_obj, map, size)
           
    def read(self, file_obj, map, size):
        start = file_obj.tell() 
        CL = list()
        UD = ''
        while True:
            CCode, code_string = get_fnum_count(file_obj)           
            if self.handlers_dict.has_key(CCode):
                h = self.handlers_dict[CCode]()
                h.read(file_obj)
                CL.append(h)
                if isinstance(h, self.end_handler): break
            else:
                h = self.default_handler(0, code_string)
                h.read(file_obj)
                CL.append(h)                
                #readbytes = file_obj.tell() - start
                #UD = code_string + file_obj.read(size - readbytes)
                #break
        
        return CL, UD
    
    #Вручную убить интенды
    def find_all_commands(self, command_class):
        "возращает список команд интансированных от command_class c их номерами"
        found_commands = list()
        for line, c in enumerate(self._command_list):
            if isinstance(c, command_class):
                found_commands.append((line, c))
        return found_commands
    
    
    def get_commands_by_frequency(self):
        return tuple(tuple('number_of_use', 'command'))
            
    def __repr__(self, depth=0):
        s = '\n'
        for e in self._command_list:
            s += e.__repr__(depth + 1)
        
        s += str_in_hex(self._unsolved_data)
        return s        
        
    
MEventCommands.installHandlersDict()
        
#------Карты файлов------
#Являются вложеннымии списками и словарями
#Описывают структуру файлов карт и бд через взаимоотношения объектов-типов

#MStruct <= {'ID': (Type, 'Name', {})}
#MBlock  <= ()
#MEnum <= ('Meaning 0', 'Meaning 1', 'Meaning 2')
#MList   <= (Type, {})

#Пример использования структуры файла
#_map.Events[1].Name
#_map.Events[1].Pages[2].EventCommands

EventCommands = ()

EventConditions = {'\x01': (MBitMap, 'BitMap', ()), #От младшего к старшему : Switch1 .. Timer
                   '\x02': (MNum, 'Switch1', ()), #default: 1
                   '\x03': (MNum, 'Switch2', ()), #default: 1
                   '\x04': (MNum, 'Variable', ()), #default: 1
                   '\x05': (MNum, 'Operand', ()), #default: 0  !Fix: Может быть отрицательным, еще не поддерживается
                   '\x06': (MNum, 'Item', ()), #default: 1
                   '\x07': (MNum, 'Hero', ()),
                   '\x08': (MNum, 'Timer', ()), #default: 0 Хранится в секундах
                  }

EventPage = (MStruct, {'\x02': (MStruct, 'EventConditions', EventConditions),
                        '\x15': (MString, 'TilePath', ()),
                        '\x16': (MBlock, 'TileNum', ()), #default: 0x00 #See TileNum.png
                        '\x17': (MEnum, 'FaceDirection', ('Up', 'Right', 'Down', 'Left')),
                        '\x18': (MEnum, 'Pattern', ('LEFT', 'MIDDLE', 'RIGHT')), #default: 0x01
                        '\x19': (MFlag, 'Transp.', ()),
                        '\x1f': (MEnum, 'MovementType', ('StayStill', 'RandomMovement', "CycleUp-Down",
                                                       "CycleLeft-Right-Down", 'StepTowardHero',
                                                       'StepAwayFromHero', "ByItsRoute")),
                        '\x20': (MBlock, 'Frequency', ()), #default: 0x03
                        '\x21': (MEnum, 'EventStartCondition', ('PushKey', 'OnHeroTouch', 'OnTouch',
                                                              'AutoStart', 'ParallelProcess')),
                        '\x22': (MEnum, 'Position', ('BelowHero', 'SameLevelAsHero', 'OverHero')),
                        '\x23': (MFlag, 'AllowEventOverLap', ()),
                        '\x24': (MEnum, 'AnimationType', ('Common/WithoutStepping', 'Common/WithStepping',
                                                        'WithoutStepping', 'FixedDirection', 'FixedGraphic',
                                                        'TurnRight')),
                        '\x25': (MEnum, 'Speed', ('', 'x8Slower', 'x4Slower', 'x2Slower', 'Normal', #default: 0x03
                                                'x2Faster', 'x4Faster')),
                        '\x33': (MBlock, 'CommandsLenght', ()),
                        '\x34': (MEventCommands, 'EventCommands', ()),
                       }
             )

Event = (MStruct, {'\x01': (MString, 'Name', ()),
                   '\x02': (MNum, 'X', ()), #default: 0x00
                   '\x03': (MNum, 'Y', ()), #default: 0x00
                   '\x05': (MList, 'Pages', EventPage),

                  }
         )


MapMap = (MStruct, {'\x01': (MBlock, 'ChipSet', ()), #default: 0x01
                     '\x02': (MNum, 'X', ()), #default: 20
                     '\x03': (MNum, 'Y', ()), #default: 15
                     '\x0b': (MEnum, 'ScrollType', ('None', 'VerticalLoop', 'HorizontalLoop', 'BothLoop')),
                     '\x1f': (MFlag, 'UseParralaxBackground', ()), #default: 0x00
                     '\x20': (MString, 'BackgroundPath', ()),
                     '\x21': (MFlag, 'HorizontalPan', ()), #default: 0x00 
                     '\x22': (MFlag, 'VerticalPan', ()), #default: 0x00
                     '\x23': (MFlag, 'HorizontalAutoScroll', ()), #default: 0x00 
                     '\x24': (MNum, 'HorizontalSpeed', ()),
                     '\x25': (MNum, 'VerticalAutoScroll', ()), #default: 0x00 
                     '\x26': (MBlock, 'VerticalSpeed', ()),
                     '\x47': (MBlock, 'LoTaleSet', ()),
                     '\x48': (MBlock, 'UpTaleSet', ()),
                     '\x51': (MList, 'Events', Event), #default: Empty
                     '\x5b': (MNum, 'SaveCount', ())
                    }
           )

HeroList = (MStruct, {'\x01': (MString, 'Name', ())
                      }
            )

SkillsList = (MStruct, {'\x01': (MString, 'Name', ())
                      }
            )

ItemList = (MStruct, {'\x01': (MString, 'Name', ())
                      }
            )

MonsterList = (MStruct, {'\x01': (MString, 'Name', ())
                      }
            )

MonsterPartyList = (MStruct, {'\x01': (MString, 'Name', ())
                             }
                   )

SwitchList = (MStruct, {'\x01': (MString, 'Name', ())
                      }
            )

VarsList = (MStruct, {'\x01': (MString, 'Name', ())
                      }
            )

CEventList = (MStruct, {'\x01': (MString, 'Name', ()),
                        '\x15': (MBlock, 'CommandsLenght', ()),
                        '\x16': (MEventCommands, 'EventCommands', ()),
                      }
            )

UnkStruct = (MStruct, {})



#Вычитаем 5
MapDB = (MStruct, {'\x0b': (MList, 'Hero', HeroList),
                   '\x0c': (MList, 'Skills', SkillsList),
                   '\x0d': (MList, 'Items', ItemList),
                   '\x0e': (MList, 'Monsters', MonsterList),
                   '\x0f': (MList, 'MonstersParty', MonsterPartyList),
                   '\x10': (MList, 'Terrain', UnkStruct),
                   '\x11': (MList, 'Attributes', UnkStruct),
                   '\x12': (MList, 'Conditions', UnkStruct),
                   '\x13': (MList, 'BattleAnimation', UnkStruct),
                   '\x14': (MList, 'ChipSets', UnkStruct),
                   '\x17': (MList, 'Switch', SwitchList),
                   '\x18': (MList, 'Vars', VarsList),
                   '\x19': (MList, 'CEvents', CEventList),
                   }
         )

#-----------------------


if __name__ == '__main__':
    pass