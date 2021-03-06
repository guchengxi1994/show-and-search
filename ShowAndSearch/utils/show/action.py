'''
lanhuage: python
Descripttion: 
version: beta
Author: xiaoshuyui
Date: 2020-09-15 14:09:29
LastEditors: xiaoshuyui
LastEditTime: 2020-09-22 13:12:13


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
import difflib
import smoothnlp


def script():
    argList = [
        ('-f', '--force', 'force to show message even do not contain the module'),
        ('-s', '--simple', 'show simple message')
    ]

    p = BaseParser(argList, 'show')
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
                logger.error(
                    'module not found \n try search {}'.format(moduleName))
                return

            # try:
            tmp.remove(tmp[0])
            methodList = dir(module)
            if len(tmp) > 0:
                methodName = '.'.join(tmp)
                if methodName in methodList:
                    if not args['simple']:
                        logger.info('press "q" to quit!')
                        help(moduleName+'.'+methodName)
                        return
                    else:
                        impo = getattr(module,methodName)
                        words = impo.__doc__
                        # print(words)
                        tmp = smoothnlp.split2sentences(str(words))
                        print(tmp[0])
                        return
                else:
                    logger.error('module {} not contain {}'.format(
                        moduleName, methodName))
                    lis = difflib.get_close_matches(methodName, methodList)
                    if len(lis) > 0:
                        logger.info(
                            'do you mean: {} ?'.format(' OR '.join(lis)))
                    del lis
                    return
            else:
                if not args['simple']:
                    logger.info('press "q" to quit!')
                    help(moduleName)
                else:
                    words = module.__doc__
                    tmp = smoothnlp.split2sentences(str(words))
                    print(tmp[0])

                    del words, tmp
                    return
