# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd
import os


class Quote2Txt:

    def process_item(self, item, spider):
        # Save the txt file
        with open(item.file, 'w') as f:
            f.write(item.text)
            f.close()

        return item


class Quote2Csv:
    def process_item(self, item, spider):
        # Create CSV with pandas
        df = pd.DataFrame([[item.author, item.tags, item.page, item.rule, item.file]], columns=['autor', 'tags', 'número da página', 'número da regra', 'nome do arquivo txt correspondente'])
        if (os.path.isfile('storage/list.csv')):
            df.to_csv('storage/list.csv', mode='a', header=False)
        else:
            df.to_csv('storage/list.csv', index=False)

        return item
