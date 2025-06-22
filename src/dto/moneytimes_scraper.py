import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime
import random
from fake_useragent import UserAgent
from service.save_database import Database

ua = UserAgent()
headers = {"User-Agent": ua.random}


class MoneyTimesScraper():
    def get_news(self, period):
        news_list = []
        pagina = 1
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
                if Database().verify_news("moneytimes", title, link): # Verifica se a notícia já foi coletada
                    continue
                timestamp = article.find("div", class_="news-item__meta")
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

    # Conta ocorrências da keyword no artigo. Essa função é usada quando trabalhamos com CSV
    def count_keyword_in_article(self, url):
        try:
            response = requests.get(url)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")
            
            if "gestao.empiricus" in url:
                full_article = soup.find("div", class_="e-content")
                return self.get_keywords(full_article)
            elif "moneytimes" in url:
                full_article = soup.find("div", class_="single_block_news_text")
                return self.get_keywords(full_article)
            elif "seudinheiro" in url:
                full_article = soup.find("div", class_="newSingle_content")
                return self.get_keywords(full_article)
        except Exception as e:
            return e
        return None
    
    def get_keywords(self, full_article):
        all_paragraphs = full_article.find_all("p") if full_article.find("p") else 0
        text = " ".join([p.get_text(strip=True) for p in all_paragraphs])
        matches = re.findall(fr"\b{re.escape(self.keyword)}\b", text, flags=re.IGNORECASE)
        return len(matches)
    
    # Retorna o texto completo do artigo. Essa função é usada quando trabalhamos com MySQL
    def get_full_article(self, url):
        try:
            response = requests.get(url)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")

            if "gestao.empiricus.com.br" in url:
                full_article = soup.find("div", class_="e-content")
                all_paragraphs = full_article.find_all("p") if full_article.find("p") else None
                if all_paragraphs is None:
                    return None, None
                text = " ".join([p.get_text(separator=" ", strip=True) for p in all_paragraphs])
                
                timestamp = soup.find("p", class_="authorSingle_infos_att")
                time_text = timestamp.get_text(separator=" ", strip=True) if timestamp else "Horário não encontrado"
                # Exemplo de time_text: "25 de março de 2025, 12:30". Essa regex abaixo coloca cada parte em uma caixa para depois puxar o mês do dicionário "meses".
                dia, mes_str, ano, hora, minuto = re.match(r'(\d{1,2}) (\w+) (\d{4}), (\d{1,2}):(\d{2})', time_text).groups()

                meses = {
                    "janeiro": 1, "fevereiro": 2, "março": 3, "abril": 4,
                    "maio": 5, "junho": 6, "julho": 7, "agosto": 8,
                    "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12
                }

                date_obj = datetime(int(ano), meses[mes_str], int(dia), int(hora), int(minuto))
                return text, date_obj
            
            if "empiricus.com.br" in url:
                full_article = soup.find("div", class_="paragraph-1 content-text content-text-post")
                all_paragraphs = full_article.find_all("p") if full_article.find("p") else None
                if all_paragraphs is None:
                    return None, None
                text = " ".join([p.get_text(separator=" ", strip=True) for p in all_paragraphs])
                
                timestamp = soup.find("p", class_="content-single-header-author-info")
                time_text = timestamp.get_text(separator=" ", strip=True) if timestamp else "Horário não encontrado"
                dia, mes_str, ano, hora, minuto = re.match(r'(\d{1,2}) (\w+) (\d{4}), (\d{1,2}):(\d{2})', time_text).groups()

                meses = {
                    "janeiro": 1, "fevereiro": 2, "março": 3, "abril": 4,
                    "maio": 5, "junho": 6, "julho": 7, "agosto": 8,
                    "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12
                }

                date_obj = datetime(int(ano), meses[mes_str], int(dia), int(hora), int(minuto))
                return text, date_obj
            
            
            elif "moneytimes.com.br" in url:
                full_article = soup.find("div", class_="single_block_news_text")
                all_paragraphs = full_article.find_all("p") if full_article.find("p") else None
                if all_paragraphs is None:
                    return None, None
                text = " ".join([p.get_text(separator=" ", strip=True) for p in all_paragraphs])
                
                timestamp = soup.find("span", class_="single_meta_author_infos_date_time")
                time_text = timestamp.get_text(separator=" ", strip=True) if timestamp else "Horário não encontrado"
                dia, mes_str, ano, hora, minuto = re.match(r'(\d{1,2}) (\w+) (\d{4}), (\d{1,2}):(\d{2})', time_text).groups()
                
                meses = {
                    "janeiro": 1, "fevereiro": 2, "março": 3, "abril": 4,
                    "maio": 5, "junho": 6, "julho": 7, "agosto": 8,
                    "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12
                }
                date_obj = datetime(int(ano), meses[mes_str], int(dia), int(hora), int(minuto))
                return text, date_obj
            
            
            elif "seudinheiro.com" in url:
                full_article = soup.find("div", class_="newSingle_content")
                all_paragraphs = full_article.find_all("p") if full_article.find("p") else None
                if all_paragraphs is None:
                    return None, None
                text = " ".join([p.get_text(separator=" ", strip=True) for p in all_paragraphs])
                
                timestamp = soup.find("div", class_="js-first-letter single__date-time")
                time_text = timestamp.get_text(separator=" ", strip=True) if timestamp else "Data não encontrada"
                
                dia, mes_str, ano, hora, minuto = re.match(r'(\d{1,2}) de (\w+) de (\d{4}) (\d{1,2}):(\d{2})', time_text).groups()

                meses = {
                    "janeiro": 1, "fevereiro": 2, "março": 3, "abril": 4,
                    "maio": 5, "junho": 6, "julho": 7, "agosto": 8,
                    "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12
                }

                date_obj = datetime(int(ano), meses[mes_str], int(dia), int(hora), int(minuto))
                return text, date_obj
        except Exception as e:
            return e