from flask import Flask, request, jsonify
import json
from pymongo import MongoClient
from bson import ObjectId
import datetime
app = Flask(__name__)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

client = MongoClient('localhost', 27017)

blog_db = client['blog-db']


@app.route("/users", methods = ["GET", "POST"])
def users():
    if request.method == 'GET':
        users_coll = blog_db['users']
        return JSONEncoder().encode(list(users_coll.find()))
    else:
        user = {
            "name": request.get_json()['name'],
            "username": request.get_json()['username'],
            "password": request.get_json()['password'],
            "created": str(datetime.datetime.now())
        }
        users_coll = blog_db['users']
        users_coll.insert_one(user)
        return "Done."

@app.route("/users/<username>", methods = ["GET", "DELETE"])
def user_username(username):
    if request.method == 'GET':
        users_coll = blog_db['users']
        return JSONEncoder().encode(list(users_coll.find()))
    else:
        users_coll = blog_db['users']
        users_coll.delete_one({"username": username})
        return "Done."

@app.route("/posts", methods = ["GET", "POST"])
def posts():
    if request.method == 'GET':
        posts_coll = blog_db['posts']
        return JSONEncoder().encode(list(posts_coll.find()))
    else:
        post = {
            "title": request.get_json()['title'],
            "body": request.get_json()['body'],
            "userID": request.get_json()['userID'],
            "created": str(datetime.datetime.now())
        }
        posts_coll = blog_db['posts']
        posts_coll.insert_one(post)
        return "Done."

@app.route("/posts/<postid>", methods = ["GET", "DELETE"])
def posts_postid(postid):
    if request.method == 'GET':
        posts_coll = blog_db['posts']
        print(list(posts_coll.find()))
        return JSONEncoder().encode(list(posts_coll.find()))
    else:
        posts_coll = blog_db['posts']
        posts_coll.delete_one({"postid": postid})
        return "Done."

@app.route("/posts/<postid>/comments", methods = ["POST"])
def comment_create():
    comment = {
        "comment": request.get_json()['comment'],
        "userID": request.get_json()['userID']
    }
    posts_coll = blog_db['posts']
    posts_coll.insert_one(comment)
    return "Done."
