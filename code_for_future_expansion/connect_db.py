import mysql.connector
from config import USER, PASSWORD, HOST
from scraper import rss
from Project.News_Capsule.main import tech_api


def connect_db(db):
    con = mysql.connector.connect(
        user=USER,
        host=HOST,
        password=PASSWORD,
        authorize="mysql_password",
        data=db
    )
    return con


def api_news(connect):
    db = "project"
    connect = connect_db(db)
    cursor = connect.cursor
    print(f"Connected to {db} successfully")

def connect_scraper(connect)
    db = "project"
    connect = connect_db(db)
    cursor = connect.cursor
    print(f"Connected to {db} successfully")

if __name__ == "__main__":
     api_news(tech_api("https://newsapi.org/"))

if __name__ == "__scraper__":
    connect_scraper(rss())

