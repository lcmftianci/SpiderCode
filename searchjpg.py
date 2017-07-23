#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import re
import urllib
import urllib2
import requests
import sys

print "Author:xll"
print "date:",time.strftime('%Y-%m-%d',time.localtime(time.time()))

#写此程序的宗旨是，先获取传入网页链接页面中的所有网页链接
#分析解析这些链接，再根据链接的特点生成新的下载链接， 在原先网址上加上/archive/master.zip就可以了
#下载压缩包

#1.首先获取网址
#设置编码
reload(sys)
sys.setdefaultencoding('utf-8')
circle = requests.get("https://user.qzone.qq.com/2497088246/infocenter")
#text与content.text中的数据有不同
content = circle.text
# #这里是正则的坑  括号的东西是分组的 外面没有括号之前 只会匹配到jpg和png不会匹配全部
#外面多一层括号才会匹配整个  但是特别的是 里面的括号也会匹配  所以
#真正findall的是整个list  list里面每个都是元组  元组里面有xxx.jpg和jpg

#匹配到之后获取开头末尾的位置
# finder = re.search(pattern, test)
# start = finder.start()
# end = finder.end()
# print test[start:end]
pattern = "(http:[^\s]*?(jpg|png|PNG|JPG))"#正则表达式
finder = re.findall(pattern, circle.text)
#匹配http获取文件名
truepis = ".*photo/p0.*"
#获取图片网址
picpattern = "http:[^\s]*/"
#匹配标题
titlepattern = '<p class="title" title=".*?"'
imgfinder = re.findall(titlepattern, circle.text)
imglen = 0

print "开始下载文件"
print "len(finder)", len(finder)
for n in xrange(0, len(finder)):
    print "下载"
    if re.match(truepis, finder[n][0]):
        print finder[n][0]

        # p0改为r0后变成了大图目录的地址，
        bigpicture = finder[n][0].replace('photo/p0', 'photo/r0')
        newimg = requests.get(bigpicture)

        # 替换掉无关的字符串
        temp = imgfinder[imglen].replace('<p class="title" title="', '')
        newfinder = re.search(picpattern, finder[n][0])

        # 截取title
        print "存储图片"
        temp = "G:/github/WebSpider_Python/img/" + temp[0:len(temp) - 1] + '.jpg'
        # 下载文件，超级简单 设定好目录  content的意义也在于这里
        with open(temp, 'wb') as newfile:
            newfile.write(newimg.content)

        imglen = imglen + 1

print "下载结束"

