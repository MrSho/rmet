# coding: UTF-8
'''
Created on 24.11.2012

@author: Sho
'''
from misc import *

class CommandHandler(object):
    CCode = None
    
    def __init__(self, dep_lvl = 0, code_string = ''):
        self._code_string = code_string
        self._dep_lvl = dep_lvl
        self._string = ''
        self._numbers = []        
    
    def read(self, file_obj):
        self._dep_lvl = get_fnum(file_obj)
        srting_len = get_fnum(file_obj)
        self._string = file_obj.read(srting_len).decode(encoding='shift_jis_2004')
        numbers_count = get_fnum(file_obj)
        for i in xrange(numbers_count):
            self._numbers.append(get_fnum(file_obj))
    
    def __repr__(self, depth = 0): pass     
   

class Unknown(CommandHandler):
    
    def __repr__(self, depth = 0): 
        format_string = '{}<>Unknown: {} \'{}\'  n:{}  {}\n'
        format_list = list()    
        format_list.append(tab_token(depth + self._dep_lvl))
        
        format_list.append(str_in_hex(self._code_string))
        #format_list.append(str(self._dep_lvl)) 
        #format_list.append(str(len(self._string)))     
        format_list.append(self._string)
        
        format_list.append(str(len(self._numbers)))
        s = '{:>6}' * len(self._numbers)
        fl = list()
        for i in self._numbers:
            fl.append(str(i))
        format_list.append(s.format(*fl))                           
        return format_string.format(*format_list)    

    
class ShowMessage(CommandHandler):
    CCode = get_fnum_str('\xce\x7e')
    
    def __init__(self, dep_lvl = 0): 
        self._dep_lvl = dep_lvl
        self._message = ''
    
    def read(self, file_obj): 
        self._dep_lvl = get_fnum(file_obj)
        message_len = get_fnum(file_obj)
        message_bytes = file_obj.read(message_len)
        self._message = message_bytes.decode(encoding='shift_jis_2004')
        file_obj.read(1)        
    
    def __repr__(self, depth = 0):
        FString = '{}<>Messg:{}\n'
        return FString.format(tab_token(depth + self._dep_lvl), self._message)

    
class ShowMessageContinue(ShowMessage):
    CCode = get_fnum_str('\x81\x9d\x0e')       
    
    def __repr__(self, depth = 0):
        FString = '{}:      :{}\n'
        return FString.format(tab_token(depth + self._dep_lvl), self._message)  


#Unknown 2 bytes
class MessageStyle(CommandHandler):
    CCode = get_fnum_str('\xcf\x08')
    _window_format_enum = ('Normal', 'Transp')
    _window_position_enum = ('Top', 'Mid', 'Bot')
    _prevent_hero_enum = ('Fix', 'Auto')
    _allow_other_events_enum = ('Disable Event Move', 'Enable Event Move')
       
    def __init__(self, dep_lvl = 0):
        self._dep_lvl = dep_lvl
        self._window_format = 0
        self._window_position = 0
        self._prevent_hero = 0
        self._allow_other_events = 0
        
        self._data = '' 
        
    def read(self, file_obj): 
        self._dep_lvl = get_fnum(file_obj)
        file_obj.read(2)    #00 04 Нет строки и Далее 4 байта?
        self._window_format = get_fnum(file_obj)
        self._window_position = get_fnum(file_obj)
        self._prevent_hero = get_fnum(file_obj)
        self._allow_other_events = get_fnum(file_obj)
                      
    def __repr__(self, depth = 0):
        format_string = '{}<>Set Message Options:{},{},{},{}\n'
        format_list = list()
        format_list.append(tab_token(depth + self._dep_lvl))
        format_list.append(self._window_format_enum[self._window_format])
        format_list.append(self._window_position_enum[self._window_position])
        format_list.append(self._prevent_hero_enum[self._prevent_hero])
        format_list.append(self._allow_other_events_enum[self._allow_other_events])        
        return format_string.format(*format_list) 
        
