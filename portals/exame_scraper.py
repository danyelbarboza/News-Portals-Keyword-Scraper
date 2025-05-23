import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime, timedelta
import random
from portals.scraper_base import NewsScraper
from fake_useragent import UserAgent


ua = UserAgent()
headers = {"User-Agent": ua.random}


class ExameScraper(NewsScraper):
    def get_news(self, period):
        pagina = 1
        news_list = []
        for pagina in range(1, self.get_pages_news(period)):
            try:
                res = requests.get(f"https://exame.com/ultimas-noticias/{pagina}", timeout = 20)
            except requests.exceptions.RequestException as e:
                print(f"Erro ao buscar página {pagina}: {e}")
                continue
            soup = BeautifulSoup(res.text, "html.parser")
            articles = soup.find_all("div", class_="sc-c60789b2-9 hhwgFF") # Extrai as notícias
            time.sleep(random.uniform(0.3, 0.6))
            all_script_text = " ".join(script.get_text() for script in soup.find_all("script"))
            date_matches = list(re.finditer(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', all_script_text))
            dates = [datetime.strptime(m.group(), "%Y-%m-%dT%H:%M:%S") for m in date_matches]

            for idx, article in enumerate(articles):
                title_tag = article.find("h3").find("a") if article.find("h3") else None
                title = title_tag.text.strip() if title_tag else "Sem título"
                link = title_tag["href"] if title_tag else None
                date_obj = dates[idx] if idx < len(dates) else None  


                news_list.append({
                    "title": title,
                    "link": f"https://exame.com{link}",
                    "time": date_obj,
                    "current_page": pagina
                })


        return news_list, pagina

    # Conta o número de páginas com notícias recentes
    def get_pages_news(self, period):
        paginas = 1
        stop = False
        while True:
            res = requests.get(f"https://exame.com/ultimas-noticias/{paginas}")
            soup = BeautifulSoup(res.text, "html.parser")
            time.sleep(random.uniform(0.1, 0.5))
            print(f"Verificando página {paginas}...")
            script = soup.find_all("script")
            for script in script:
                script_text = script.get_text()
                matches = re.findall(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', script_text)
                for date_str in matches:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
                    diference = datetime.now() - date_obj
                    if period == 1:
                        if diference > timedelta(hours=1):
                            stop = True
                            break
                    elif period == 2:
                        if diference > timedelta(days=1):
                            stop = True
                            break
                    elif period == 3:
                        if diference > timedelta(days=7):
                            stop = True
                            break
                    elif period == 4:
                        if diference > timedelta(days=30):
                            stop = True
                            break
                    
            if stop:
                break    
            paginas += 1
        return paginas

    # Conta ocorrências da keyword no artigo. Essa função é usada quando trabalhamos com CSV
    def count_keyword_in_article(self, url):
        try:
            response = requests.get(f"https://exame.com{url}")
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")


            full_article = soup.find_all("p", class_="m-0 p-0 xl:text-pretty body-extra-large overflow-hidden py-3 text-colors-text dark:text-colors-background lg:py-4")
            if full_article:
                text = " ".join([p.get_text(strip=True) for p in full_article])
                matches = re.findall(fr"\b{re.escape(self.keyword)}\b", text, flags=re.IGNORECASE)
                return len(matches)
        except Exception as e:
            return e
        return None
    
    # Retorna o texto completo do artigo. Essa função é usada quando trabalhamos com MySQL
    def get_full_article(self, url):
        try:
            response = requests.get(f"https://exame.com{url}")
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")


            full_article = soup.find_all("p", class_="m-0 p-0 xl:text-pretty body-extra-large overflow-hidden py-3 text-colors-text dark:text-colors-background lg:py-4")
            text = " ".join([p.get_text(separator=" ", strip=True) for p in full_article])
            return text
        except Exception as e:
            return e