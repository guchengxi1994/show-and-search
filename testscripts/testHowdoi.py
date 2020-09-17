'''
lanhuage: python
Descripttion: 
version: beta
Author: xiaoshuyui
Date: 2020-09-17 13:37:49
LastEditors: xiaoshuyui
LastEditTime: 2020-09-17 14:13:25
'''
import sys
sys.path.append('..')
import requests

from ShowAndSearch.utils.search.searchWeb import script

if __name__ == "__main__":
    x = script(' print stack trace python')
    print(x)

    r = requests.get('https://cn.bing.com/search?q=stackoverflow.com%20%20print%20stack%20trace%20python&toHttps=1&redig=4C72A2C577E941C7A802A1B46268FAAD')

    # print(r.text)

    with open('D:\\testALg\\ShowAndSearch\\show-and-search\\testscripts\\2.html','w',encoding='utf-8') as f:
        f.write(str(r.text))

    