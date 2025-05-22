import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime
import random
from scraper_base import NewsScraper
from fake_useragent import UserAgent


ua = UserAgent()
headers = {"User-Agent": ua.random}


class MoneyTimesScraper(NewsScraper):
    def get_news(self, period):
        news_list = []
        for pagina in range(1, self.get_pages_news(period)):
            try:
                res = requests.get(f"https://www.moneytimes.com.br/ultimas-noticias/page/{pagina}", timeout = 20)
            except requests.exceptions.RequestException as e:
                print(f"Erro ao buscar página {pagina}: {e}")
                continue
            soup = BeautifulSoup(res.text, "html.parser")
            articles = soup.find_all("div", class_="news-item__content")
            time.sleep(random.uniform(0.3, 0.6))
            for article in articles:
                title_tag = article.find("h2", class_="news-item__title")
                title = title_tag.text.strip() if title_tag else "Sem título"
                link = title_tag.find("a")["href"] if title_tag.find("a") else None
                timestamp = article.find("div", class_="news-item__meta")
                time_text = timestamp.text.strip() if timestamp else "Horário não encontrado"


                news_list.append({
                    "title": title,
                    "link": link,
                    "time": time_text,
                    "current_page": pagina
                })


        return news_list

    # Conta o número de páginas com notícias recentes
    def get_pages_news(self, period):
        paginas = 2
        while True:
            res = requests.get(f"https://www.moneytimes.com.br/ultimas-noticias/page/{paginas}")
            soup = BeautifulSoup(res.text, "html.parser")
            articles = soup.find_all("div", class_="news-item__content")
            time.sleep(random.uniform(0.1, 0.5))
            stop = False
            print(f"Verificando página {paginas - 1}...")
            for article in articles:
                timestamp = article.find("div", class_="news-item__meta")
                time_text = timestamp.text.strip() if timestamp else "Horário não encontrado"


                if not any(p in time_text.lower() for p in period):
                    stop = True
                    break
            if stop:
                break    
            paginas += 1
        return paginas

    # Conta ocorrências da keyword no artigo
    def count_keyword_in_article(self, url):
        try:
            response = requests.get(url)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")
            
            if "gestao.empiricus" in url:
                full_article = soup.find("div", class_="e-content")
                return self.get_article_text(full_article)
            elif "moneytimes" in url:
                full_article = soup.find("div", class_="single_block_news_text")
                return self.get_article_text(full_article)
            elif "seudinheiro" in url:
                full_article = soup.find("div", class_="newSingle_content")
                return self.get_article_text(full_article)
        except Exception as e:
            return e
        return None
    
    def get_article_text(self, full_article):
        all_paragraphs = full_article.find_all("p") if full_article.find("p") else 0
        text = " ".join([p.get_text(strip=True) for p in all_paragraphs])
        matches = re.findall(fr"\b{re.escape(self.keyword)}\b", text, flags=re.IGNORECASE)
        return len(matches)