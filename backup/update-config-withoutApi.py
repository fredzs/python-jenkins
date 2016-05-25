#!/usr/bin/env python
#-*- encoding:UTF-8 -*-

import urllib
import urllib2
import os
import ast
import time
import re
import xml.dom.minidom
from xml.etree.ElementTree import ElementTree,Element
from jenkinsapi.jenkins import Jenkins

def read_xml(in_path):
  '''读取并解析xml文件
    in_path: xml路径
    return: ElementTree'''
  tree = ElementTree()
  tree.parse(in_path)
  return tree

def write_xml(tree, out_path):
  '''将xml文件写出
    tree: xml树
    out_path: 写出路径'''
  tree.write(out_path, encoding="utf-8",xml_declaration=True)

def find_nodes(tree, path):
  '''查找某个路径匹配的所有节点
    tree: xml树
    path: 节点路径'''
  return tree.findall(path)

def change_node_text(nodelist, text, is_add=False, is_delete=False):
  '''改变/增加/删除一个节点的文本
    nodelist:节点列表
    text : 更新后的文本'''
  for node in nodelist:
    if is_add:
      node.text += text
    elif is_delete:
      node.text = ""
    else:
      node.text = text

def editConfigFile():   
  #1. 读取xml文件
  tree = read_xml("./config-old.xml")
      
  #2. 修改节点文本
    #定位节点
  text_nodes = find_nodes(tree, "publishers/org.korosoft.jenkins.plugin.rtp.RichTextPublisher/stableText")
  change_node_text(text_nodes, javaScript)
  
  #3. 输出到结果文件
  write_xml(tree, "./config.xml")
    
f = open('./script.js','r')
javaScript = f.read()

url ='http://172.16.100.150:8085/api/python?pretty=true&tree=jobs[name[*],url[*]]'
data =  ast.literal_eval(urllib2.urlopen(url).read())
jobList =  data.values()[0]

tempUrl = "http://172.16.100.150:8085/job/bjmcManagerFE_beta/"
homedir = os.getcwd()

# for l in jobList:
#     jobUrl = l.values()[0]
#     jobName = l.values()[1]
#     
#     # 通过调用Jenkins的RESTful API，获取每一个job的配置文件config.xml，并保存在本地;
#     configUrl = jobUrl + "config.xml";
#     print "downloading " + configUrl;
#     req = urllib2.Request(configUrl)
#     # "emhhbmdzaGVuZzoxMjM0NQ=="这个值是Jenkins账号与密码组成的字符串经过Base64加密后的值，原值为"zhangsheng:12345"
#     req.add_header("Authorization","Basic emhhbmdzaGVuZzoxMjM0NQ==")
#     req.add_header("user_agent","Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)")
#     response = urllib2.urlopen(req)
#     data = response.read()
#     filePath = homedir + '\\configFiles\\'  + jobName
#     #os.mkdir(filePath)
#     #with open(filePath + "\\config.xml.old", "wb+") as code:
#        # code.write(data)

# 利用ElementTree，读取本地的config.xml，修改其中的字段，并保存；
# editConfigFile()
    
# 通过调用Jenkins的RESTful API，将修改后的config.xml，上传至Jenkins对应的jobs中并覆盖原文件；
# def uploadConfigFile():
#     # req = urllib2.Request(tempUrl + "config.xml")
#     boundary = '----------%s' % hex(int(time.time() * 1000))
#     data = []
#     data.append('--%s' % boundary)
#         
#     fr=open("config-1.xml",'rb')
#     data.append('Content-Disposition: form-data; name="%s"; filename="config.xml"' % 'profile')
#     data.append('Content-Type: %s\r\n' % 'text/xml')
#     data.append(fr.read())
#     fr.close()
#     data.append('--%s--\r\n' % boundary)
#     http_url=tempUrl + "config.xml"
#     http_body='\r\n'.join(data)
#     print http_body
#     try:
#         #buld http request
#         req=urllib2.Request(http_url, data=http_body)
#         #header
#         req.add_header("Authorization","Basic emhhbmdzaGVuZzoxMjM0NQ==")
#         req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
#         req.add_header('User-Agent','Mozilla/5.0')
#         #post data to server
#         resp = urllib2.urlopen(req, timeout=5)
#         
#         #get response
#         qrcont=resp.read()
#         print qrcont
#     except Exception,e:
#         print e
# 
# uploadConfigFile();
jenkinsSource = 'http://172.16.100.150:8085/'
server = Jenkins(jenkinsSource, username = 'zhangsheng', password = '12345')
myJob=server.get_job("bjmcManagerFE_beta")
keys = server.keys();
# print keys
#print server['bjmcManagerFE_beta']
myConfig=myJob.get_config()
# print myConfig
new = myConfig.replace('<string>clean</string>', '<string>string bean</string>')
f = open('config-old.xml','r')
cc = f.read()

nnn = re.sub(r"<stableText>.*</stableText>","<stableText>ggg</stableText>",cc)

# with open("config-new.xml", "wb+") as code:
#          code.write(nnn)
myJob.update_config(nnn)


