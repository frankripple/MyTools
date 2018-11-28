# -*- coding: utf-8 -*-
'''    Some small function which can be used in project  '''
import os
import re
import csv
import datetime
from filecmp import dircmp


def findallfilesbycondition(rootdir, condition):
    '''
    This function is used to find files which can match user-defined conditions
    Args:
        rootdir:    The root path for the file search. Include subfolders
        Condition:  a function for match the file.
                    And Condtion must accept a parameter file_name and return True or False
    Returns:
        The list of all the fullname of files. If list is empty, it means the dir is empty
    Raises:
        Raise NotADirectoryError is the rootdir not exsit or is a dirname
    '''
    if not os.path.isdir(rootdir):
        raise NotADirectoryError
    result = list()
    for parent, _, filenames in os.walk(rootdir, followlinks=True):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            if condition(file_path):
                result.append(os.path.abspath(file_path))
    return result

def findallfilesbyname(rootdir, pfilename=''):
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
    for parent, _, filenames in os.walk(rootdir, followlinks=True):
        for filename in filenames:
            if pfilename == '' or re.search(pfilename, filename):
                file_path = os.path.join(parent, filename)
                result.append(os.path.abspath(file_path))
    return result

def get_keywords(pattern_list, content):
    '''
        Find matches in content according to the pattern in the pattern_list.
        Args:
            pattern_list:   A list of pattern string
            content:        The string which look up in
        Returns:
            The first match in the pattern_list
        Raise:
            re.error: if the pattern is not corret
    '''
    #TODO need to try to optimize the re search
    for _p in pattern_list:
        try:
            _t = re.search(_p, content)
        except re.error as _e:
            raise _e
        if _t:
            return _t.groups()[0]
    return None

def get_current_time(_format="%Y-%m-%d %H:%M:%S"):
    '''
        Get a current time string
        Args:
            A time format string which following 1999 version of the C standard
        Returns:
            The time string or 'Error Time Format'
    '''
    try:
        return datetime.datetime.now().strftime(_format)
    except ValueError as _e:
        LOGS.add_error(_e)
        return "Error Time Format"

class LogTools():
    '''
    Class is for log record and display

    Functions:
        Add_error: Add log with time and Error label
        Add_info : Add log with time and info label
    Attributes:
        count: Count of all logs
        errors: list of all error logs
        infos:  list of all Info logs
    '''
    error_logs = list()
    info_logs = list()
    def __init__(self):
        self.logs = []

    def add_error(self, detail):
        ''' Format an error string'''
        self.error_logs.append("%s Error: %s\n"%(get_current_time(), detail))
        return self.count

    def add_info(self, detail):
        ''' Format an log string'''
        self.info_logs.append("%s Info: %s\n"%(get_current_time(), detail))
        return self.count

    @property
    def count(self):
        ''' Return number of all logs. including errors and infomations'''
        return len(self.all_logs)

    @property
    def all_logs(self):
        ''' All logs including errors and infomation'''
        return self.error_logs+self.info_logs

    @property
    def errors(self):
        '''Error logs'''
        return self.error_logs

    @property
    def infos(self):
        '''Infomation logs'''
        return self.info_logs

LOGS = LogTools()

def list_write_to_csv(file_name, content, header=None):
    '''
        Output all content to a csv file. item of content can be list or dict
        if content is dict, header should by matched with keys of dict
        Args:
            file_name:
                Full name of the CSV file
            content:
                List which need to be written. item of content can be list or dict
            header:
                if there is header, add it.
        Returns:
        Raises:
            IOError: If can not open or write the file.
            KeyError: When content is not list
            PermissionError: When reopen the file
    '''
    with open(file_name, 'w', newline='') as csvfile:
        if content:
            if isinstance(content[0], (list, tuple)):
                writer = csv.writer(csvfile)
                if header:
                    writer.writerow(header)
                writer.writerows(content)
            elif isinstance(content[0], dict):
                if not header:
                    header = content[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=header)
                writer.writeheader()
                writer.writerows(content)



def _get_common_files(dcmp, common, left, right, _base_len=0):
    '''
        Loop function only for get common files
    '''
    if not _base_len:
        _base_len = len(dcmp.left) + 1
    cur_dir = dcmp.left[_base_len:]
    for name in dcmp.common_files:
        common.append(os.path.join(cur_dir, name))

    for name in dcmp.left_only:
        left.append(os.path.join(cur_dir, name))

    for name in dcmp.right_only:
        right.append(os.path.join(cur_dir, name))

    for sub_dcmp in dcmp.subdirs.values():
        _get_common_files(sub_dcmp, common, left, right, _base_len)

def get_common_files(left_dir, right_dir):
    '''
        Function to get common and diff files in dir. And it will search all sub dirs
        Args:
            left_dir, right_dir:
                Dirs which need to be compare
        returns:
            If dir is not correct, will return (None, None, None)
            common:
                result of all common file names
            left:
                result of all files and dirs which only in left dir
            right:
                result of all files and dirs which only in right dir
    '''
    dcmp = dircmp(left_dir, right_dir)
    common_file_list = list()
    left_only_list = list()
    right_only_list = list()

    try:
        _get_common_files(dcmp, common_file_list, left_only_list, right_only_list)
    except OSError as _e:
        return (None, None, None)

    return common_file_list, left_only_list, right_only_list

if __name__ == '__main__':
    pass