class SelectFaceGraphic(CommandHandler):
    CCode = get_fnum_str('\xcf\x12')
    _display_pos_enum = ('Left', 'Right')
    _flip_enum = ('Normal', 'Mirrored')  
    
    def __init__(self, dep_lvl = 0):
        self._dep_lvl = dep_lvl
        self._pathlen = 0
        self._face_graphic_path = ''
        self._face_num = 0
        self._display_pos = 0
        self._flip = 0

        self._data = '' 
        
    def read(self, file_obj):
        self._dep_lvl = get_fnum(file_obj)
        self._pathlen = get_fnum(file_obj)
        face_graphic_bytes = file_obj.read(self._pathlen)
        self._face_graphic_path = face_graphic_bytes.decode(encoding='shift_jis_2004')
        file_obj.read(1) #03 Далее 3 байт?
        self._face_num = get_fnum(file_obj)
        self._display_pos = get_fnum(file_obj)
        self._flip = get_fnum(file_obj)
        
    def __repr__(self, depth = 0):
        if self._pathlen:
            format_string = '{}<>Select Face Graphic: {}, {}, {}, {}\n'
            format_list = list()                 
            format_list.append(tab_token(depth + self._dep_lvl))
            format_list.append(self._face_graphic_path)
            format_list.append(str(self._face_num + 1))
            format_list.append(self._display_pos_enum[self._display_pos])
            format_list.append(self._flip_enum[self._flip])
            return format_string.format(*format_list)
        else:
            format_string = '{}<>Select Face Graphic: Eras\n'
            format_list = list()                 
            format_list.append(tab_token(depth + self._dep_lvl))
            return format_string.format(*format_list)                                         
  
class ShowChoise(CommandHandler):
    CCode = get_fnum_str('\xcf\x1c')
    
    def __init__(self, dep_lvl = 0):
        self._dep_lvl = dep_lvl
        self._case_message = ''
        self._unk1 = 0
        self._cancel_case  = 0
    
    def read(self, file_obj):
        self._dep_lvl = get_fnum(file_obj)
        message_len = get_fnum(file_obj)
        message_bytes = file_obj.read(message_len)
        self._case_message = message_bytes.decode(encoding='shift_jis_2004')
        self._unk1 = file_obj.read(1)
        self._cancel_case = file_obj.read(1)
    
    def __repr__(self, depth = 0):
        FString = '{}<>Show Choise: {} C:{}\n' 
        return FString.format(tab_token(depth + self._dep_lvl), self._case_message, str_in_hex(self._cancel_case))


class Case(CommandHandler):
    CCode = get_fnum_str('\x81\x9d\x2c')
    
    def __init__(self, dep_lvl = 0):
        self._dep_lvl = dep_lvl
        self._case_message = ''
        self._unk1 = 0
        self._case_num = 0       
    
    def read(self, file_obj):
        self._dep_lvl = get_fnum(file_obj)
        message_len = get_fnum(file_obj)
        message_bytes = file_obj.read(message_len)
        self._case_message = message_bytes.decode(encoding='shift_jis_2004')
        self._unk1 = file_obj.read(1)
        self._case_num = get_fnum(file_obj)                       
    
    def __repr__(self, depth = 0): 
        format_string = '{}: [{}] Case\n'
        if self._case_num == 4:
            message = 'CANCEL'
        else:
            message = self._case_message
        return format_string.format(tab_token(depth + self._dep_lvl), message) 

    
class EndCase(CommandHandler):
    CCode = get_fnum_str('\x81\x9d\x2d')
    
    def __init__(self, dep_lvl = 0):
        self._dep_lvl = dep_lvl
    
    def read(self, file_obj):
        self._dep_lvl = get_fnum(file_obj)
        file_obj.read(2)
    
    def __repr__(self, depth = 0):
        return tab_token(depth + self._dep_lvl) + ':END Case\n'


class CaseEmpty(CommandHandler):
    CCode = get_fnum_str('\x0a')
    
    def __init__(self, dep_lvl = 0):
        self._dep_lvl = dep_lvl
    
    def read(self, file_obj):
        self._dep_lvl = get_fnum(file_obj)
        file_obj.read(2)
    
    def __repr__(self, depth = 0):
        return tab_token(depth + self._dep_lvl) + '<>\n'     


