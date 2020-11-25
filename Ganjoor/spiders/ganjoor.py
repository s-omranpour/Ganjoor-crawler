# -*- coding: utf-8 -*-
import scrapy
import re
import json
import os


class GanjoorSpider(scrapy.Spider):
    name = 'ganjoor'
    allowed_domains = ['ganjoor.net']
    output_dir = '/Users/soroushomranpour/Desktop/Folders/crawlers/Ganjoor/data/'
    # custom_settings = {
    #     'CONCURRENT_REQUESTS': 64,
    #     'DOWNLOAD_DELAY': 0,
    #     'CONCURRENT_REQUESTS_PER_DOMAIN': 64,
    #     'ITEM_PIPELINES':{
    #         '.pipelines.ganjoor.ganjoorPipeline': 300,
    #     }
    # }
    
    def start_requests(self):
        url = 'https://ganjoor.net/'

        yield scrapy.Request(url, callback=self.poets_extractor)

    def poets_extractor(self, response):
        poets = response.xpath('//div[@class="poet"]/a/@href').extract()
        poets = list(set(poets))
        
        for poet in poets:
            author = poet.split('/')[-2]
            print(author)
            os.makedirs(self.output_dir + author, exist_ok=True)
            yield scrapy.Request(url=poet, callback=self.poems_extractor, meta={'author': author})

    def poems_extractor(self, response):
        url = response.url
        author = response.meta['author']
        links = response.xpath('//a/@href').extract()
        filter_links = lambda link: link.startswith(url) and url != link and (link.split('/')[-1][0] != '#' if link[-1] != '/' else link.split('/')[-2][0] != '#')
        poems = list(filter(filter_links, links))
        if len(poems) > 0:
            for poem in poems:
                yield scrapy.Request(url=poem, callback=self.poems_extractor, meta={'author': author})
        else:
            poem = ''
            audios = []
            m1 = response.xpath('//div[@class="m1"]/p/text()').extract()
            m2 = response.xpath('//div[@class="m2"]/p/text()').extract()
            for i in range(0,len(m1)):
                poem += m1[i]+'\n'+m2[i]+'\n'

            audio_script = response.xpath('//script[contains(.,"\n//<![CDATA[")]').get()
            if audio_script:
                audios = re.findall(r'https://i.ganjoor.net/a[0-9]*/[\-0-9a-z]+.mp3', audio_script)

            item = {
                'poem': poem,
                'audios': audios
            }

            name = '-'.join(url.replace('https://ganjoor.net/'+author+'/','')[:-1].split('/'))
            json.dump(item, open(self.output_dir + '/' + author + '/' + name + '.json', 'w'))