import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime, timedelta
import random
from scraper_base import NewsScraper
from fake_useragent import UserAgent


ua = UserAgent()
headers = {"User-Agent": ua.random}


class UolScraper(NewsScraper):
    def get_todays_news(self):
        news_list = []
        for pagina in range(1, self.get_pages_today_news() + 1):
            try:
                res = requests.get(f"https://noticias.uol.com.br/ultimas/?page={pagina}")
            except requests.exceptions.RequestException as e:
                print(f"Erro ao buscar página {pagina}: {e}")
                continue
            soup = BeautifulSoup(res.text, "html.parser")
            articles = soup.find_all("div", class_="thumbnails-wrapper")
            time.sleep(random.uniform(0.1, 0.5))


            for article in articles:
                a_tag = article.find("a")
                title_tag = a_tag.find("h3") if a_tag else None
                title = title_tag.text.strip() if title_tag else "Sem título"
                link = a_tag['href'] if a_tag else None
                timestamp = article.find("time", class_="thumb-date")
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
            res = requests.get(f"https://noticias.uol.com.br/ultimas/?page={paginas}")
            soup = BeautifulSoup(res.text, "html.parser")
            articles = soup.find_all("div", class_="thumbnails-wrapper")
            time.sleep(random.uniform(0.3, 0.6))
            stop = False
            print(f"Verificando página {paginas - 1}...")
            for article in articles:
                timestamp = article.find("time", class_="thumb-date")
                time_text = timestamp.text.strip() if timestamp else "Horário não encontrado"


                if time_text:
                    news_datetime = datetime.strptime(time_text, "%d/%m/%Y %Hh%M")
                    diference = datetime.now() - news_datetime


                    if diference > timedelta(hours=1):
                        stop = True
                        break
            paginas += 1
            if stop:
                break
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





