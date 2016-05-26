#!/usr/bin/env python
#-*- encoding:UTF-8 -*-

import os
import re
import sys
from jenkinsapi.jenkins import Jenkins
    
reload(sys)
sys.setdefaultencoding('utf-8')
f1 = open('./default-script','r')
f2 = open('./add-script','r')
editScript = f1.read()
addScript = f2.read()

baseUrl ='http://172.16.100.150:8085/'
homedir = os.getcwd()
server = Jenkins(baseUrl, username = 'zhangsheng', password = '12345')
jobKeys = server.keys();

def download(key, config):
  filePath = homedir + '\\configFiles\\'  + key
  if not os.path.isdir(filePath):
  #   print(filePath + u'路径已存在')
  # else:
    print(filePath + u'路径不存在，自动新建。')
    os.makedirs(filePath)
  output = open(filePath + "\\oldConfig.xml", "wb+")
  output.write(config)

def saveNewConfigFile(key, newConfig):
  filePath = homedir + '\\configFiles\\'  + key
  output = open(filePath + "\\newConfig.xml", "wb+")
  output.write(newConfig)
  
def test():
  key = 'benmu-test'
  #j = server.get_job('bjmcManagerFE_beta，benmu-health-img-maven')
  j = server.get_job(key)
  c = j.get_config()
  newC = re.search(r"<stableText>.*</stableText>", c, flags=re.DOTALL)
  if newC == None:
    print('job: ' + key + u' 的config.xml中没有设置\"构建后执行的HTML\"，将自动追加！')
    newC = re.sub(r"<publishers>",addScript, c)
  else:
    newC = re.sub(r"<stableText>.*</stableText>","<stableText>" + editScript + "</stableText>", c,0,flags=re.DOTALL)
  print(u'--更新  \"http://172.16.100.150:8085/job/' + key + '/config.xml\" 成功!')
  #print(newC)
  j.update_config(newC)
  

def main():
  total = 0
  count = 0
  todo = []
  for key in jobKeys:
    jobUrl = baseUrl + key
    job = server.get_job(key)
    config = job.get_config()
    print('---------------------------------------------------------------------');
    # 下载并保存旧的config.xml文件
    download(key, config);
    
    search = re.search(r"<stableText>.*</stableText>", config, flags=re.DOTALL)
    total = total + 1
    if search == None:
      print(str(total) + ' job: ' + key + u' 的config.xml中没有设置\"构建后执行的HTML\"。')
      todo.append(key)
      #newConfig = re.sub(r"<publishers>",addScript, c)
    else:
      newConfig = re.sub(r"<stableText>.*</stableText>","<stableText>" + editScript + "</stableText>", config, 0, flags=re.DOTALL)
      count = count + 1
      
      # 下面这句是向jenkins刷新config文件，不可撤销，谨慎操作！
      job.update_config(newConfig)
      
      # 保存修改后的config.xml文件，便于对比修改是否正确
      saveNewConfigFile(key, newConfig)
      
      print(str(total) + u' : 更新 ' + jobUrl + u'/config.xml 成功!')
  print('---------------------------------------------------------------------');
  print(u'共有' + str(count) + u'个job更新了配置。')
  print(u'以下' + str(total - count) + u'个job需要手动修改配置：')
  for key in todo:
    print(key + ' : ' + baseUrl + key)
  
#test();
main();

