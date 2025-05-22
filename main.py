import csv
from datetime import datetime
from g1_scraper import G1Scraper
from exame_scraper import ExameScraper
from carta_scraper import CartaCapitalScraper
from suno_scraper import SunoScraper
from moneytimes_scraper import MoneyTimesScraper

def save_to_csv(news_data):
    CSV_FILE = f"{portal_name}_keyword_noticias.csv"
    fieldnames = ["data_coleta", "titulo", "link", "horario", "keyword_count", "keyword_used"]
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
       
        try:
            f.seek(0)
            if f.read(1) == "":
                writer.writeheader()
        except:
            pass


        for row in news_data:
            row["keyword_used"] = keyword
            writer.writerow(row)


def run_scraper(portal_scaper, period):
    keyword_total_count = 0
    keyword_count = 0
    noticias = portal_scaper.get_news(period)
    resultados = []
    data_coleta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   
    for item in noticias:
        keyword_count = portal_scaper.count_keyword_in_article(item['link']) if item['link'] else None
        resultados.append({
            "data_coleta": data_coleta,
            "titulo": item['title'],
            "link": item['link'],
            "horario": item['time'],
            "keyword_count": keyword_count
        })
        print(f"Coletado: {item['title']} - Keyword: {keyword_count}")
        print(f"Página atual: {item['current_page']}")
        keyword_total_count += keyword_count if keyword_count is not None else 0


    save_to_csv(resultados)
    print(f"\nColeta finalizada ({len(resultados)} notícias salvas)")
    print(f"Keyword total: {keyword_total_count}")
    

if __name__ == "__main__":
    keyword = input("\nBem-vindo ao Keyword Monitor!\nEssa ferramenta coleta notícias de portais brasileiros e conta a quantidade de ocorrências de uma palavra-chave no corpo de cada artigo.\n\nDigite a keyword que deseja analisar: ")
    while True:
        portal = input("\nVocê deseja analisar qual desses portais?\n1 - G1\n2 - Exame\n3 - Carta Capital\n4 - Money Times\n5 - Suno\n")
        if portal == "1":
            g1_scraper = G1Scraper(keyword)
            portal_name = "g1"
            periodo = input("\nVocê deseja analisar qual período?\n1 - 1 hora\n2 - Hoje \n3 - 7 dias\n")
            if periodo == "1":
                run_scraper(g1_scraper, ['minuto', 'minutos'])
            elif periodo == "2":
                run_scraper(g1_scraper, ['minuto', 'minutos', 'hora', 'horas'])
            elif periodo == "3":
                run_scraper(g1_scraper, ['minuto', 'minutos', 'hora', 'horas', "ontem", 'dia', 'dias'])
            break
        elif portal == "2":
            exame_scraper = ExameScraper(keyword)
            portal_name = "exame"
            periodo = input("\nVocê deseja analisar qual período?\n1 - 1 hora\n2 - Hoje\n3 - 7 dias\n4 - 30 dias\n")
            if periodo == "1":
                run_scraper(exame_scraper,1)
            elif periodo == "2":
                run_scraper(exame_scraper, 2)
            elif periodo == "3":
                run_scraper(exame_scraper, 3)
            elif periodo == "4":
                run_scraper(exame_scraper, 4)
            break
        elif portal == "3":
            carta_scraper = CartaCapitalScraper(keyword)
            portal_name = "carta"
            periodo = input("\nVocê deseja analisar qual período?\n1 - 1 hora\n2 - Hoje\n3 - 7 dias\n4 - 30 dias\n")
            if periodo == "1":
                run_scraper(carta_scraper,1)
            elif periodo == "2":
                run_scraper(carta_scraper, 2)
            elif periodo == "3":
                run_scraper(carta_scraper, 3)
            elif periodo == "4":
                run_scraper(carta_scraper, 4)
            break
        elif portal == "4":
            moneytimes_scraper = MoneyTimesScraper(keyword)
            portal_name = "moneytimes"
            periodo = input("\nVocê deseja analisar qual período?\n1 - 1 hora\n2 - Hoje\n3 - 30 dias\n")
            if periodo == "1":
                run_scraper(moneytimes_scraper,['minuto', 'minutos'])
            elif periodo == "2":
                run_scraper(moneytimes_scraper, ['minuto', 'minutos', 'hora', 'horas'])
            elif periodo == "3":
                run_scraper(moneytimes_scraper, ['minuto', 'minutos', 'hora', 'horas', "ontem", 'dia', 'dias'])
            break
        elif portal == "5":
            suno_scraper = SunoScraper(keyword)
            portal_name = "suno"
            periodo = input("\nVocê deseja analisar qual período?\n1 - 1 hora\n2 - Hoje\n3 - 7 dias\n4 - 30 dias\n")
            if periodo == "1":
                run_scraper(suno_scraper,1)
            elif periodo == "2":
                run_scraper(suno_scraper, 2)
            elif periodo == "3":
                run_scraper(suno_scraper, 3)
            elif periodo == "4":
                run_scraper(suno_scraper, 4)
            else:
                print("\n===========\nOpção inválida. Tente novamente.\n===========\n")
                continue
            break
        else:
            print("\n===========\nOpção inválida. Tente novamente.\n===========\n")
            continue