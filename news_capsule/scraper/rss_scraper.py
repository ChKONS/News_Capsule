import requests
from bs4 import BeautifulSoup


class FailureToConnect(Exception):
    pass


def scrape_rss(url):
    news_articles_list = list()

    try:
        request = requests.get(url)
        xml_data = BeautifulSoup(request.content, features="xml")

        news_articles = xml_data.findAll("item")

        for article in news_articles:
            article_title = article.find("title").text
            article_url = article.find("link").text
            article_published_date = article.findNext("pubDate").text

            news_article = {
                "title": article_title,
                "article_url": article_url,
                "article_published_date": article_published_date
            }
            news_articles_list.append(news_article)

        return news_articles_list
    except:
        raise FailureToConnect


# print(scrape_rss("https://www.wired.com/feed/tag/ai/latest/rss"))
