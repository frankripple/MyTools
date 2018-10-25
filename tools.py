# -*- coding: utf-8 -*-  
import os
import re
def findaddfiles(rootdir,pfilename):
    result = list()
    for parent, dirnames, filenames in os.walk(rootdir,followlinks=True):
        for filename in filenames:
            if re.search(pfilename,filename):
                file_path = os.path.join(parent, filename)
                result.append(file_path)
    return result