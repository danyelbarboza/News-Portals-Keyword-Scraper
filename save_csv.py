import csv

class SaveCSV:
    def save_to_csv(news_data, portal_name, keyword):
        CSV_FILE = f"{portal_name}_keyword_noticias.csv"
        fieldnames = ["titulo", "link", "scraping_date", "news_date", "keyword_count", "keyword_used"]
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