#NEED VAR
class InputNumber(CommandHandler):
    CCode = get_fnum_str('\xcf\x26')
    
    def __init__(self, dep_lvl = 0):
        self._dep_lvl = dep_lvl
        self._digit_num = 0
        self._variable = 0
    
    def read(self, file_obj):
        self._dep_lvl = get_fnum(file_obj)
        get_fnum(file_obj)
        file_obj.read(1) #02 прочитать два _числа_?
        self._digit_num = get_fnum(file_obj)
        self._variable = get_fnum(file_obj) 
        
    def __repr__(self, depth = 0):    
        format_string = '{}<>Input Number: {} Dg.[{}:{}]\n'
        format_list = list()
        format_list.append(tab_token(depth + self._dep_lvl))
        format_list.append(str(self._digit_num))
        format_list.append(str(self._variable))
        format_list.append(get_MVar_name(self._variable))                  
        return format_string.format(*format_list)
    

class ChangeSwitch(CommandHandler):
    CCode = get_fnum_str('\xcf\x62')
    _set_enum = ('ON Set', 'OFF Set', 'ON/OFF Triger')
    
    def __init__(self):
        CommandHandler.__init__(self)
        self._exprtype = 0
        self._v1 = 0
        self._v2 = 0
        self._set = 0
      
    def read(self, file_obj):
        CommandHandler.read(self, file_obj)
        self._exprtype = self._numbers[0]
        self._v1 = self._numbers[1]        
        self._v2 = self._numbers[2] 
        self._set = self._numbers[3]

    def __repr__(self, depth = 0):
        format_list = list()
        format_list.append(tab_token(depth + self._dep_lvl))
        if   self._exprtype == 0:
            format_string = '{}<>Change Switch: [{}:{}]-{}\n'
            format_list.append(str(self._v1))
            format_list.append(get_MSwitch_name(self._v1))
            format_list.append(self._set_enum[self._set])                        
        elif self._exprtype == 1:
            format_string = '{}<>Change Switch: [{}*{}]-{}\n'
            format_list.append(str(self._v1))            
            format_list.append(str(self._v2))
            format_list.append(self._set_enum[self._set])                           
        elif self._exprtype == 2:
            format_string = '{}<>Change Switch: [V[{}:{}]]-{}\n'
            format_list.append(str(self._v1))            
            format_list.append(get_MVar_name(self._v1))
            format_list.append(self._set_enum[self._set]) 
                    
        return format_string.format(*format_list)


class ChangeVariable(CommandHandler):
    CCode = get_fnum_str('\xcf\x6c')
    _settype_enum = ('Set', '+', '-', '*', '/', 'Mod')
    
    def __init__(self):
        CommandHandler.__init__(self)
        self._vartype = 0
        self._targetvar1 = 0
        self._targetvar2 = 0
        self._settype = 0
        self._operandtype = 0
        self._operand1 = 0
        self._operand2 = 0
        
    def read(self, file_obj):
        CommandHandler.read(self, file_obj)
        self._vartype = self._numbers[0]
        self._targetvar1 = self._numbers[1]
        self._targetvar2 = self._numbers[2]
        self._settype = self._numbers[3]
        self._operandtype = self._numbers[4]
        self._operand1 = self._numbers[5]
        self._operand2 = self._numbers[6]
        
    def __repr__(self, depth = 0):
        sformat_list = list()
        sformat_list.append(tab_token(depth + self._dep_lvl))
        sformat_string = '{}<>Variable Ch:{} {}, {}\n'
        
        vformat_list = list()       
        if self._vartype == 0:
            vformat_string = '[{}:{}]'
            vformat_list.append(str(self._targetvar1))
            vformat_list.append(get_MVar_name(self._targetvar1))
        elif self._vartype == 1:
            vformat_string = '[{}*{}]'
            vformat_list.append(str(self._targetvar1))
            vformat_list.append(str(self._targetvar2))
        elif self._vartype == 2:
            vformat_string = '[V[{}]]'
            vformat_list.append(str(self._targetvar1))
        sformat_list.append(vformat_string.format(*vformat_list))
        
        sformat_list.append(self._settype_enum[self._settype])
        
        oformat_list = list()
        if self._operandtype == 0:
            oformat_string = '{}'
            oformat_list.append(str(self._operand1))
        elif self._operandtype == 1:
            oformat_string = 'Var.[{}]val'
            oformat_list.append(str(self._operand1))
        elif self._operandtype == 2:
            oformat_string = 'Var.[V[{}]]val'
            oformat_list.append(str(self._operand1))
        elif self._operandtype == 3:
            oformat_string = 'Randm[{}*{}]'
            oformat_list.append(str(self._operand1))
            oformat_list.append(str(self._operand2))                    
        elif self._operandtype == 4:
            oformat_string = '{} - {}'
            oformat_list.append(str(self._operand1))
            oformat_list.append(str(self._operand2)) 
        elif self._operandtype == 5:
            oformat_string = '{} - {}'
            oformat_list.append(str(self._operand1))
            oformat_list.append(str(self._operand2)) 
        elif self._operandtype == 6:
            oformat_string = '{} - {}'
            oformat_list.append(str(self._operand1))
            oformat_list.append(str(self._operand2)) 
        elif self._operandtype == 7:
            oformat_string = '{}'
            oformat_list.append(str(self._operand1))
        sformat_list.append(oformat_string.format(*oformat_list))            
        
        return sformat_string.format(*sformat_list)

        
