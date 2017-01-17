import requests
from math import log
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import hashlib


app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.secret_key = 'iadfansdfnakjsdnfkansd'

limit = 10
naive_limit = 2
query_count = 0


class User(db.Model):
    id = db.Column(db.Integer, unique=True)
    hash_id = db.Column(db.String(80), unique=True, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    name = db.Column(db.String(120))
    avatar = db.Column(db.String(256))
    naive_score = db.Column(db.String(10))
    bonus = db.Column(db.String(10))
    final_score = db.Column(db.String(10))
    locale = db.Column(db.String(80))
    timezone = db.Column(db.String(80))
    gender = db.Column(db.String(80))
    currency = db.Column(db.String(80))

    def __init__(self, token, user_id=False, set_limit=False):
        info_query = "?fields=first_name,last_name,locale,timezone,gender,currency"
        if not user_id:
            info = fb(token, "me", info_query)
            self.id = info["id"]
            self.hash_id = md5(info["id"])
        else:
            self.id = user_id
            self.hash_id = md5(user_id)
            info = fb(token, str(user_id), info_query)
        try:
            self.name = info["first_name"] + " " + info["last_name"]
            self.first_name = info["first_name"]
            self.last_name = info["last_name"]
        except KeyError:
            print info
        self.locale = info["locale"]
        self.reaction_count = 0
        self.timezone = info["timezone"]
        self.gender = info["gender"]
        self.currency = info["currency"]["user_currency"]
        self.avatar = fb(token, "me", "picture?redirect=0")["data"]["url"]
        self.token = token
        if not set_limit:
            global limit
            self.limit = limit
        else:
            self.limit = set_limit
        self.reactions_weights = []
        self.naive_score = 0
        self.bonus = 0
        self.final_score = 0

    def get_scores(self):
        posts = self.get_posts()
        reactions = []
        for post in posts:
            reactions += self.get_reactions(post["id"])
            self.reaction_count += len(reactions)
            print("Base score updated to:" + str(self.reaction_count))
        self.get_bonus(reactions)
        n = self.reaction_count
        # The Base Score
        self.naive_score = log(n * 10 + 20, 10) - 0.3
        self.final_score = self.naive_score + self.bonus
        print("The user's final score:" + str(self.final_score))
        return self.naive_score, self.bonus, self.final_score

    def get_posts(self):
        posts = fb(self.token, "me", "posts?limit=" + str(self.limit))
        return posts["data"]

    def get_reactions(self, post_id):
        return fb(self.token, post_id, "reactions")["data"]

    def get_bonus(self, reactions):
        if reactions:
            for reaction in reactions:
                friend_score = get_naive_score(self.token, reaction["id"])
                self.reactions_weights.append(friend_score / 5)
            self.bonus = log(sum(self.reactions_weights) + 1, 10) * 0.5
            return self.bonus
        else:
            return 0


def get_naive_score(token, user_id):
    friend = fb(token, user_id, "friends")
    try:
        n = friend["summary"]["total_count"]
    except KeyError:  # Does not have permission to read
        n = 0
    score = log(n * 20 + 20, 10)
    return score


def fb(token, first, second=""):
    global query_count
    if "?" in second:
        suffix = "&access_token="
    else:
        suffix = "?access_token="
    query = "https://graph.facebook.com/v2.8/" + first + "/" + second + suffix + token
    response = requests.get(query)
    query_count += 1
    return response.json()


def md5(user_id):
    return hashlib.md5(str(user_id)).hexdigest()