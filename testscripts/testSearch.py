'''
lanhuage: python
Descripttion: 
version: beta
Author: xiaoshuyui
Date: 2020-09-15 15:28:42
LastEditors: xiaoshuyui
LastEditTime: 2020-09-15 15:42:28
'''
from ruia import TextField, Item, Spider

class HackerNewItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')


class HackerNewSpider(Spider):
    start_urls = ['https://pypi.org/project/arsenic/']

    def parse(self, response):
        for item in HackerNewItem.get_item(html=response.html):
            yield item

if __name__ == "__main__":

    import asyncio

    from ruia import Request

    request = Request("https://pypi.org/project/arsenic/")
    response = asyncio.get_event_loop().run_until_complete(request.fetch())

    print(response.html)
    # HackerNewSpider.start()

    # print(HackerNewSpider.)