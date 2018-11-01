# -*- coding: utf-8 -*-  
import os
import re


def findaddfilesbyCondition(rootdir,Condition):
    '''
    rootdir is the root path for the file search.
    Condition is a function for match the file. And Condtion must accept a parameter file_path and return True or False
    return value is the list of all the fullname of files.
    '''
    result = list()
    for parent, dirnames, filenames in os.walk(rootdir,followlinks=True):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            if Condition(file_path):
                result.append(file_path)
    return result

def findaddfilesbyname(rootdir,pfilename=''):
    '''
    rootdir is the root path for the file search.
    pfilename is the parttern for match the filename
    return value is the list of all the fullname of files.
    '''
    result = list()
    for parent, dirnames, filenames in os.walk(rootdir,followlinks=True):
        for filename in filenames:
            if pfilename == '' or re.search(pfilename,filename):
                file_path = os.path.join(parent, filename)
                result.append(file_path)
    return result
