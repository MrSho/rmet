# coding: UTF-8
'''
Created on 24.11.2012

@author: Sho
'''
from misc import getFNum, getFNumStr, strInHex, tabToken

class CommandHandler(object):
    CCode = None
    
    def __init__(self, Dlvl): pass
    
    def read(self, fileObj): pass
    
    def __repr__(self, depth = 0): pass     
   
    
class ShowMessage(CommandHandler):
    CCode = getFNumStr('\xce\x7e')
    
    def __init__(self, Dlvl = 0): 
        self.Dlvl = Dlvl
        self.Message = ''
    
    def read(self, fileObj): 
        self.Dlvl = getFNum(fileObj)
        Messagelen = getFNum(fileObj)
        MessageBytes = fileObj.read(Messagelen)
        self.Message = MessageBytes.decode(encoding='shift_jis_2004')
        fileObj.read(1)        
    
    def __repr__(self, depth = 0):
        FString = '{}<>Messg:{}\n'
        return FString.format(tabToken(depth + self.Dlvl), self.Message)
    
class ShowMessageContinue(ShowMessage):
    CCode = getFNumStr('\x81\x9d\x0e')       
    
    def __repr__(self, depth = 0):
        FString = '{}:      :{}\n'
        return FString.format(tabToken(depth + self.Dlvl), self.Message)  
    
class ShowChoise(CommandHandler):
    CCode = getFNumStr('\xcf\x1c')
    
    def __init__(self, Dlvl = 0):
        self.Dlvl = Dlvl
        self.CaseMessage = ''
        self.Unk1 = 0
        self.CancelCase  = 0
    
    def read(self, fileObj):
        self.Dlvl = getFNum(fileObj)
        Messagelen = getFNum(fileObj)
        MessageBytes = fileObj.read(Messagelen)
        self.CaseMessage = MessageBytes.decode(encoding='shift_jis_2004')
        self.Unk1 = fileObj.read(1)
        self.CancelCase = fileObj.read(1)
    
    def __repr__(self, depth = 0):
        FString = '{}<>Show Choise: {} C:{}\n' 
        return FString.format(tabToken(depth + self.Dlvl), self.CaseMessage, strInHex(self.CancelCase))

class Case(CommandHandler):
    CCode = getFNumStr('\x81\x9d\x2c')
    
    def __init__(self, Dlvl = 0):
        self.Dlvl = Dlvl
        self.CaseMessage = ''
        self.Unk1 = 0
        self.CaseNum = 0       
    
    def read(self, fileObj):
        self.Dlvl = getFNum(fileObj)
        Messagelen = getFNum(fileObj)
        MessageBytes = fileObj.read(Messagelen)
        self.CaseMessage = MessageBytes.decode(encoding='shift_jis_2004')
        self.Unk1 = fileObj.read(1)
        self.CaseNum = getFNum(fileObj)                       
    
    def __repr__(self, depth = 0): 
        FString = '{}: [{}] Case\n'
        if self.CaseNum == 4:
            Message = 'CANCEL'
        else:
            Message = self.CaseMessage
        return FString.format(tabToken(depth + self.Dlvl), Message) 
    
class EndCase(CommandHandler):
    CCode = getFNumStr('\x81\x9d\x2d')
    
    def __init__(self, Dlvl = 0):
        self.Dlvl = Dlvl
    
    def read(self, fileObj):
        self.Dlvl = getFNum(fileObj)
        fileObj.read(2)
    
    def __repr__(self, depth = 0):
        return tabToken(depth + self.Dlvl) + ':END Case\n'

class CaseEmpty(CommandHandler):
    CCode = getFNumStr('\x0a')
    
    def __init__(self, Dlvl = 0):
        self.Dlvl = Dlvl
    
    def read(self, fileObj):
        self.Dlvl = getFNum(fileObj)
        fileObj.read(2)
    
    def __repr__(self, depth = 0):
        return tabToken(depth + self.Dlvl) + '<>\n'     
    
class Empty(CommandHandler):
    CCode = getFNumStr('\x00')
    
    def __init__(self, Dlvl = 0):
        self.Dlvl = Dlvl
    
    def read(self, fileObj):
        self.Dlvl = getFNum(fileObj)
        fileObj.read(2)        
    
    def __repr__(self, depth = 0):
        return tabToken(depth + self.Dlvl) + '<>\n'