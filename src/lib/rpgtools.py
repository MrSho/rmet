# coding: UTF-8
'''
Created on 20.11.2012

@author: Sho
'''
import cProfile

import os.path as path
import glob
import cmd

import misc
import command
import mtypes


#------------------Глобальные Константы------------------
VHgamePath = u'D:/аниме/хентай/bestiality^monster^tentacles/!VH/VHゲーム０１_121212_translated/\
VHゲーム０１_121212_translated'
#VHgamePath = u'D:/аниме/хентай/bestiality^monster^tentacles/!VH/my try/\
#VHゲーム０１_121005_translated'
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

def find_commands_Maps(command_class, **attr):
    for m in get_maps_list():
        print 'Searching: Map name: {}'.format(m)
        find_commands_Map(read_map(m), command_class, **attr)


def find_commands_Map(Map, command_class, **attr):
    '''Ищет в структуре карты Map команды command_class с атрибутами
    attr и печатает их в stdout. command_class и атрибуты смотреть в
    command.py'''
    for Event_id, Event in Map.Events.get_elist():
        for Page_id, Page in Event.Pages.get_elist():
            CL = Page.EventCommands.find_all_commands(command_class)
            for line, command in CL:
                for key, value in attr.items():
                    try:
                        if not getattr(command, key) == value:
                            break
                    except AttributeError:
                        break
                else:
                    print 'Found at E:{} P:{} in line {}'.format(Event_id,
                                                                 Page_id,
                                                                 line)
                    found = True
                

    
def find_commands_DB(DB, command_class, **attr):
    '''Ищет в структуре базы данных DB команды command_class с атрибутами
    attr и печатает их в stdout. command_class и атрибуты смотреть в
    command.py'''
    found = False
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
                found = True
    if not found: print 'DB: Nothing found'


def check_rpgmaker_limits(DB):
    'Выводит отношение между используемыми ресурсами рпг макера к его лимитам'
    def nonzero_size(elist):
        c = 0
        for i, e in elist:
            try:
                if e.Name != '': c += 1
            except AttributeError: pass
        return c
    
    print       'RecName    Used       Alloc      Limit   (Used/Limit)%'
    print       '------------------------------------------------------'
    formatstr = '{name:<10} {used:<10} {alloc:<10} 5000     {percent:>5}%'
    switch_elist = DB.Switch.get_elist()
    switch_used  = nonzero_size(switch_elist)
    print formatstr.format(name    = 'Switch', 
                           used    = switch_used,
                           alloc   = len(switch_elist),
                           percent = switch_used / 50)
    var_elist = DB.Vars.get_elist()
    var_used  = nonzero_size(var_elist)
    print formatstr.format(name    = 'Var', used=var_used,
                           alloc   = len(var_elist),
                           percent = var_used / 50)
    cevent_elist = DB.CEvents.get_elist()
    cevent_used  = nonzero_size(cevent_elist)
    print formatstr.format(name    = 'CEvent', 
                           used    = cevent_used, 
                           alloc   = len(cevent_elist),
                           percent = cevent_used / 50)
    
    
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

#------------------Коммандный интерпритатор------------------
#!Warning: Оболочка должна работать в кодировке shift_jis
class CommandInter(cmd.Cmd):
    
    def __init__(self, Intro=None):
        cmd.Cmd.__init__(self, Intro)
        self.prompt = '@>'
    
    def do_foo(self, args):
        print 'foo'
        
    def do_checklimits(self, args):
        check_rpgmaker_limits(misc.DB)
        
    def do_findindb(self, args):
        arga = args.split(' ')
        if len(arga) < 2:
            print 'error: not enough arguments'
            return
        if arga[0] == 'picture':
            if len(arga) != 2:
                print 'error: too many/not enough arguments'
                return
            kwarg = {'_picturepath': arga[1].decode('shift_jis_2004')}
            find_commands_DB(misc.DB, command.ShowPicture, **kwarg)
        else:
            print 'unknown command: ' + arga[0]
    
    def do_findinmaps(self, args):
        arga = args.split(' ')
        if len(arga) < 2:
            print 'error: not enough arguments'
            return
        if arga[0] == 'picture':
            if len(arga) != 2:
                print 'error: too many/not enough arguments'
                return
            kwarg = {'_picturepath': arga[1].decode('shift_jis_2004')}
            find_commands_Maps(command.ShowPicture, **kwarg)
        else:
            print 'unknown command: ' + arga[0]
    
    def do_exit(self, args):
        quit()

        
def inter_mode():
    CI = CommandInter()
    CI.cmdloop()    
        

def main():
    print 'Loading DB....',
    DB = read_db()
    print 'Done!'
    inter_mode()    

        
if __name__ == '__main__':
    #cProfile.run('read_db()')
    main()
    #Map = read_map(u'Map0545.lmu')
    

    #mtypes.MEventCommands.print_handlers_dict()
    #print 'Page: ' + repr(Map.Events[3].Pages[1].EventCommands)

    #find_commands_Maps(command.ShowPicture, _picturepath = u'00-出産-素体　触手05')
    #find_commands_DB(DB, command.ShowPicture, _picturepath = u'00-出産-素体　触手05')
        


