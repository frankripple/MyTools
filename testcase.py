# -*- coding: utf-8 -*-  
import tools
import re

current_path = 'log/'
#r = tools.findaddfilesbyname(current_path,r'show run.txt')

def findrun(filename):
    if re.search(r'show run.txt',filename):
        return True
    elif re.search(r'show running-config.txt',filename):
        return True
    else:
        return False

r = tools.findaddfilesbyCondition(current_path,findrun)
print(r)
print(len(r))

def findcommand(filename):
    f = open(filename,'r')
    content = f.read()
    f.close()
    if re.search('hostname ',content):
        return True
    else:
        return False

#r = tools.findaddfilesbyCondition(current_path,findcommand)
