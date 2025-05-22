from abc import ABC, abstractmethod

class NewsScraper(ABC):
    def __init__(self, keyword):
        self.keyword = keyword

    @abstractmethod
    def get_news(self, period):
        pass

    @abstractmethod
    def count_keyword_in_article(self, url):
        pass
