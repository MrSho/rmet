# coding: UTF-8
'''
Created on 24.11.2012

@author: Sho
'''

#Command Handlers
class Unknown(object):
    
    def __init__(self, fileObj, Map): pass
    
    def read(self, fileObj, Map): pass
    
    def __repr__(self, depth = 0): pass 
    

class Empty(object):
    
    def __init__(self, fileObj, Map): pass
    
    def read(self, fileObj, Map): pass
    
    def __repr__(self, depth = 0): pass  

    
class ShowMessage(object):
    
    def __init__(self, fileObj, Map): pass
    
    def read(self, fileObj, Map): pass
    
    def __repr__(self, depth = 0): pass 