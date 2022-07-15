# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3
import os


class ArticlesPipeline:

    def __init__(self):
        db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../db/articles.db')
        self.con = sqlite3.connect(db_path)
        self.c = self.con.cursor()
        #self.drop_table()
        self.create_table()

    def process_item(self, item, spider):
        self.insert_item(item)
        return item

    def insert_item(self, item):
        self.c.execute("""
            INSERT OR IGNORE INTO articles (name, link, date, labels, content) VALUES (?, ?, ?, ?, ?)
            """, (item['name'], item['link'], item['date'], str(item['labels']), item['content'])
            )
        self.con.commit()

    def create_table(self):
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS articles(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            link TEXT UNIQUE,
            date TEXT,
            labels TEXT,
            content TEXT
        )
        """)

    def drop_table(self):
        self.c.execute("""
            DROP TABLE articles;
        """)