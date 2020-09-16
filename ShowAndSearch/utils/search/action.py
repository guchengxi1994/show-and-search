'''
lanhuage: python
Descripttion: 
version: beta
Author: xiaoshuyui
Date: 2020-09-16 16:22:55
LastEditors: xiaoshuyui
LastEditTime: 2020-09-16 17:07:06
'''
import importlib
from ShowAndSearch.utils.logger import logger
from ShowAndSearch.utils.parser import BaseParser
import os
import asyncio
from ruia import Request

python_module_url = {
    'pypi':'https://pypi.org/simple/',
    'tshua':'https://pypi.tuna.tsinghua.edu.cn/simple/',
    'ali':"http://mirrors.aliyun.com/pypi/simple/"
}

def search_module_isExist(moduleName:str,searchEngine:str='pypi')->bool:
    global python_module_url
    request = Request(python_module_url.get(searchEngine,python_module_url['pypi'])+'{}/'.format(moduleName))
    response = asyncio.get_event_loop().run_until_complete(request.fetch())

    return response.status == 200
    

def script():
    argList = [
        ('-f','--force','force to show message even do not find the module'),
        ('-s','--simple','show simple message'),
        ('-i','--install','auto install the module')
    ]

    p = BaseParser(argList,'search')
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

    if args['install'] and args['force']:
        try:
            os.system("pip install {} -i https://pypi.tuna.tsinghua.edu.cn/simple/".format(' '.join(args['question'])))
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
        if len(existList)>0:
            try:
                os.system("pip install {} -i https://pypi.tuna.tsinghua.edu.cn/simple/".format(' '.join(existList)))
            except Exception as e:
                logger.error(e)


        
        