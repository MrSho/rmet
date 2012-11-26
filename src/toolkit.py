'''
Created on 26.11.2012

@author: Sho
'''

class MessageStyle(CommandHandler):
    CCode = get_fnum_str('\xcf\x08')
    _window_format_enum = ()
    _window_position_enum = ()
    _prevent_hero_enum = ()
    _allow_other_events_enum = ()
       
    def __init__(self, dep_lvl = 0):
        self._dep_lvl = dep_lvl
        self._window_format = 0
        self._window_position = 0
        self._prevent_hero = 0
        self._allow_other_events = 0
        
        self._data = '' 
        
    def read(self, file_obj): 
        self._dep_lvl = get_fnum(file_obj)
        self._data = file_obj.read(6)   
             
     
    def __repr__(self, depth = 0):
        format_string = u'{}<>Set Message Options: {}\n'
        format_list = list()
        format_list.append(tab_token(depth + self._dep_lvl))
        format_list.append(self._data)
        #format_list.append(self._window_format_enum[self._window_format])
        return format_string.format(*format_list)


def generate_handler_class(name, size, message): pass