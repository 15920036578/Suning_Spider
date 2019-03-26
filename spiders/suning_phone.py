# -*- coding: utf-8 -*-
__author__ = 'Gobi Xu'


import scrapy
import re
import json
import datetime
from Article.items import Suning_phoneItem


# 商品列表页 一共有 50页
# 每页分为4层，直接请求 商品列表页地址 的话，只会显示第一层，其余 3层 是用户下拉后 异步加载出来的，使用抓包的方法可以截取到，所以每一页都分为 4步来分别请求
# 商品详情页 可以加载出 商品价格页，携带 商品的id 即可请求


class SuningPhoneSpider(scrapy.Spider):
    name = 'suning_phone'
    allowed_domains = ['suning.com']
    # start_urls = ['https://search.suning.com/emall/searchV1Product.do?keyword={0}&pg=01&cp=0&paging=0'.format(keyword)]
    # 需要爬取的 类目
    keyword = '手机'
    # 商品列表页的 初始页
    page = 0
    # 商品列表页的 层数
    layer = 0
    # 商品列表页的 地址
    url = 'https://search.suning.com/emall/searchV1Product.do?keyword={0}&pg=01&cp=%d&paging=%d'.format(keyword)
    # 商品价格页的 地址
    price_url = 'https://icps.suning.com/icps-web/getVarnishAllPriceNoCache/0000000%s_010_0100101_0000000000_1_getClusterPrice.jsonp?callback=getClusterPrice'

    # custom_settings = {}

    def start_requests(self):
        yield scrapy.Request(url=self.url%(self.page,self.layer), callback=self.parse)

    def parse(self, response):
        # 获取 商品列表页 的所有商品
        goodsInfoList = response.css('.item-wrap')
        for goodsInfo in goodsInfoList:
            # 获取 id 并清洗
            id = goodsInfo.css('.item-wrap::attr(id)').extract()[0].split('-')[1]
            # 获取 详情页地址 并清洗
            url = ''.join(['https:', goodsInfo.css('.img-block a::attr(href)').extract()[0]])
            # 获取 标题
            title = goodsInfo.css('.img-block a img::attr(alt)').extract_first('')
            # 获取 评论数 并清洗
            comment_count = goodsInfo.css('.evaluate-old.clearfix .info-evaluate a i::text').extract_first('0').strip('+')
            # 进一步清洗 评论数
            comment_count = int(float(comment_count.strip('万'))*10000) if comment_count.endswith('万') else int(comment_count)
            # 获取 店名
            shop_name = goodsInfo.css('.store-stock a::text').extract_first('')
            # 回调去处理 parseDetail函数（处理商品详情页函数）
            yield scrapy.Request(url=url, callback=self.parseDetail, meta={'id':id,'url':url,'title':title,'comment_count':comment_count,'shop_name':shop_name})
        # 判断 商品列表页 层数 并 回调 parse函数（处理商品列表页函数）
        if self.layer < 3 and self.page < 50:
            self.layer += 1
            yield scrapy.Request(url=self.url%(self.page,self.layer), callback=self.parse)  # meta={'download_timeout':3}（设置超时时间）
        if self.layer == 3 and self.page < 49:
            self.layer = 0
            self.page += 1
            yield scrapy.Request(url=self.url%(self.page,self.layer), callback=self.parse)

    def parseDetail(self, response):
        # 获取 商品品牌
        brand = response.css('.dropdown-text a::text').extract()[2] if len(response.css('.dropdown-text').extract()) == 3 else ''
        # 获取 商品型号 并 清洗
        model_clean = brand.split('(')
        model = response.css('.breadcrumb-title::attr(title)').extract_first('')
        model = model.replace(model_clean[0], '').replace(''.join(['(', model_clean[1]]), '').replace('手机', '') if len(model_clean) == 2 else model.replace(model_clean[0], '').replace('手机', '')
        # 回调去处理 parsePrice函数（处理商品价格页函数）
        yield scrapy.Request(url=self.price_url%(response.meta['id']), callback=self.parsePrice, meta={'id':response.meta['id'],'url':response.meta['url'],'title':response.meta['title'],'comment_count':response.meta['comment_count'],'shop_name':response.meta['shop_name'],'brand':brand,'model':model})

    def parsePrice(self, response):
        # 获取 商品价格信息 的json 并 清洗
        text = response.text
        price_info = re.match('.*getClusterPrice\(?(.+)\).*', text, re.S).group(1)
        price = json.loads(price_info)[0]['price']
        price = float(price) if price else 0.0
        # 传入item
        item = Suning_phoneItem()
        item['id'] = response.meta['id']
        item['title'] = response.meta['title']
        item['price'] = price
        item['brand'] = response.meta['brand']
        item['model'] = response.meta['model']
        item['shop_name'] = response.meta['shop_name']
        item['comment_count'] = response.meta['comment_count']
        item['url'] = response.meta['url']
        item['crawl_date'] = datetime.datetime.now()
        yield item
