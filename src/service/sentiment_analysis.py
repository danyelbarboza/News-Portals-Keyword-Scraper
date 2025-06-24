from transformers import pipeline
import re

class SentimentAnalysis:
    def __init__(self):
        self.classificador_sentimento = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-xlm-roberta-base-sentiment",
            truncation=True, 
            max_length=512
        )

    def analyze(self, news_list):
        caracteres = 150
        analysis = []

        for news in news_list:
            text = news['article'][:caracteres].ljust(caracteres)
            text = re.sub(r'["\']', '', text)

            resultado = self.classificador_sentimento(text)
            label = resultado[0]['label']
            score = resultado[0]['score']
            rounded_score = round(score, 2)
            analysis.append({
                "title": news['title'],
                "link": news['link'],
                "scraping_date": news['scraping_date'],
                "news_date": news['news_date'],
                "article": news['article'],
                "sentiment_analysis": label,
                "confidence_score": rounded_score
            })
        return analysis