import sqlite3

from flask import Flask
from flask import g
import json
app = Flask(__name__)


def connect_db(db_name):
    return sqlite3.connect(db_name)


@app.before_request
def before_request():
    g.db = connect_db(app.config['DATABASE'])


# implement your views here
#public view
@app.route('/profile/<username>', methods = ['GET', 'POST'])
def profile_view(username):
    #SQL query of profile, user id, username, firstname, last name, birthdate
    #sql query of all tweets owned by user, tweet ID, text, date, uri
    #tweet count
    profile_info = _get_user_info(username)
    #encode into json and then dump
    profile_json = {}
    
    profile_json['user_id'] = profile_info[0][0]
    profile_json['first_name'] = profile_info[0][1]
    profile_json['last_name'] = profile_info[0][2]
    profile_json['birth_date'] = profile_info[0][3]
    
    profile_json['tweets'] = []
    profile_tweets = _get_user_tweets(profile_json['user_id'])
    # return str(profile_tweets)
    for column in profile_tweets:
        tweet_dict = {}
        tweet_dict['id'] = column[0]
        tweet_dict['text'] = column[1]
        tweet_dict['date'] = column[2]
        tweet_dict['uri'] = "/tweet/{}".format(tweet_dict['id'])
        profile_json['tweets'].append(tweet_dict)
        
    # return str(profile_json['tweets'])
    profile_json["tweet_count"] = len(profile_json['tweets']) #count number of tweet dictionaries to get # of tweets for user
    return json.dumps(profile_json)
    
@app.route('/login', methods = ['POST'])
def login_view():
    

    pass
    #recieve json file
    #load json file into dictionary, get username, get password
    #give access token

@app.route('/logout')
def logout_view():
    pass
    #give back access token
    #token will no longer work to prove user is logged in 
    
@app.errorhandler(404)
def not_found(e):
    return '', 404


@app.errorhandler(401)
def not_found(e):
    return '', 401

def _get_user_info(username):
    query = "SELECT id, first_name, last_name, birth_date FROM user WHERE username = ?"
    cursor = g.db.execute(query, (username,))
    results = cursor.fetchall()
    return results
    
def _get_user_tweets(user_id):
    query = "SELECT id, content, created FROM tweet WHERE user_id = ?"
    cursor = g.db.execute(query, (user_id,))
    results = cursor.fetchall()
    return results
# 
# DROP TABLE if exists user;
# CREATE TABLE user (
#   id INTEGER PRIMARY KEY autoincrement,
#   username TEXT NOT NULL,
#   password TEXT NOT NULL,
#   first_name TEXT,
#   last_name TEXT,
#   birth_date DATE,
#   CHECK (
#       length("birth_date") = 10
#   )
# );

# DROP TABLE if exists tweet;
# CREATE TABLE tweet (
#   id INTEGER PRIMARY KEY autoincrement,
#   user_id INTEGER,
#   created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#   content TEXT NOT NULL,
#   FOREIGN KEY(user_id) REFERENCES user(id),
#   CHECK(
#       typeof("content") = "text" AND
#       length("content") <= 140
#   )
# );
