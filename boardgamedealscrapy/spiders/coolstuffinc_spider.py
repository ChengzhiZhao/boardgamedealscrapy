import scrapy
import re
from boardgamedealscrapy.items import BoardgamedealscrapyItem

class CollStuffIncSpider(scrapy.Spider):
    name = "coolstuffinc_spider"

    def start_requests(self):
        urls = []
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for i in range(1,3):
            print 'scrapy on page' + str(i)
            urls.append('https://www.coolstuffinc.com/main_saleItems.php?p={0}&s=5&sb=ratings|desc'.format(i))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response):
        games = response.xpath('//div[@class="product"]')

        for game in games:
            item = BoardgamedealscrapyItem()
            if game.xpath('.//p[@class="product-name expand"]//text()').extract() != []:
                item['name'] = game.xpath('.//p[@class="product-name expand"]//text()').extract()
            else:
                item['name'] = game.xpath('.//p[@class="product-name "]//text()').extract()

            item['original_price'] = game.xpath('.//span[@class="product-msrp"]//text()').extract()[0]

            item['price'] = game.xpath('.//span[@class="product-price"]//text()').extract()[0]

            item['url'] = game.xpath('.//a/@href').extract()[0]

            item['img_url'] = game.xpath('.//img//@src').extract()[0]

            yield item