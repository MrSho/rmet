# coding: UTF-8
'''
Created on 24.11.2012

@author: Sho
'''
from misc import get_fnum, get_fnum_str, str_in_hex, tab_token

class CommandHandler(object):
    CCode = None
    
    def __init__(self, Dlvl): pass
    
    def read(self, file_obj): pass
    
    def __repr__(self, depth = 0): pass     
   
    
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
    
class ShowChoise(CommandHandler):
    CCode = get_fnum_str('\xcf\x1c')
    
    def __init__(self, Dlvl = 0):
        self._dep_lvl = Dlvl
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
    
class Empty(CommandHandler):
    CCode = get_fnum_str('\x00')
    
    def __init__(self, dep_lvl = 0):
        self._dep_lvl = dep_lvl
    
    def read(self, file_obj):
        self._dep_lvl = get_fnum(file_obj)
        file_obj.read(2)        
    
    def __repr__(self, depth = 0):
        return tab_token(depth + self._dep_lvl) + '<>\n'