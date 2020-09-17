'''
lanhuage: python
Descripttion: 
version: beta
Author: xiaoshuyui
Date: 2020-09-17 08:31:44
LastEditors: xiaoshuyui
LastEditTime: 2020-09-17 14:18:14
'''
from pyquery import PyQuery



if __name__ == "__main__":
    s = PyQuery(url = 'https://cn.bing.com/search?q=stackoverflow.com%20%20print%20stack%20trace%20python')
    # print(s)
    with open('D:\\testALg\\ShowAndSearch\\show-and-search\\testscripts\\3.html','w',encoding='utf-8') as f:
        f.write(str(s))