class TimerOperations(CommandHandler):
    CCode = get_fnum_str('\xcf\x76')
    _settype_enum = ('Create', 'StartTmr', 'StopTmr')

    def __init__(self):
        CommandHandler.__init__(self)
        self._settype = 0
        self._operandtype = 0
        self._operand = 0
        self._displaytimer = 0
        self._availableinbattle = 0

    def read(self, file_obj):
        CommandHandler.read(self, file_obj)
        self._settype = self._numbers[0]
        self._operandtype = self._numbers[1]
        self._operand = self._numbers[2]
        self._displaytimer = self._numbers[3]
        self._availableinbattle = self._numbers[4]

    def __repr__(self, depth = 0):
        format_list = list()
        format_list.append(tab_token(depth + self._dep_lvl))
        format_string = '{}<>Timer Operation:{}\n'
        format_list.append(self._settype_enum[self._settype])
        if self._settype == 0:
            format_string = '{}<>Timer Operation:{} {}\n'
            if not self._operandtype:
                format_list.append(str(self._operand) + ' sec')
            else:
                format_list.append('V[' + str(self._operand) + ']')
                            
        elif self._settype == 1:
            format_string = '{}<>Timer Operation:{} {} {}\n'
            format_list.append(str(self._displaytimer))
            format_list.append(str(self._availableinbattle))
        return format_string.format(*format_list)

                   
class ChangeMoney(CommandHandler):
    CCode = get_fnum_str('\xd0\x46')
    _settype_enum = ('Incr.', 'Decr.')

    def __init__(self):
        CommandHandler.__init__(self)
        self._settype = 0
        self._operandtype = 0
        self._var = 0

    def read(self, file_obj):
        CommandHandler.read(self, file_obj)
        self._settype = self._numbers[0]
        self._operandtype = self._numbers[1]
        self._var = self._numbers[2]

    def __repr__(self, depth = 0):
        format_list = list()
        format_list.append(tab_token(depth + self._dep_lvl))
        if self._operandtype:
            format_string = '{}<>Change Money: Money V[{}] {} \n'
        else:
            format_string = '{}<>Change Money: Money {} {} \n'
        format_list.append(str(self._var))
        format_list.append(self._settype_enum[self._settype])
        return format_string.format(*format_list)


class ChangeItem(CommandHandler):
    CCode = get_fnum_str('\xd0\x50')
    _settype_enum = ('Incr.', 'Decr.')

    def __init__(self):
        CommandHandler.__init__(self)
        self._settype = 0
        self._itemtype = 0
        self._item = 0
        self._operandtype = 0
        self._operand = 0

    def read(self, file_obj):
        CommandHandler.read(self, file_obj)
        self._settype = self._numbers[0]
        self._itemtype = self._numbers[1]
        self._item = self._numbers[2]
        self._operandtype = self._numbers[3]
        self._operand = self._numbers[4]

    def __repr__(self, depth = 0):
        format_list = list()
        format_list.append(tab_token(depth + self._dep_lvl))
        format_string = '{}<>Add/Remove Item:{}->{} {}\n'
        if not self._itemtype:
            format_list.append(get_Item_name(self._item))
        else:
            format_list.append('V[{}]'.format(str(self._item)))
        if not self._operandtype:
            format_list.append(str(self._operand))
        else:
            format_list.append('V[{}]'.format(str(self._operand)))
        format_list.append(self._settype_enum[self._settype])
        return format_string.format(*format_list)


