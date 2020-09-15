'''
lanhuage: python
Descripttion: 
version: beta
Author: xiaoshuyui
Date: 2020-09-15 14:10:02
LastEditors: xiaoshuyui
LastEditTime: 2020-09-15 14:59:36
'''
import os
import subprocess
import importlib


def cmd(command):
    subp = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8")
    subp.wait(2)
    if subp.poll() == 0:
        print(subp.communicate()[1])
    else:
        print("失败")

if __name__ == "__main__":
    # cmd("java -version")
    # cmd("exit 1")
    # cmd("python")
    tmp = 'cv2'.split('.')
    # module = importlib.__import__(tmp[0])
    # methodList = dir(module)

    x = 'cv2.imshow'

    x = 'cv2'

    # if 'imshow' in methodList:
    #     print(True)
    
    help(x)

    # help(module.imshow)

