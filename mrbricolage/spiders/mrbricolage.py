# -*- coding: utf-8 -*-
import scrapy
import re

class MrBricolage(scrapy.Spider):
    name = "products"
    start_urls = ["https://www.mr-bricolage.bg/bg/Instrumenti/Avto-i-veloaksesoari/Veloaksesoari/c/006008012"]
    
    def parse(self, response):
        for product_url in response.css("div.title a::attr(href)").extract():
            yield response.follow(product_url, callback = self.parse_product)
        next_page = response.css("li.pagination-next a::attr(href)").extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback = self.parse)

    def parse_product(self, response):
        name = response.css("div.row div.col-md-6 h1::text").extract_first()
        price = response.css("div.row div.col-md-6 p.price::text").extract_first().strip()
        price = re.sub("[^,0-9]", "" , price)
        price = re.sub("," , "." , price)
        picture = response.css("div.row div.col-md-6 div img::attr(src)").extract_first()
        rows = response.css("table.table tr")
        characteristics = {}
        for row in rows:
            key = row.css("td::text").extract()[0]
            value = row.css("td::text").extract()[1].strip()
            characteristics[key] = value 
        yield {"product_name" : name , 
               "product_price" : price ,
               "product_picture" : picture ,
               "product_characteristics" : characteristics}
        
        
        