# coding: UTF-8
'''
Created on 24.11.2012

@author: Sho
'''
from misc import get_fnum, get_fnum_str, str_in_hex, tab_token, get_MVar_name

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
        format_string = '{}<>Unknown: {}  d:{}  sl:{} \'{}\'  nc:{}  {}\n'
        format_list = list()    
        format_list.append(tab_token(depth + self._dep_lvl))
        
        format_list.append(str_in_hex(self._code_string))
        format_list.append(str(self._dep_lvl)) 
        format_list.append(str(len(self._string)))     
        format_list.append(self._string)
        
        format_list.append(str(len(self._numbers)))
        s = str()
        for i in self._numbers:
            s += str(i) + ' '
        format_list.append(s)                           
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
           
class Empty(CommandHandler):
    CCode = get_fnum_str('\x00')
    
    def __init__(self, dep_lvl = 0):
        self._dep_lvl = dep_lvl
    
    def read(self, file_obj):
        self._dep_lvl = get_fnum(file_obj)
        file_obj.read(2)        
    
    def __repr__(self, depth = 0):
        return tab_token(depth + self._dep_lvl) + '<>\n'