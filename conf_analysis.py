# -*- coding: utf-8 -*-  
from collections import Counter
import tools
import csv
import re
import matplotlib
from wordcloud import WordCloud
from django.db import models
from tkinter import messagebox,filedialog

def findrun(filename):
    if re.search(r'show run.txt',filename):
        return True
    elif re.search(r'show running-config.txt',filename):
        return True
    else:
        return False

r = tools.findallfilesbyCondition('log',findrun)

#Get text and join all from all configuration.
#t = list()
#wordtext = str()
#for p in r:
#    f = open(p,'r')
#    content = f.read()
#    f.close()
#    wordtext += content

def config_frequency(config_str):
    # Get the frequency of the words in all configuration
    t = config_str.split()
    t = Counter(t)
    t = Counter(t).most_common()
    with open('names.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(t)

    # Get the frequency of the lines in all configuration
    t = config_str.split('\n')
    t = Counter(t).most_common()
    with open('lines.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(t)

# Use wordcloud for all co有多nfigurations
#wc = WordCloud(
#    background_color='white',# 设置背景颜色
#    max_words=200, # 设置最大现实的字数
#    max_font_size=150,# 设置字体最大值
#    random_state=30,# 设置少种随机生成状态，即有多少种配色方案
#    width=800, 
#    height=600
#)
#wc.generate_from_text(wordtext)
#wc.to_file( "2.jpg")

t = list()
wordtext = str()

def add_device(device):
    return device

class Interface_Test():
    iName = ''
    iType = ''
    iIP = ''
    description = ''
    iVlan = ''
    iDevice = ''
    iUsed = ''
    def __init__(self):
        self.iName = ''
        self.iType = ''
        self.iIP = ''
        self.description = ''
        self.iVlan = ''
        self.iDevice = ''
        self.iUsed = ''

    def save(self):
        with open("interface.csv","a+") as csvfile: 
            f_csv = csv.writer(csvfile)
            f_csv.writerow((self.iDevice,self.iName,self.iVlan,self.iIP,self.description,self.iType))

CSV = 1
DB = 2
save_type = 1


def get_interface(file_list):
    for p in file_list:
        f = open(p,'r')
        lines  = f.readlines()
        f.close()
        hostname = ''
        interface = None
        for l in lines:
            if hostname == '':
                t = re.search('hostname (\S+)',l)
                if t:
                    hostname = add_device(t.groups()[0])

            t = re.search('^interface (\S+)',l)
            if t:
                if interface is not None:
                    interface.save()
                    interface = Interface_Test()
                else:
                    interface = Interface_Test()
                interface.iName = t.groups()[0]
                interface.iDevice = hostname

            if interface is not None:
                t = re.search('^\s+description (.*)\n',l)
                if t:
                    interface.description = t.groups()[0]
                
                t = re.search('ip address (\d+\.\d+\.\d+\.\d+)',l)
                if t:
                    interface.iIP = t.groups()[0]
                    interface.iType = 1
                
                t = re.search('switchport trunk allowed vlan (.*)',l)
                if t:
                    interface.iVlan = t.groups()[0]
                    interface.iType = 2

                t = re.search('switchport access vlan (\d+)',l)
                if t:
                    interface.iVlan = t.groups()[0]
                    interface.iType = 2

        if interface is not None:
            interface.save()


def get_interface_vlan(file_list):
    for p in file_list:
        f = open(p,'r')
        lines  = f.readlines()
        f.close()
        hostname = ''
        result = list()
        interface = list()
        for l in lines:
            t = re.search('^interface (\S+)',l)
            if t:
                result.append(interface)
                interface = list()
                interface.append(t.groups()[0])
            
            t = re.search('switchport trunk allowed vlan (\S+)',l)
            if t:
                interface.append(t.groups()[0])
            
            t = re.search('switchport access vlan (\d+)',l)
            if t:
                interface.append(t.groups()[0])
            
            t = re.search('channel-group (\d+) mode',l)
            if t:
                interface.append(t.groups()[0])
        
        return result


if __name__ == "__main__":
    #f = filedialog.askopenfile()
    #content = f.read()
    #f.close()
    #config_frequency(content)
    r = get_interface_vlan(('D:\\Python\\Tools\\B_HYA02_ZBA_AS02',))
    print(r)
    #with open("interface_vlan.csv","a+") as csvfile: 
    #    f_csv = csv.writer(csvfile)
    #    f_csv.writerows(r)
    