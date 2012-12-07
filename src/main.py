# coding: UTF-8
'''
Created on 20.11.2012

@author: Sho
'''

import os.path as path
import glob

import misc
import command
import mtypes


#------------------Глобальные Константы------------------
VHgamePath = u'D:/аниме/хентай/bestiality^monster^tentacles/!VH/my try/\
VHゲーム０１_121005_translated'
DBfileName = u'RPG_RT.ldb'

#------------------Вспомогательные Функции------------------      
def print_all_calls(M, event, page):
    '''Печатает все найденные command.CallEvent на карте map_obj(M),
     event_id(event), page_id(page)'''
    block = M.Events[event].Pages[page].EventCommands
    cl = block.find_all_commands(command.CallEvent)
    for i in cl:
        print i

        
def get_maps_list():
    'Возвращает список карт найденных в директории игры'
    return glob.glob1(VHgamePath, '*.lmu')





def save_str_to_file(filepath, str):
    'Сохраняет строку str в файл filepath'
    f = open(filepath, 'w')
    f.write(str)
    f.close()

    
def find_commands_DB(DB, command_class, **attr):
    '''Ищет в структуре базы данных DB команды command_class с атрибутами
    attr и печатает их в stdout. command_class и атрибуты смотреть в
    command.py'''
    for id, CEvent in DB.CEvents.get_elist():
        CL = CEvent.EventCommands.find_all_commands(command_class)
        for line, command in CL:
            for key, value in attr.items():
                try:
                    if not getattr(command, key) == value:
                        break
                except AttributeError:
                    break
            else:
                print 'Found at CE:{} in line {}'.format(id, line)

#------------------Основные Функции------------------
def read_map(map_name):
    'Десериализует карту map_name и возвращает ее структуру'
    targetFile = path.join(VHgamePath, map_name)   
    f = open(targetFile, 'rb')
    signature = f.read(11)
    Map = mtypes.MStruct(f, mtypes.MapMap[1])
    return Map


def read_db():
    '''Десериализует базу данных и возвращает ее структуру, предварительно
    сохранив ее под именем misc.DB(для дальнейшего использования функциями
    get_*_Name'''
    targetFile = path.join(VHgamePath, DBfileName)   
    f = open(targetFile, 'rb')    
    signature = f.read(12)
    misc.DB = mtypes.MStruct(f, mtypes.MapDB[1])
    return misc.DB    

if __name__ == '__main__':
    DB = read_db()
    Map = read_map(u'Map0545.lmu')
    
    #mtypes.MEventCommands.print_handlers_dict()
    print 'Page: ' + repr(Map.Events[3].Pages[1].EventCommands)


    #find_commands_DB(DB, command.ShowPicture, _picturepath = u'1-a-00bote')
        


