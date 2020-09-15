'''
lanhuage: python
Descripttion: 
version: beta
Author: xiaoshuyui
Date: 2020-09-15 14:09:29
LastEditors: xiaoshuyui
LastEditTime: 2020-09-15 17:24:40


show

Usage:
    action.py   params  [-f,-s]

Options:
    -h  --help  show help.   :)
    -v  --version  show current version.
'''

import importlib
from ShowAndSearch.utils.logger import logger
from ShowAndSearch.utils.parser import BaseParser

def script():
    argList = [
        ('-f','--force','force to show message even do not contain the module'),
        ('-s','--simple','show simple message')
    ]

    p = BaseParser(argList,'show')
    parser = p.get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        from ShowAndSearch import __version__
        print(__version__)
        del __version__
        return
    
    if not args['question']:
        parser.print_help()
        return
    else:
        question = args['question'][0]
        if not args['force']:
            tmp = question.split('.')
            moduleName = tmp[0]
            try:
                module = importlib.__import__(moduleName)
            except:
                logger.error('module not found \n try search {}'.format(moduleName))
                return

            # try:
            tmp.remove(tmp[0])
            methodList = dir(module) 
            if len(tmp)>0:
                methodName = '.'.join(tmp)
                if methodName in methodList:
                    help(moduleName+'.'+methodName)
                else:
                    logger.error('module {} not contain {}'.format(moduleName,methodName))
                    return
            else:
                return

        







