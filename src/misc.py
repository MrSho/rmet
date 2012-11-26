# coding: UTF-8
'''
Created on 25.11.2012

@author: Sho
'''
import struct
import StringIO

HexRepr = 1 #0 - with 0x, 1 - without 0x


#Читает закодированное число
#!Fix : Есть отрицательные числа!!!   
def get_fnum(file_obj, summ = 0):
    b = struct.unpack('B', file_obj.read(1))[0]
    if 0b10000000 & b:
        return get_fnum(file_obj, summ * 0x80 + (0b01111111 & b))
    else:
        return summ * 0x80 + (0b01111111 & b)

    
def get_fnum_str(string):
    SI = StringIO.StringIO(string)
    return get_fnum(SI)

#Читает закодированное число
#!Fix : Есть отрицательные числа!!! 
def get_fnum_count(file_obj, summ = 0, string = ''):
    c = file_obj.read(1)
    b = struct.unpack('B', c)[0]
    string += c
    if 0b10000000 & b:
        return get_fnum_count(file_obj, summ * 0x80 + (0b01111111 & b), string)
    else:
        return (summ * 0x80 + (0b01111111 & b), string)

#Возвращает шестнадцатиричное представление для
#для последовательности байтов в виде строки  
def str_in_hex(string):
    if HexRepr:    
        s = str()
        for i in string:
            c = struct.unpack('B', i)[0]
            c = hex(c).replace('0x', '')
            if len(c) == 1: c = '0' + c
            s += ' ' + c
        return s.strip()
    else:
        s = str()
        for i in string:
            c = struct.unpack('B', i)[0]
            c = hex(c)
            if len(c) == 3: c = c.replace('0x', '0x0')
            s += ' ' + c
        return s.strip()    


#Fix!: Добавить во все месте, где используется отступы
def tab_token(depth):
    return u'    ' * depth
    

def get_MVar_name(id): return u''

def get_MSwitch_name(id): return u''




if __name__ == '__main__':
    pass