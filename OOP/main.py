import csv
from datetime import datetime
from g1_scraper import G1Scraper
from uol_scraper import UolScraper


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


def run_scraper(portal_scaper):
    keyword_total_count = 0
    keyword_count = 0
    noticias = portal_scaper.get_todays_news()
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
    print(f"Coleta finalizada ({len(resultados)} notícias salvas)")
    print(f"Keyword total: {keyword_total_count}")


if __name__ == "__main__":
    keyword = input("Digite a keyword que deseja analisar: ")
    while True:
        portal = input(f"Você deseja analisar qual desses portais?\n1 - G1\n2 - UOL\n")
        if portal == "1":
            g1_scraper = G1Scraper(keyword)
            portal_name = "g1"
            run_scraper(g1_scraper)
            break
        elif portal == "2":
            uol_scraper = UolScraper(keyword)
            portal_name = "uol"
            run_scraper(uol_scraper)
            break
        else:
            print("\n===========\nOpção inválida. Tente novamente.\n===========\n")
            continue