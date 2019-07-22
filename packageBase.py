#coding=utf-8
import sys
sys.path.append('script/')
import podPackageHelper

def main():

    specName = sys.argv[1]
    podPackageHelper.readpodspec(specName)   #得到用户选择的spec中的tag prefix
    podPackageHelper.getTagVersion()         #获取用户输入的新版本号
    specInfo =  podPackageHelper.getSpecInfo()

    oldVersion = specInfo['oldVersion']
    newVersion = specInfo['newVersion']
    tagPrefix = specInfo['tagPrefix']
##################################################################################
    podPackageHelper.writeNewVersionToSpec(specName,oldVersion,newVersion) #修改spec文件的version为新版本
    podPackageHelper.pushSpec(specName) #提交spec文件
    podPackageHelper.gitTagCommand(tagPrefix,newVersion)      #提交新tag

    repoName = podPackageHelper.getRepoInfo()       #获取pod repo信息
    podPackageHelper.runPodPushCommand(repoName,specName)     #run push command

if __name__ == '__main__':
    main()