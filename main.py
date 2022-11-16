from flask import Flask, request, render_template, redirect, url_for, session
from news_capsule.scraper.rss_scraper import scrape_rss
from news_capsule.db_connector.db_connect import DBPreferences, UserNotFound, DBUsers, store_news_articles, DbConnectionError
from news_capsule.config import *
from functools import wraps
# Including modules from Christelle's code
from flask_bcrypt import Bcrypt
import os

template_dir = os.path.abspath('front_end/templates')
static_dir = os.path.abspath('front_end/static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Integration with Christelle's code
bcrypt = Bcrypt(app)
app.secret_key = os.getenv('SECRET_KEY')


# End of first portion of Christelle's code

# Creating function to use as decorator to prevent unauthorized access to user profiles

def unauthorized_access(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if session.get('username') is None or session.get('login_success') is None or session.get(
                'user_id') != int(kwargs["user_id"]):
            return redirect(url_for("home_page"))
        return function(*args, **kwargs)

    return decorated_function


@app.route('/', methods=['GET', 'POST'])
def home_page():
    return render_guest_or_user()


def render_guest_or_user():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Continue as guest':
            return redirect(url_for("render_preferences_page"))
        elif request.form['submit_button'] == "Log in for a personalized experience":
            return redirect(url_for("login_or_register"))  # linked to login code from Christelle
        else:
            pass
    return render_template("home.html")


@app.route('/news-preferences', methods=['GET', 'POST'])
def render_preferences_page():
    if request.method == 'POST':
        if request.form['submit_button'] == '>':
            return redirect(url_for("render_selected_news"))
    return render_template("preferences.html")


@app.route('/<user_id>/news-preferences', methods=['GET', 'POST'])
@unauthorized_access
def customize_user_preferences(user_id):
    if request.method == 'POST':
        if request.form['submit_button'] == '>':
            selected_topics = request.form.getlist("topic")
            db_preferences = DBPreferences()
            db_preferences.update_preferences(user_id, selected_topics)
            return redirect(url_for("render_user_preferred_news", user_id=user_id))
    return render_template("user_preferences.html", user_id=user_id)


@app.route('/news-feed', methods=['GET', 'POST'])
def render_selected_news():
    selected_topics = request.form.getlist("topic")
    news_mix = [item for sublist in list(map(scrape_rss, urls)) for item in sublist]
    selection_articles = [item for item in news_mix for topic in selected_topics if topic in item["article_url"]]
    store_news_articles(news_mix)
    return render_template("guest_news.html", value=selection_articles)


@app.route('/<user_id>/news-feed')
@unauthorized_access
def render_user_preferred_news(user_id):
    db_preferences = DBPreferences()
    try:
        preferences = db_preferences.retrieve_preferences(user_id)
    except UserNotFound:
        return redirect(url_for("customize_user_preferences", user_id=user_id))
    preferred_topics = [item for item in preferences if preferences[item]]
    news_mix = [item for sublist in list(map(scrape_rss, urls)) for item in sublist]
    selection_articles = [item for item in news_mix for topic in preferred_topics if topic in item["article_url"]]
    store_news_articles(news_mix)
    return render_template("news.html", value=selection_articles, user_id=user_id)


"""
Integration with Christelle's code (below is her code; commented lines are additions or updates)
"""


@app.route('/sign-in', methods=['GET', 'POST'])
def login_or_register():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            db_users = DBUsers()
            info = db_users.get_user(username)
            user_id = info["person_id"]
            if info is not None:
                if bcrypt.check_password_hash(info['user_password'],
                                              password):  # updating with Christelle's most recent code
                    session['login_success'] = True
                    session['username'] = username
                    session['user_id'] = user_id  # included to use with login_required decorator
                    return redirect(url_for('profile', user_id=user_id))  # passing user_id to profile to obtain
                    # session's user id and return news preferences in other pages
            else:
                return redirect(url_for('login_or_register'))
    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])  # check if data is filled in
def new_user():
    if request.method == "POST":
        if "one" in request.form and "two" in request.form and "three" in request.form:
            email = request.form["one"]
            username = request.form["two"]
            password = request.form["three"]
            password_hashed = bcrypt.generate_password_hash(password)  # line from Christelle's most recent code
            db_users = DBUsers()
            db_users.create_user(email, username, password_hashed)
            return redirect(url_for('login_or_register'))
    return render_template("register.html")


@app.route('/<user_id>/profile')
@unauthorized_access
def profile(user_id):
    if session['login_success']:
        return render_template("profile.html", user_id=user_id, username=session['username'])


@app.route('/logout')
def logout():
    session.pop('login_success', None)
    return redirect(url_for('home_page'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
