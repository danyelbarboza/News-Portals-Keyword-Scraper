import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime
import random
from portals.scraper_base import NewsScraper
from fake_useragent import UserAgent


ua = UserAgent()
headers = {"User-Agent": ua.random}


class G1Scraper(NewsScraper):
    def get_news(self, period):
        news_list = []
        for pagina in range(1, self.get_pages_news(period)):
            try:
                res = requests.get(f"https://g1.globo.com/ultimas-noticias/index/feed/pagina-{pagina}.ghtml", timeout = 20)
            except requests.exceptions.RequestException as e:
                print(f"Erro ao buscar página {pagina}: {e}")
                continue
            soup = BeautifulSoup(res.text, "html.parser")
            articles = soup.find_all("div", class_="feed-post-body")
            time.sleep(random.uniform(0.3, 0.6))
            for article in articles:
                title_tag = article.find("a", class_="feed-post-link")
                title = title_tag.text.strip() if title_tag else "Sem título"
                link = title_tag["href"] if title_tag else None
                timestamp = article.find("span", class_="feed-post-datetime")
                time_text = timestamp.text.strip() if timestamp else "Horário não encontrado"


                news_list.append({
                    "title": title,
                    "link": link,
                    "time": time_text,
                    "current_page": pagina
                })


        return news_list, pagina

    # Conta o número de páginas com notícias recentes
    def get_pages_news(self, period):
        paginas = 1
        while True:
            res = requests.get(f"https://g1.globo.com/ultimas-noticias/index/feed/pagina-{paginas}.ghtml")
            soup = BeautifulSoup(res.text, "html.parser")
            articles = soup.find_all("div", class_="feed-post-body")
            time.sleep(random.uniform(0.1, 0.5))
            stop = False
            print(f"Verificando página {paginas - 1}...")
            for article in articles:
                timestamp = article.find("span", class_="feed-post-datetime")
                time_text = timestamp.text.strip() if timestamp else "Horário não encontrado"


                if not any(p in time_text.lower() for p in period):
                    stop = True
                    break
            if stop:
                break    
            paginas += 1
        return paginas

    # Conta ocorrências da keyword no artigo. Essa função é usada quando trabalhamos com CSV
    def count_keyword_in_article(self, url):
        try:
            response = requests.get(url)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")


            full_article = soup.find("article")
            if full_article:
                text = full_article.get_text(separator=" ", strip=True)
                matches = re.findall(fr"\b{re.escape(self.keyword)}\b", text, flags=re.IGNORECASE)
                return len(matches)
        except Exception as e:
            return e
        return None
    
    # Retorna o texto completo do artigo. Essa função é usada quando trabalhamos com MySQL
    def get_full_article(self, url):
        try:
            response = requests.get(url)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")


            full_article = soup.find("article")
            all_paragraphs = full_article.find_all("p") if full_article.find("p") else None
            text = " ".join([p.get_text(separator=" ", strip=True) for p in all_paragraphs])
            return text
        except Exception as e:
            return e