# -*- coding: utf-8 -*-  
from collections import Counter
import tools
import csv
import re
import matplotlib
from wordcloud import WordCloud


def findrun(filename):
    if re.search(r'show run.txt',filename):
        return True
    elif re.search(r'show running-config.txt',filename):
        return True
    else:
        return False

r = tools.findaddfilesbyCondition('log',findrun)

t = list()
wordtext = str()
for p in r:
    f = open(p,'r')
    content = f.read()
    f.close()
    wordtext += content

#t = wordtext.split()
#t = Counter(t)
#with open('names.csv', 'w', newline='') as csvfile:
#    writer = csv.writer(csvfile)
#    writer.writerows(t.items())

#t = wordtext.split('\n')
#t = Counter(t)
#with open('lines.csv', 'w', newline='') as csvfile:
#    writer = csv.writer(csvfile)
 #   writer.writerows(t.items())


wc = WordCloud(
    background_color='white',# 设置背景颜色
    max_words=200, # 设置最大现实的字数
    max_font_size=150,# 设置字体最大值
    random_state=30,# 设置有多少种随机生成状态，即有多少种配色方案
    width=800, 
    height=600
)
wc.generate_from_text(wordtext)
wc.to_file( "2.jpg")

