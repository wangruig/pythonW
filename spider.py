# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from Demo.items import DemoItem
class StackSpider(BaseSpider):
   name = "dongfang"
   allowed_domains = ["guba.eastmoney.com"]
   start_urls = ["http://guba.eastmoney.com/list,600482_1.html"]

   rules = [
      Rule(SgmlLinkExtractor(allow=(r'http://guba.eastmoney.com/default_1.html\?start=\d+.*'))),
      Rule(SgmlLinkExtractor(allow=(r'http://guba.eastmoney.com/subject/\d+')), callback="parse_item"),
   ]
   for i in range (1,1150,1):
       start_urls.append('http://guba.eastmoney.com/list,600482_%d.html'%i)
   def parse(self, response):
       hxs = HtmlXPathSelector(response)
       sites = hxs.select('/html/body[@class="hlbody"]/div[@class="gbbody"][5]/div[@id="mainbody"]/div[@id="articlelistnew"]/div[@class="articleh"]')
       #sites = hxs.select('ml/body[@class="hlbody"]/div[@class="gbbody"][5]/div[@id="mainbody"]/div[@id="articlelistnew"]/div[@class="articleh"]')
       items = []
       for site in sites:
           item = DemoItem()
           item['title'] = site.select('span[@class="l3"]/a/text()').extract()
           #item['readtime'] = site.select('cite[@class="date"]/text()').extract()
           item['lasttime'] = site.select('cite[@class="last"]/text()').extract()
           items.append(item)
       return items