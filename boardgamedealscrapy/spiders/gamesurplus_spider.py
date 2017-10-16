import scrapy
from boardgamedealscrapy.items import BoardgamedealscrapyItem

class GameSurPlusSpider(scrapy.Spider):
    name = "gamesurplus_spider"

    def start_requests(self):
        urls = [
            'https://www.gamesurplus.com/product-category/board-games/'
        ]
        for i in range(2,25):
            print 'scrapy on page' + str(i)
            urls.append('https://www.gamesurplus.com/product-category/board-games/page/{0}/'.format(i))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        games = response.xpath('//a[@class="woocommerce-LoopProduct-link woocommerce-loop-product__link"]')
        for game in games:
            item = BoardgamedealscrapyItem()
            item['name'] = game.xpath('.//h2[@class="woocommerce-loop-product__title"]//text()').extract()[0]

            original_price = game.xpath('.//span[@class="woocommerce-Price-amount amount"]//text()').extract()
            prices = filter(lambda p:p != '$', original_price)
            item['original_price'] = prices[0]
            if len(prices) > 1:
                item['price'] = prices[1]
            else:
                item['price'] = item['original_price']

            item['url'] = game.xpath('@href').extract()[0]

            item['img_url'] = game.xpath('.//img//@src').extract()[0]

            yield item