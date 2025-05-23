
import cloudscraper
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime, timedelta
import random
from portals.scraper_base import NewsScraper
from fake_useragent import UserAgent


ua = UserAgent()
headers = {"User-Agent": ua.random}


class SunoScraper(NewsScraper):
    def get_news(self, period):
        news_list = []
        for pagina in range(1, self.get_pages_news(period)):
            try:
                res = cloudscraper.create_scraper().get(f"https://www.suno.com.br/noticias/todos/page/{pagina}", timeout = 20)
            except requests.exceptions.RequestException as e:
                print(f"Erro ao buscar página {pagina}: {e}")
                continue
            soup = BeautifulSoup(res.text, "html.parser")
            articles = soup.find_all("div", class_="cardsPage__listCard__boxs__content") # Container comum a todas as noticias
            time.sleep(random.uniform(0.3, 0.6))
            for article in articles:
                title_tag = article.find("h2", class_="content__title") if article.find("h2") else None
                title = title_tag.text.strip() if title_tag else "Sem título"
                link = article.find("a")["href"] if article else None
                timestamp = article.find("time", itemprop="datePublished")
                time_text = timestamp.get_text(separator=" ", strip=True) if timestamp else "Horário não encontrado"
                match = re.search(r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}', time_text)
                date_str = match.group()
                date_obj = datetime.strptime(date_str, "%d/%m/%Y %H:%M")


                news_list.append({
                    "title": title,
                    "link": link,
                    "time": date_obj,
                    "current_page": pagina
                })


        return news_list, pagina

    # Conta o número de páginas com notícias recentes
    def get_pages_news(self, period):
        paginas = 2
        while True:
            res = cloudscraper.create_scraper().get(f"https://www.suno.com.br/noticias/todos/page/{paginas}")
            soup = BeautifulSoup(res.text, "html.parser")
            articles = soup.find_all("div", class_="cardsPage__listCard__boxs__content")
            time.sleep(random.uniform(0.1, 0.5))
            stop = False
            print(f"Verificando página {paginas - 1}...")
            for article in articles:
                timestamp = article.find("time", itemprop="datePublished")
                time_text = timestamp.get_text(separator=" ", strip=True) if timestamp else "Horário não encontrado"
                match = re.search(r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}', time_text)
                date_str = match.group()
                date_obj = datetime.strptime(date_str, "%d/%m/%Y %H:%M")
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

    # Conta ocorrências da keyword no artigo. Essa função é usada quando trabalhamos com csv
    def count_keyword_in_article(self, url):
        try:
            response = cloudscraper.create_scraper().get(url)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")


            full_article = soup.find("div", class_="newsContent__box")
            all_paragraphs = full_article.find_all("p") if full_article.find("p") else None
            text = " ".join([p.get_text(strip=True) for p in all_paragraphs])
            matches = re.findall(fr"\b{re.escape(self.keyword)}\b", text, flags=re.IGNORECASE)
            return len(matches)
        except Exception as e:
            try:
                print("Erro no seletor, tentando outro...")
                response = cloudscraper.create_scraper().get(url)
                response.encoding = "utf-8"
                soup = BeautifulSoup(response.text, "html.parser")


                full_article = soup.find("div", class_="liveNews__updates")
                all_paragraphs = full_article.find_all("p") if full_article.find("p") else None
                text = " ".join([p.get_text(strip=True) for p in all_paragraphs])
                matches = re.findall(fr"\b{re.escape(self.keyword)}\b", text, flags=re.IGNORECASE)
                return len(matches)
            except Exception as e:
                print("Erro em ambos os seletores.")
                return e
            
    # Retorna o texto completo do artigo. Essa função é usada quando trabalhamos com MySQL
    def get_full_article(self, url):
        try:
            response = cloudscraper.create_scraper().get(url)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")


            full_article = soup.find("div", class_="newsContent__box")
            all_paragraphs = full_article.find_all("p") if full_article.find("p") else None
            text = " ".join([p.get_text(strip=True) for p in all_paragraphs])
            return text
        except Exception as e:
            try:
                print("Erro no seletor, tentando outro...")
                response = cloudscraper.create_scraper().get(url)
                response.encoding = "utf-8"
                soup = BeautifulSoup(response.text, "html.parser")


                full_article = soup.find("div", class_="liveNews__updates")
                all_paragraphs = full_article.find_all("p") if full_article.find("p") else None
                text = " ".join([p.get_text(separator=" ", strip=True) for p in all_paragraphs])
                return text
            except Exception as e:
                print("Erro em ambos os seletores.")
                return e