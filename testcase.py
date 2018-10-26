# -*- coding: utf-8 -*-  
import tools
import re
import shutil

current_path = 'log/'
#r = tools.findaddfilesbyname(current_path,r'show run.txt')

def findrun(filename):
    if re.search(r'show run.txt',filename):
        return True
    elif re.search(r'show running-config.txt',filename):
        return True
    else:
        return False

def findcommand(filename):
    f = open(filename,'r')
    content = f.read()
    f.close()
    if re.search('hostname ',content):
        return True
    else:
        return False

r = tools.findaddfilesbyCondition(current_path,findrun)

for p in r:
    f = open(p,'r')
    content = f.read()
    f.close()
    t = re.search('hostname (\S+)',content)
    if t:
        shutil.copyfile(p,'Running-configuration\\%s.txt'%t.groups()[0])



#r = tools.findaddfilesbyCondition(current_path,findcommand)


