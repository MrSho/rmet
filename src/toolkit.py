'''
Created on 26.11.2012

@author: Sho
'''
'''
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
'''

def generate_handler_class(name, code, message, string_name, (var_name1, t), (var_name1, t)): pass