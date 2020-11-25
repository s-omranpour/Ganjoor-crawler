# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class GanjoorPipeline:
    def process_item(self, item, spider):
        return item
        # if item['output_dir'] != '':
        #     os.system('mkdir -p {}'.format(item['output_dir']))
        # else:
        #     item['output_dir'] = 'data'
        #     os.system('mkdir -p {}'.format(item['output_dir']))
        # with open(item['output_dir']+'/'+item['author']+'.json', 'a+') as file:
        #     del item['output_dir']
        #     line = json.dumps(dict(item)) + "\n"
        #     file.write(line)
        #     return item