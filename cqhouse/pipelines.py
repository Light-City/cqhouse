# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import pymysql


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):

        self.db[item.collection].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()

class MysqlPipeline(object):
    def process_item(self, item, spider):
        '''
        将爬取的信息保存到mysql
        '''

        connection = pymysql.connect(host='localhost', user='root', password='0312', db='scrapydb',
                                     charset='utf8mb4')
        try:

            with connection.cursor() as cursor:
                for i in range(len(item['lpname'])):
                    sql = "insert into `cqhouse`(`lpname`,`address`,`price`)values(%s,%s,%s)"
                    cursor.execute(sql, (
                        item['lpname'][i], item['address'][i], item['price'][i]))

                    connection.commit()
        # except pymysql.err.IntegrityError as e:
        #     print('重复数据，勿再次插入!')
        finally:
            connection.close()

        return item