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
        inserted_count = 0
        try:
            with self.connection.cursor() as cursor:
                sql = f"INSERT INTO {portal_name} (title, link, scraping_date, news_date, article) VALUES (%s, %s, %s, %s, %s)"
                for news in news_list:
                    try:
                        cursor.execute(sql, (news['title'], news['link'], news['scraping_date'], news['news_date'], news['article']))
                        inserted_count += 1
                    except psycopg2.errors.UniqueViolation:
                        print(f"Notícia duplicada: {news['title']}")
                        self.connection.rollback() # Desfaz a operação
                    else:
                        self.connection.commit()
            print(f"\nColeta finalizada: ({len(news_list)} notícias coletadas e {inserted_count} inseridas com sucesso.)\n")
        except Exception as e:
            print(f"Erro ao inserir notícia: {e}")