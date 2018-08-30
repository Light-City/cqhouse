# -*- coding: utf-8 -*-
import re

import scrapy

from cqhouse import items


class CqhosespiderSpider(scrapy.Spider):
    name = 'CQSpider'
    allowed_domains = ['cq.newhouse.fang.com']
    # 'http://cq.newhouse.fang.com/house/s/daxuecheng/?ctm=1.cq.xf_search.lpsearch_area.15',
    start_urls = [
               'http://cq.newhouse.fang.com/house/s/yuzhong/?ctm=1.cq.xf_search.lpsearch_area.2',
               'http://cq.newhouse.fang.com/house/s/jiangbei/?ctm=1.cq.xf_search.lpsearch_area.3',
               'http://cq.newhouse.fang.com/house/s/jiangbei/b92/?ctm=1.cq.xf_search.page.2',
               'http://cq.newhouse.fang.com/house/s/jiangbei/b93/?ctm=1.cq.xf_search.page.4',]


    def parse(self, response):
        f = open('./wr.txt','w',encoding='utf8')
        f.write(response.text)
        # print(response.text)
        raw_lpname = response.xpath('//div[@class="nhouse_list"]/div[@id="newhouse_loupai_list"]/ul/li/div/div[@class="nlc_details"]/div[@class="house_value clearfix"]/div[@class="nlcd_name"]/a/text()').extract()
        lpname = self.parseBlank(raw_lpname)
        print(lpname)
        print(len(lpname))

        address_data = response.xpath('//div[@class="relative_message clearfix"]/div[@class="address"]')
        raw_address = address_data.xpath('string(.)').extract()
        address = self.parseBlank(raw_address)

        # address.pop(4)
        print(address)
        print(len(address))

        price_data = response.xpath('//div[@class="nlc_details"]/div[@class="nhouse_price"]')
        raw_price = price_data.xpath('string(.)').extract()
        price = self.parseBlank(raw_price)
        # if self.start_urls[0] == 'http://cq.newhouse.fang.com/house/s/daxuecheng/?ctm=1.cq.xf_search.lpsearch_area.15':
        #     self.start_urls.pop(0)
        # price.insert(0,'价格待定')
        print(price)
        print(len(price))
        item = items.CqhouseItem()
        item['lpname'] = lpname
        item['address'] = address
        item['price'] = price
        yield item
    def parseBlank(self,ls):
        lp = []
        for each in ls:
            name = re.sub(r'\s+', '', each)
            lp.append(name)
        return lp