class ChangeParty(CommandHandler):
    CCode = get_fnum_str('\xd0\x5a')
    _settype_enum = ('Add', 'Remv')

    def __init__(self):
        CommandHandler.__init__(self)
        self._settype = 0
        self._operandtype = 0
        self._operand = 0

    def read(self, file_obj):
        CommandHandler.read(self, file_obj)
        self._settype = self._numbers[0]
        self._operandtype = self._numbers[1]
        self._operand = self._numbers[2]

    def __repr__(self, depth = 0):
        format_list = list()
        format_list.append(tab_token(depth + self._dep_lvl))
        format_string = "{}<>Change Hero's Party:{}->{}\n"
        if not self._operandtype:
            format_list.append(get_Hero_name(self._operand))
        else:
            format_list.append('V[{}]'.format(str(self._operand)))
        format_list.append(self._settype_enum[self._settype])
        return format_string.format(*format_list)


class ChangeExp(CommandHandler):
    CCode = get_fnum_str('\xd1\x2a')
    _settype_enum = ('Incr.', 'Decr.')    

    def __init__(self):
        CommandHandler.__init__(self)
        self._targettype = 0
        self._target = 0
        self._settype = 0
        self._operandtype = 0
        self._operand = 0
        self._showlvlmessg = 0

    def read(self, file_obj):
        CommandHandler.read(self, file_obj)
        self._targettype = self._numbers[0]
        self._target = self._numbers[1]
        self._settype = self._numbers[2]
        self._operandtype = self._numbers[3]
        self._operand = self._numbers[4]
        self._showlvlmessg = self._numbers[5]

    def __repr__(self, depth = 0):
        format_list = list()
        format_list.append(tab_token(depth + self._dep_lvl))
        format_string = '{}<>Change EXP: {:<15} EXP {:>10} {} {}\n'
        if self._targettype == 0:
            format_list.append('All Members')
        elif self._targettype == 1:
            format_list.append(get_Hero_name(self._target))
        elif self._targettype == 2:
            format_list.append('V[{}]'.format(str(self._target)))
        
        if not self._operandtype:
            format_list.append(str(self._operand))
        else:
            format_list.append('V[{}]'.format(str(self._operand)))
            
        format_list.append(self._settype_enum[self._settype])
        if self._showlvlmessg:
            format_list.append('Show')
        else:
            format_list.append('')
        return format_string.format(*format_list)
        

class CallEvent(CommandHandler):
    CCode = get_fnum_str('\xe0\x2a')
    
    def __init__(self):
        CommandHandler.__init__(self)
        self._calltype = 0
        self._event = 0
        self._page = 0
        
    def read(self, file_obj):
        CommandHandler.read(self, file_obj)
        self._calltype = self._numbers[0]
        self._event = self._numbers[1]
        self._page = self._numbers[2]

    def __repr__(self, depth = 0):
        format_list = list()
        format_list.append(tab_token(depth + self._dep_lvl))
        if   self._calltype == 0:
            format_string = '{}<>Call Event: {}:{}\n'
            format_list.append(self._event)
            format_list.append(get_MCEvent_name(self._event))
        elif self._calltype == 1:
            format_string = '{}<>Call Event: {}[{}]\n'
            format_list.append(str(self._event))
            format_list.append(str(self._page))
        elif self._calltype == 2:
            format_string = '{}<>Call Event: V[{}]:{}[V[{}]:{}]\n'
            format_list.append(str(self._event))
            format_list.append(get_MVar_name(self._event))
            format_list.append(str(self._page))
            format_list.append(get_MVar_name(self._page))            
        return format_string.format(*format_list)                                         
    
               
class Empty(CommandHandler):
    CCode = get_fnum_str('\x00')
    
    def __init__(self, dep_lvl = 0):
        self._dep_lvl = dep_lvl
    
    def read(self, file_obj):
        self._dep_lvl = get_fnum(file_obj)
        file_obj.read(2)        
    
    def __repr__(self, depth = 0):
        return tab_token(depth + self._dep_lvl) + '<>\n'