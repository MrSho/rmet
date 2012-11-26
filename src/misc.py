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
def get_fnum(fileObj, summ = 0):
    b = struct.unpack('B', fileObj.read(1))[0]
    if 0b10000000 & b:
        return get_fnum(fileObj, summ * 0x80 + (0b01111111 & b))
    else:
        return summ * 0x80 + (0b01111111 & b)

    
def get_fnum_str(Str):
    SI = StringIO.StringIO(Str)
    return get_fnum(SI)


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
    return '    ' * depth
    

if __name__ == '__main__':
    pass