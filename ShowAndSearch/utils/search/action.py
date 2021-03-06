'''
lanhuage: python
Descripttion: 
version: beta
Author: xiaoshuyui
Date: 2020-09-16 16:22:55
LastEditors: xiaoshuyui
LastEditTime: 2020-09-18 09:27:10
'''
import importlib
from ShowAndSearch.utils.logger import logger
from ShowAndSearch.utils.parser import BaseParser
import os
import asyncio
# from ruia import Request
from pyquery import PyQuery
import re

reg = "\d+\.\d+(\.\d+)*"

python_module_url = {
    'pypi': 'https://pypi.org/simple/',
    'tshua': 'https://pypi.tuna.tsinghua.edu.cn/simple/',
    'ali': "http://mirrors.aliyun.com/pypi/simple/"
}


def search_module_isExist(moduleName: str, searchEngine: str = 'pypi') -> list:
    global python_module_url
    try:
        s = PyQuery(python_module_url.get(
            searchEngine, python_module_url['pypi'])+'{}/'.format(moduleName))
        # print(s)
        validVersion = s.find('body').find('a')
        # print(type(validVersion))
        if validVersion is not None:
            # print(x)
            return [i.text() for i in validVersion.items('a')]
        else:
            return None
    except:
        return None
    # response = asyncio.get_event_loop().run_until_complete(request.fetch())


def script():
    argList = [
        ('-f', '--force', 'force to show message even do not find the module'),
        ('-s', '--simple', 'show simple message'),
        ('-i', '--install', 'auto install the module'),
        # ('-w','--web','search from web'),  # code copied from howdoi
    ]

    p = BaseParser(argList, 'search')
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

    if args['question'] and not args['install']:
        # print('test')
        moduleList = args['question']
        existList = []
        if not args['simple']:
            for tmp in moduleList:
                s = search_module_isExist(tmp)
                if s is not None:
                    existList.extend(s)
                else:
                    logger.warning('module {} is not found'.format(tmp))

            if len(existList) > 0:
                logger.info('found: \n {}'.format(' \n'.join(existList)))
            else:
                logger.info('found: \n nothing :)')
        else:
            global reg
            for tmp in moduleList:
                vs = search_module_isExist(tmp)
                if vs is not None:
                    v = re.search(reg, vs[-1]).group()
                    logger.info(
                        'module {} lastest version is {}'.format(tmp, v))
                else:
                    logger.warning('module {} is not found'.format(tmp))

    if args['install'] and args['force']:
        try:
            os.system(
                "pip install {} -i https://pypi.tuna.tsinghua.edu.cn/simple/".format(' '.join(args['question'])))
        except Exception as e:
            logger.error(e)

    if args['install'] and not args['force']:
        moduleList = args['question']
        existList = []
        for tmp in moduleList:
            if search_module_isExist(tmp):
                existList.append(tmp)
            else:
                logger.warning('module {} not found'.format(tmp))
        # print(existList)
        if len(existList) > 0:
            try:
                os.system(
                    "pip install {} -i https://pypi.tuna.tsinghua.edu.cn/simple/".format(' '.join(existList)))
            except Exception as e:
                logger.error(e)
