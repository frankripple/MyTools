# -*- coding: utf-8 -*-  
'''
    Some small function which can be used in project
'''
import os
import re
import datetime


def findallfilesbyCondition(rootdir,Condition):
    '''
    This function is used to find files which can match user-defined conditions
    Args:
        rootdir is the root path for the file search. Include subfolders
        Condition is a function for match the file. And Condtion must accept a parameter file_name and return True or False
    Returns:
        The list of all the fullname of files. If list is empty, it means the dir is empty
    Raises:
        Raise NotADirectoryError is the rootdir not exsit or is a dirname
    '''
    if not os.path.isdir(rootdir):
        raise NotADirectoryError
    result = list()
    for parent, dirnames, filenames in os.walk(rootdir,followlinks=True):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            if Condition(file_path):
                result.append(os.path.abspath(file_path))
    return result

def findallfilesbyname(rootdir,pfilename=''):
    '''
    This function is used to find files whose name can match pfilename

    Args:
        rootdir is the root path for the file search.
        [pfilename] is the parttern for match the filename. Include subfolders
    Returns:
        The list of all the full path of files which match the pfilename.
        If no pfilename or pfilename is '', it will return all files in this folder.
    Raises:
        Raise NotADirectoryError is the rootdir not exsit or is not a dirname
    '''
    result = list()
    if not os.path.isdir(rootdir):
        raise NotADirectoryError
    for parent, dirnames, filenames in os.walk(rootdir,followlinks=True):
        for filename in filenames:
            if pfilename == '' or re.search(pfilename,filename):
                file_path = os.path.join(parent, filename)
                result.append(os.path.abspath(file_path))
                
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
        return len(self.all_logs)
    
    @property
    def all_logs(self):
        return self.error_logs+self.info_logs
    
    @property
    def errors(self):
        return self.error_logs
    
    @property
    def infos(self):
        return self.info_logs
