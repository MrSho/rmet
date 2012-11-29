#coding: UTF-8
'''
Created on 26.11.2012

@author: Sho
'''

int = 0
enum = 1

def generate_handler_class(name, code, message, string_name, *vars):
    indent = '    ' 
    print 'class {}(CommandHandler):'.format(name)
    print indent + 'CCode = get_fnum_str(\'{}\')'.format(code)
    for varname, vartype in vars:
        if vartype == enum:
            print indent + '_{}_enum = (\'\', \'\')'.format(varname)
    print
    print indent + 'def __init__(self):'
    print indent * 2 + 'CommandHandler.__init__(self)'
    if string_name:
        print indent * 2 + 'self._{} = \'\''.format(string_name)
    for varname, vartype in vars:
        print indent * 2 + 'self._{} = 0'.format(varname)
    print
    print indent + 'def read(self, file_obj):'
    print indent * 2 + 'CommandHandler.read(self, file_obj)' 
    if string_name:
        print indent * 2 + 'self._{} = self._string'.format(string_name)
    for i, e in enumerate(vars):
        varname = e[0]
        vartype = e[1]
        print indent * 2 + 'self._{} = self._numbers[{}]'.format(varname, str(i))
    print
    print indent + 'def __repr__(self, depth = 0):'
    print indent * 2 + 'format_list = list()'
    print indent * 2 + 'format_list.append(tab_token(depth + self._dep_lvl))'
    print indent * 2 + "format_string = '{}" + '<>{}:'.format(message) + \
         '{} ' * (len(vars) + bool(string_name)) + "'\\n"
    print
    if string_name:
        print indent * 2 + 'format_list.append(self._{})'.format(string_name)
    print
    for varname, vartype in vars:
        if vartype == enum:
            print indent * 2 + 'format_list.append(self._{}_enum[self._{}])'\
                .format(varname, varname)
        else:
            print indent * 2 + 'format_list.append(str(self._{}))'.format(varname)
    print indent * 2 + 'return format_string.format(*format_list)'