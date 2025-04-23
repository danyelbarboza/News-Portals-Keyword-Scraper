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


class G1Scraper(NewsScraper):
    def get_todays_news(self):
        news_list = []
        for pagina in range(1, self.get_pages_today_news() + 1):
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


        return news_list


    def get_pages_today_news(self):
        paginas = 2
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


                if not any(p in time_text.lower() for p in ['minuto', 'minutos']):
                    stop = True
                    break
               
            if stop:
                break    
            paginas += 1


        return paginas


    def count_keyword_in_article(self, url):
        try:
            response = requests.get(url)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")


            article = soup.find("article")
            if article:
                text = article.get_text(separator=" ", strip=True)
                matches = re.findall(fr"\b{re.escape(self.keyword)}\b", text, flags=re.IGNORECASE)
                return len(matches)
        except:
            return None
        return None