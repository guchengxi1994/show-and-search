'''
lanhuage: python
Descripttion: 
version: beta
Author: xiaoshuyui
Date: 2020-09-15 16:39:03
LastEditors: xiaoshuyui
LastEditTime: 2020-09-15 16:54:19
'''
import sys
sys.path.append('..')

from ShowAndSearch.utils.parser import BaseParser

if __name__ == "__main__":
    argList = [
        ('-f','--force','force to show message even do not contain the module'),
        ('-s','--simple','show simple message')
    ]
    p = BaseParser(argList,'show')

    parser = p.get_parser()


    args = vars(parser.parse_args())

    print(args)