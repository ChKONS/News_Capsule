import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template


class TechRss:
    pass


def silicon_rss(url):
    try:
        url = "https://www.siliconrepublic.com/rss-feeds/#"
        result = requests.get(url)
        return print("successful", result.status_code)
    except Exception as err:
        print("Failed. See error")
        print(err)


def techrepublic_rss(url):
    try:
        url = "https://techrepublic.com/"
        result = requests.get(url)
        return print("successful", result.status_code)
    except Exception as err:
        print("Failed. See error")
        print(err)


def theverge_rss(url):
    try:
        url = "https://theverge.com/"
        result = requests.get(url)
        return print("successful", result.status_code)
    except Exception as err:
        print("Failed. See error")
        print(err)


def user_options():
    options = ["Amazon", "Facebook", "Google", "Apple", "Android", "Netflix"]
    print(options)
    search_options = input("What would you like to search, please choose from the list? ")
    if not search_options.isalpha():
        raise ValueError("Sorry your search must match one of the options")

    result1 = f"https://www.siliconrepublic.com/search-results/?q={search_options}"
    result2 = f"https://www.techrepublic.com/search/?q={search_options}"
    result3 = f"https://www.theverge.com/search/?q={search_options}"
    return print(result1, result2, result3)


def rss():
    rss_list = []
    try:
        result = f"https://www.siliconrepublic.com/#"
        result2 = f"https://www.techrepublic.com/"
        result3 = f"https://www.theverge.com/"
        soup = BeautifulSoup(result.content, result2.content, result3.content, refeatures="xml")
        articles = soup.findAll("item")

        for a in articles:
            title = a.find('title').text
            link = a.find('link').text
            published = a.find('pubDate').text

            article = {
                "Title": "Title",
                "Link": "Link",
                "Published": "Published"
            }
            rss_list.append(article)
        return print(rss_list)
    except Exception as err:
        return print(err)


app = Flask(__name__)


@app.route("/guest_news.html")
@app.route("/home.html")
@app.route("/login.html")
@app.route("/news.html")
@app.route("/preferences.html")
@app.route("/profile.html")
@app.route("/register.html")
@app.route("/user_preferences.html")
def topic():
    return render_template("buttons.html")


rss()
print("Loading")
silicon_rss("https://www.siliconrepublic.com/rss-feeds/#")
user_options()
print("Complete")
