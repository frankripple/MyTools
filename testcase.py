# -*- coding: utf-8 -*-  
import tools
import re
import shutil
import os
import csv


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


def copy_configuration(path):
    r = tools.findaddfilesbyCondition(path,findrun)
    for p in r:
        f = open(p,'r')
        content = f.read()
        f.close()
        t = re.search('hostname (\S+)',content)
        if t:
            shutil.copyfile(p,'Running-configuration\\%s.txt'%t.groups()[0])

current_path = 'log/'

higher_version = ('12.2','15.0','15.2')
lower_version = ('6.2(20)','5.2(1)N1(8)','7.0(3)I6(1)','7.0(8)N1(1)')
firewall_version = ('9.6(4)')
if __name__ == "__main__":
    #copy_configuration(current_path)
    r = tools.findaddfilesbyname('Running-configuration\\')
    versions = list()
    ACLs = list()
    ACLs.append(('Device',"IP"))
    for p in r:
        hostname = os.path.basename(p).split('.')[0]
        f = open(p,'r')
        content = f.readlines()
        f.close()
        device_type = ''
        ACLs.append((hostname,""))
        count = 0
        start = 0
        for l in content:
            if device_type == '':
                t = re.search('ersion (.*?)\n',l)
                if t:
                    device_type = t.groups()[0].strip()
                    if (device_type in higher_version) or (device_type in lower_version) or (device_type in firewall_version):
                        #print('%s version is matched. Version is %s' %(hostname,device_type) )
                        versions.append((hostname,device_type))
                    else:
                        pass
                        #print('%s version is not matched. Version is %s' %(hostname,device_type) )
            
            if device_type in higher_version:
                t = re.search('access-list 89 permit (.*?)\n',l)
                if t:
                    ACLs.append((hostname,t.groups()[0]))
                    count +=1

            if device_type in lower_version:
                if start == 0:
                    t = re.search('ip access-list (\d+)',l)
                    if t and t.groups()[0].strip() == '89':
                        start = 1
                else:
                    t = re.search('permit \S+ (.*?) any',l)
                    if t:
                        ACLs.append((hostname,t.groups()[0]))
                        count +=1

            if device_type in firewall_version:
                t = re.search('ssh ([0-9.]+ [0-9.]+)',l)
                if t:
                    ACLs.append((hostname,t.groups()[0]))
                    count +=1
        if count == 0:
            print(hostname)

    with open('ACLs.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(ACLs)

    with open('version.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(versions)
