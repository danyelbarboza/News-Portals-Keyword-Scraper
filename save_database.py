import pymysql
from dotenv import load_dotenv
import os

load_dotenv()


class Database():
    def __init__(self):
        self.connection = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            db=os.getenv("DB_NAME"),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
    
    def insert_news(self, news_list, portal_name):
        try:
            with self.connection.cursor() as cursor:
                sql = f"INSERT INTO {portal_name} (title, link, scraping_date, news_date, article) VALUES (%s, %s, %s, %s, %s)"
                for news in news_list:
                    cursor.execute(sql, (news['title'], news['link'], news['scraping_date'], news['news_date'], news['article']))
            self.connection.commit()
            print(f"\nColeta finalizada ({len(news_list)} notícias salvas no banco de dados)\n")
        except Exception as e:
            print(f"Erro ao inserir notícia: {e}")