# -*- coding: utf-8 -*-  
import os
import re
import datetime


def findallfilesbyCondition(rootdir,Condition):
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

def findallfilesbyname(rootdir,pfilename=''):
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

def get_keywords(pattern_list,content):
    for p in pattern_list:
        t = re.search(p,content)
        if t:
            return t.groups()[0]
    return ''

def get_current_time(format="%Y-%m-%d %H:%M:%S"):
    try:
        return datetime.datetime.now().strftime(format)
    except:
        return "Error Time Format"

class log_tools():
    
    logs = list()
    error_logs = list()
    info_logs = list()
    def __init__(self):
        self.logs = []
    
    def add_error(self,detail):
        self.error_logs.append("%s Error: %s"%(get_current_time(),detail))
        return self.count

    def add_info(self,detail):
        self.info_logs.append("%s Info: %s"%(get_current_time(),detail))
        return self.count

    @property
    def count(self):
        return len(self.logs)
    
    @property
    def all_logs(self):
        return self.error_logs+self.info_logs
    
    @property
    def errors(self):
        return self.error_logs
    
    @property
    def infos(self):
        return self.info_logs
