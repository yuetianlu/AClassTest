#coding=utf-8
import re
import sys
import os
import subprocess
from git import Repo

#脚本环境：
#brew install pyenv
#pyenv init  （需要按提示修改相应文件）
#pyenv install 3.7.0
#pyenv shell 3.7.0
#pip install GitPython
#将该脚本放置工程spec同级目录
#python podPackage.py 

#pod私有库打版本脚本v2 - 配合.gitlab-ci.yml自动打包脚本
#主要流程：
# 1、固定文件名字
# 2、版本号自动+1，修改spec文件
# 3、信息无误后，提交spec文件，打tag，并执行pod spec push 命令上传spec文件

currentDir = os.getcwd()    #当前路径
repo = Repo(currentDir)     #GitPython 操作git相关

privateRepoURL = 'https://github.com/yuetianlu/MySpec.git'   #私有库url
oldVersion = ''    #选择的spec的version
tagPrefix = ''  #选择的spec的tag前缀
newVersion = '' #输入输入的新version

#获取信息
def getSpecInfo():
    return {'oldVersion':oldVersion,
    'newVersion':newVersion,
    'tagPrefix':tagPrefix}

#读取spec文件
def readpodspec (specName):
    # 读取podspec文件，用于获取当前的tag前缀，version等信息
    f = open(specName)
    content = f.read()
    f.close

    newContent = content.replace(' ', '')  #去除空格
    getInfo(newContent)
     
#得到spec中的version，tagPrefix
def getInfo(content):
    #获取spec中的版本和tag前缀
    global oldVersion 
    global tagPrefix
    oldVersion = re.findall(r's.version=(.*?)\n', content, re.S)[0]
    oldVersion = oldVersion.replace('"','').replace("'","")
    tagPrefix = re.findall(r':tag=>"(.*?)#{s.version}"', content, re.S)[0]

#获取新version版本
def getTagVersion():
    global newVersion 
    oldVersionNumberList = oldVersion.split('.')
    lastNumber = oldVersionNumberList[len(oldVersionNumberList)-1]
    newLastNumber = int(lastNumber) +1
    oldVersionNumberList[len(oldVersionNumberList)-1] = str(newLastNumber)

    for number in oldVersionNumberList:
        newVersion = newVersion+'.'+ number
        pass
    newVersion = newVersion.strip('.')

def gitTagCommand(tagPrefix,newTagVersion):
    print('push tag')
    newTag = tagPrefix+newTagVersion
    #这里先判断是否有该tag，有的话返回
    repo.create_tag(newTag)
    origin = repo.remotes.origin
    origin.push(newTag)
    print('done')

def getRepoInfo():
    repoList = subprocess.getoutput('pod repo')
    newRepoList = repoList.replace(' ', '')  #去除空格
    repoNames = re.findall(r'\n\n(.*?)\n-Type:', newRepoList, re.S)   #缺少第一个master
    repoUrls = re.findall(r'-URL:(.*?)\n-Path:', newRepoList, re.S)   #含有master的url
    repoUrls.remove('https://github.com/CocoaPods/Specs.git')  #移除master的url

    repoName = ''
    for repoUrl in repoUrls:
        if(repoUrl == privateRepoURL):
            index = repoUrls.index(privateRepoURL)
            repoName = repoNames[index]
    if(repoName == ''):
        #当前环境没有specLibrary，直接添加
        repoName = 'yrd_common_util_spec'
        subprocess.getoutput('pod repo add %s %s' %(repoName,privateRepoURL))
    print('repo name : %s' %(repoName))
    return repoName

def runPodPushCommand(podName,specName):
    print('run pod push command')
    podCommand = "pod repo push %s %s --allow-warnings --use-libraries --sources='https://github.com/CocoaPods/Specs.git,https://github.com/yuetianlu/MySpec.git' " % (podName, specName)
    output = subprocess.getoutput(podCommand)
    print(output)

def writeNewVersionToSpec(specName,oldVersion,newVersion):
    print('write to spec')
    f = open(specName,'r')
    content = f.read()
    content = content.replace('%s' %(oldVersion),'%s' %(newVersion))
    f2 = open(specName,'w')
    f2.write(content)
    f.close()
    f2.close()
    print('done')

def pushSpec(specName):
    print('push spec')
    origin = repo.remotes.origin
    index = repo.index
    index.add([specName])
    index.commit('[ci skip]PYTHON: pod package upgrade podspec')
    origin.push()
    print('done')
