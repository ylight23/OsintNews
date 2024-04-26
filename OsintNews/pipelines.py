# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
import json


class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open('result.json', 'w')
        self.file.write("[\n")

    def close_spider(self, spider):
        self.file.write("\n]")
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + ",\n"
        self.file.write(line)
        return item


class OsintnewsPipeline:
    def process_item(self, item, spider):
        return item
    def __init__(self) :
        self.create_connection()
        self.create_table()
    def create_connection(self):
        self.conn = sqlite3.connect("osintnews.db")
        self.curr = self.conn.cursor()
    # def create_table(self):
    #     self.curr.execute("""DROP TABLE IF EXISTS article""")
    #     self.curr.execute("""CREATE TABLE "article" (
    #                 id	        INTEGER NOT NULL,
    #                 title	    VARCHAR(255) NOT NULL,
    #                 url 	    VARCHAR(255),
    #                 image_url	VARCHAR(255),
    #                 author	    VARCHAR(100) NOT NULL,
    #                 content	    TEXT NOT NULL,
    #                 created_at	DATETIME NOT NULL,
    #                 sentiment	VARCHAR(50),
    #                 is_fake 	BOOLEAN,
                    
    #                 PRIMARY KEY("id")
    #     )""")
    def process_item(self, item, spider):
        self.table_data(item)   
        return item
    
    def table_data(self, item):
        for data in range(len(item['title'])):
            self.curr.execute("""insert into article values (?,?,?,?,?,?,?,?)""",
            (
                item['title'][data],        
                item['url'][data],        
                item['image_url'][data],        
                item['author'][data],        
                item['content'][data],        
                item['created_at'][data],        
                item['sentiment'][data],        
                item['is_fake'][data]        
            ))
            self.conn.commit()