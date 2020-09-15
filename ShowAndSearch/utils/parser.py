'''
lanhuage: python
Descripttion: 
version: beta
Author: xiaoshuyui
Date: 2020-09-15 15:59:10
LastEditors: xiaoshuyui
LastEditTime: 2020-09-15 17:10:24
'''
import argparse
from ShowAndSearch.utils.logger import logger

class BaseParser(object):
    def __init__(self,args:list,method:str):
        """
        args type:list
        arg type:tuple
        arg example : ('-f','--force','force to show message even do not contain the module')
        """
        self.args = args
        self.method = method
        self.parser = argparse.ArgumentParser(description='{} method or module information'.format(self.method))
    
    def get_parser(self):
        
        self.parser.add_argument('question',metavar='QUESTION',type=str,nargs='*',help='the question to answer')
        self.parser.add_argument('-v','--version',help='show current version')
        if len(self.args)>0:
            # self.parser.add_argument('-f','--force',help='force to show message even do not contain the module')
            # self.parser.add_argument('-s','--simple',help='show simple message')
            for i in self.args:
                self.parser.add_argument(i[0],i[1],help=i[2],action='store_true')
        else:
            logger.warning('args list is null')
        
        return self.parser
    
    def add_parser(self,arg):
        if type(arg) is tuple and len(arg) == 3:
            self.parser.add_argument(arg[0],arg[1],help=arg[2],action='store_true')
        else:
            logger.error('input error')
        return self.parser
        