# -*- coding: utf-8 -*-  
from collections import Counter
import tools
import csv
import re
import matplotlib
from wordcloud import WordCloud
from django.db import models

def findrun(filename):
    if re.search(r'show run.txt',filename):
        return True
    elif re.search(r'show running-config.txt',filename):
        return True
    else:
        return False

r = tools.findaddfilesbyCondition('log',findrun)

#Get text and join all from all configuration.
#t = list()
#wordtext = str()
#for p in r:
#    f = open(p,'r')
#    content = f.read()
#    f.close()
#    wordtext += content

# Get the frequency of the words in all configuration
#t = wordtext.split()
#t = Counter(t)
#with open('names.csv', 'w', newline='') as csvfile:
#    writer = csv.writer(csvfile)
#    writer.writerows(t.items())

# Get the frequency of the lines in all configuration
#t = wordtext.split('\n')
#t = Counter(t)
#with open('lines.csv', 'w', newline='') as csvfile:
#    writer = csv.writer(csvfile)
 #   writer.writerows(t.items())

# Use wordcloud for all configurations
#wc = WordCloud(
#    background_color='white',# 设置背景颜色
#    max_words=200, # 设置最大现实的字数
#    max_font_size=150,# 设置字体最大值
#    random_state=30,# 设置有多少种随机生成状态，即有多少种配色方案
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
save_type = DB

# Create your models here.
class Device(models.Model):
    hostname = models.CharField(max_length=64)
    Mgt_IP = models.GenericIPAddressField()
    description = models.CharField(max_length=200)

class Interface(models.Model):
    iName = models.CharField(max_length=64)
    iType = models.IntegerField()
    iIP = models.GenericIPAddressField()
    description = models.CharField(max_length=200)
    iVlan = models.CharField(max_length=64)
    iDevice = models.ForeignKey(Device,on_delete=models.CASCADE,default ='')
    iUsed = models.BooleanField()

for p in r:
    f = open(p,'r')
    lines  = f.readlines()
    f.close()
    hostname = ''
    interface = None
    for l in lines:
        if hostname == '':
            t = re.search('hostname (\S+)',l)
            if t:
                if save_type == CSV:
                    hostname = add_device(t.groups()[0])
                else:


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




if __name__ == "__main__":
    pass