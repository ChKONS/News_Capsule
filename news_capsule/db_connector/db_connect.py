import os
import mysql.connector
from mysql.connector import IntegrityError

DB_NAME = "news_capsule"
NEWS_TOPICS = dict.fromkeys(['cryptonews.com', 'teslarati.com', 'wired.com', 'siliconrepublic.com', 'tomshardware.com'],
                            0)

class DbConnectionError(Exception):
    pass


class UserNotFound(Exception):
    pass


def _connect_to_db():
    cnx = mysql.connector.connect(
        host=os.getenv('DATABASE_HOST'),
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
        auth_plugin='mysql_native_password',
        database=os.getenv('DATABASE_DB')
    )
    return cnx


class DBClient:
    def __init__(self):
        self.cnx = _connect_to_db()


class DBUsers(DBClient):
    login_info_columns = ["person_id", "username", "email", "user_password"]

    def get_user(self, username):
        cur = self.cnx.cursor()
        with cur as cursor:
            cursor.execute(
                f"SELECT * FROM login_info WHERE username='{username}'")  # updating with Christelle's most recent code
            match = cursor.fetchone()
            return dict(zip(self.login_info_columns, match))

    def create_user(self, email, username, password_hashed):
        cur = self.cnx.cursor()
        with cur as cursor:
            cursor.execute("INSERT INTO login_info(email, username, user_password)VALUES(%s, %s, %s)",
                           (email, username, password_hashed))  # line from Christelle's most recent code
            self.cnx.commit()


class DBPreferences(DBClient):

    @staticmethod
    def _select_query(cursor, statement, user_id):
        cursor.execute(statement, [user_id])
        matches = [match for match in cursor]
        return matches

    @staticmethod
    def _insert_query(cursor, preferences, statement, user_id):
        user_preferences = {k: (1 if k in preferences else v) for k, v in NEWS_TOPICS.items()}
        sql_data = [user_id] + list(user_preferences.values())
        cursor.execute(statement, sql_data)

    def create_preferences(self, user_id, preferences):
        cur = self.cnx.cursor()
        with cur as cursor:
            self._insert_query(cursor, preferences, "INSERT INTO user_preferences (user_id, crypto, tesla, `ml/ai`, "
                                                    "`faang/general_tech`, hardware) VALUES (%s, %s, %s, %s, %s, %s) ", user_id)
        self.cnx.commit()

    def update_preferences(self, user_id, preferences):
        if self._check_if_user_set_preferences(user_id):
            cur = self.cnx.cursor()
            with cur as cursor:
                self._insert_query(cursor, preferences, "REPLACE INTO user_preferences VALUES (%s, %s, %s, %s, %s, %s)",
                                   user_id)
            self.cnx.commit()
        else:
            self.create_preferences(user_id, preferences)

    def _check_if_user_set_preferences(self, user_id) -> bool:
        cur = self.cnx.cursor()
        with cur as cursor:
            matches = self._select_query(cursor, "SELECT user_id FROM user_preferences WHERE user_id = %s", user_id)
            return False if not matches else True

    def retrieve_preferences(self, user_id):
        cur = self.cnx.cursor()
        if not self._check_if_user_set_preferences(user_id):
            raise UserNotFound
        with cur as cursor:
            matches = self._select_query(cursor, "SELECT crypto, tesla, `ml/ai`, `faang/general_tech`, hardware FROM "
                                                 "user_preferences WHERE "
                                                 "user_id = %s", user_id)
            stored_user_preferences = {k: v for k, v in zip(list(NEWS_TOPICS.keys()), [i for j in matches for i in j])}
            return stored_user_preferences


def store_news_articles(news_articles_list):
    db_name = DB_NAME
    db_connection = _connect_to_db()
    try:
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)
        with cur as cursor:
            for news_piece in news_articles_list:
                try:
                    title = news_piece["title"]
                    article_url = news_piece["article_url"]
                    article_published_date = news_piece["article_published_date"]
                    sql_statement = "INSERT INTO news_articles (News_Title, News_URL, News_Date) VALUES (%s, %s, %s)"
                    sql_data = (title, article_url, article_published_date)
                    cursor.execute(sql_statement, sql_data)
                except IntegrityError:
                    db_connection.rollback()
                    continue
        db_connection.commit()
    except DbConnectionError:
        raise
    finally:
        db_connection.close()