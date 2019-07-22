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

#pod私有库打版本脚本
#主要流程：
# 1、查找当前路径所有spec，输入人选择上传的spec
# 2、根据输入新的版本号，修改spec文件
# 3、确认信息无误后，提交spec文件，打tag，并执行pod spec push 命令上传spec文件

currentDir = os.getcwd()   #当前路径
repo = Repo(currentDir)    #GitPython 操作git相关
privateRepoURL = 'https://github.com/yuetianlu/MySpec.git'   #私有库url
oldVersion = ''    #选择的spec的version
tagPrefix = ''  #选择的spec的tag前缀
newVersion = '' #输入输入的新version

#查找当前目录的所有spec，返回用户选择的specName
def searchspec():
    fileList = os.listdir(currentDir)   #当前目录所有文件
    number = 0        
    specList =[]    #当前目录spec列表
    #添加.podspec文件列表
    for fileName in fileList:
        if(fileName.endswith('.podspec')):
            specList.append(fileName)
            print('['+repr(number)+']'+fileName)
            number = number+1
    #判断list
    if(len(specList)<=0):
        print('该目录下没有任何spec文件')
        os._exit(0)
    else:
        return specList 
#获取选择的spec
def getInput(specList):
    specnNumber = int(input("input spec number(example: 1)?: "))
    if(0<=specnNumber<len(specList)):
        specName = specList[specnNumber]
        print('####################################################')
        print('selected spec is      : '+specName)
        return specName
    else:
        print('input error：invalid number')
        os._exit(0)

#读取spec文件
def readpodspec (specName):
    # 读取podspec文件，用于获取当前的tag前缀，version等信息
    f = open(specName)
    content = f.read()
    f.close

    newContent = content.replace(' ', '')  #去除空格
    getInfo(newContent)
    
    
#得到spec中的version，tagPrefix做展示
def getInfo(content):
    #获取spec中的版本和tag前缀
    global oldVersion 
    global tagPrefix
    
    oldVersion = re.findall(r's.version=(.*?)\n', content, re.S)[0]
    oldVersion = oldVersion.replace('"','').replace("'","")
    tagPrefix = re.findall(r':tag=>"(.*?)#{s.version}"', content, re.S)[0]

#获取输入的version版本
def getTagVersion():
    global newVersion 
    newVersion = input("input new version (example : 0.1.1): ")

def gitBranchInfo():
    print('current active branch : ')
    print(repo.active_branch)

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
    content = content.replace('"%s"' %(oldVersion),'"%s"' %(newVersion))
    f2 = open(specName,'w')
    f2.write(content)
    f.close()
    f2.close()
    print('done')

def showInfo():
    #打印相关信息
    print('\ncurrent version       : '+oldVersion)
    if(newVersion!=''):
        print('new version           : '+newVersion)
    print('tagPrefix             : '+tagPrefix)
    #git分支信息
    gitBranchInfo()
    print('\nplz check the information!')
    print('####################################################')

def pushSpec(specName):
    print('push spec')
    index = repo.index
    index.add([specName])
    index.commit('PYTHON: pod package upgrade podspec')
    origin = repo.remotes.origin
    origin.push()
    print('done')

def makeSure():
    print('we will edit podspec file and run git command')
    sure = input("make sure the information is correct(y/n)?: ")
    if(sure == 'y'):
        print('\n')
    elif(sure == 'n'):
        os._exit(0)
    else:
        print('only y and n can be recognized！')
        makeSure()

def main():
    specList = searchspec()  #获取当前目录下的spec文件列表
    specName = getInput(specList)   #用户选择的spec
    readpodspec(specName)   #得到用户选择的spec中的tag prefix

    showInfo()
    getTagVersion()         #获取用户输入的新版本号
    showInfo()
##################################################################################
    makeSure()  #确认信息正确，后面将对文件和git进行操作
    writeNewVersionToSpec(specName,oldVersion,newVersion) #修改spec文件的version为新版本
    pushSpec(specName) #提交spec文件
    gitTagCommand(tagPrefix,newVersion)      #提交新tag

    repoName = getRepoInfo()       #获取pod repo信息
    runPodPushCommand(repoName,specName)     #run push command

if __name__ == '__main__':
    main()
