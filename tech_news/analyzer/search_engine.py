from tech_news.database import search_news
from datetime import datetime


# Requisito 6
def search_by_title(title):

    news_list = search_news({"title": {"$regex": f"{title.lower()}"}})
    if len(news_list) == 0:
        return []

    title_list = [(news["title"], news["url"]) for news in news_list]
    return title_list


# Requisito 7
def search_by_date(date):
    try:
        data_obj = datetime.strptime(date, "%Y-%m-%d")
        formated_date = datetime.strftime(data_obj, "%d/%m/%Y")

        news_list = search_news({"timestamp": formated_date})

        title_list = [
            tuple([news["title"], news["url"]]) for news in news_list
        ]
        return title_list

    except ValueError:
        raise ValueError("Data inválida")


# Requisito 8
def search_by_tag(tag):
    news_list = search_news({"tags": {"$regex": f"{tag}", "$options": "i"}})
    news = [(new["title"], new["url"]) for new in news_list]
    return news


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
