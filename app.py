import os
import json
import math
from urllib.parse import urlparse, parse_qs
from flask import Flask, render_template, url_for, request, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from get_video_info import youtube_search, get_video_id_from_url
from googleapiclient.errors import HttpError

import config

app = Flask(__name__)
app.config['MONGO_DBNAME'] = config.MONGO_DBNAME
app.config['MONGO_URI'] = config.MONGO_URI

mongo = PyMongo(app)


def get_mongo_search_query(value, search_query):
    if len(search_query) == 1:
        return {value: search_query[0]}
    else:
        arr = []
        for item in search_query:
            arr.append({value:item})
        return {'$or': arr}

def append_to_query(value, query_arr):
    if request.form.get(value):
            category_name_query = get_mongo_search_query(value, request.form.getlist(value))
            return query_arr.append(category_name_query)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_videos/<category>/<page_number>", methods=["GET", "POST"])
def get_videos(category, page_number):
    """
    This function will show the videos with and without filtering, by creating a query_filter string that will be used to retrieve the right videos.
    If there is no POST request, the filter is simply the category or empty if no category.
    """
    query_arr = []
    query_filter=''

    if request.method == "POST":
        append_to_query('category_name', query_arr)
        append_to_query('body_part_name', query_arr)
        append_to_query('language_name', query_arr)

        if len(query_arr) == 0:
            query_filter = ""
        else:
            query_filter = {'$and':query_arr}

    if query_filter == '':
        if category != "all":
            query_filter = {'category_name':category}

    #Create a dict to identify in the template what was selected
    selected = {
        'category_name': request.form.getlist("category_name") or [],
        'body_part_name': request.form.getlist("body_part_name") or [],
        'language_name': request.form.getlist("language_name") or [],
    }

    #Retrieve the filtered videos (or all) and the right amount of videos for pagination
    skips = 9*(int(page_number)-1)

    if category == "all" and query_filter == "":
        videos=mongo.db.videos.find().skip(skips).limit(9)
        number_of_pages= math.ceil(mongo.db.videos.count()/9)
    else:
        videos=mongo.db.videos.find(query_filter).skip(skips).limit(9)
        number_of_pages= math.ceil(mongo.db.videos.count(query_filter)/9)

    return render_template("get_videos.html",
                            videos=videos,
                            category=category,
                            categories= mongo.db.categories.find(),
                            targetted_body_parts=mongo.db.targetted_body_parts.find(),
                            languages=mongo.db.languages.find(),
                            number_of_pages=number_of_pages,
                            page_number=page_number,
                            selected=selected)

@app.route("/add_video")
def add_video():
    return render_template('add_video.html',
                            categories=mongo.db.categories.find(),
                            languages=mongo.db.languages.find(),
                            targetted_body_parts=mongo.db.targetted_body_parts.find())


@app.route("/insert_video", methods=["POST"])
def insert_video():
    video_id = get_video_id_from_url(request.form.get('video_url'))

    try:
        youtube_data = youtube_search(video_id)[0]
        new_video = {
            "_id":video_id,
            "video_url" : request.form.get("video_url"),
            "video_description": request.form.get("video_description"),
            "category_name": request.form.get("category_name"),
            "language_name":request.form.get("language_name"),
            "body_part_name":request.form.getlist('body_part_name'),
            "contributor_username":request.form.get("contributor_username"),

            "video_title" : youtube_data['video_title'],
            "youtuber":youtube_data['youtuber'],
            "published_at":youtube_data["published_at"],
            "YT_popularity":youtube_data["YT_popularity"],
            "duration":youtube_data["duration"],
            "thumbnails":youtube_data["thumbnails"]
        }
        try:
            mongo.db.videos.insert(new_video)
        except:
           print("There was a problem with mongoDB")

    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))

    return redirect(url_for('get_videos', category="all", page_number=1))
    

@app.route('/get_detail/<video_id>')
def get_detail(video_id):
    return render_template("get_detail.html", video=mongo.db.videos.find_one({"_id": video_id}))

@app.route("/like_video/<video_id>", methods=["POST"])
def like_video(video_id):
    mongo.db.videos.update({"_id": video_id}, {"$inc":{"number_of_likes":1}})
    return redirect(url_for('get_detail', video_id=video_id))

@app.route("/delete_video/<video_id>", methods=["POST"])
def delete_video(video_id):
    mongo.db.videos.remove({"_id": video_id})
    return redirect(url_for('get_videos', category="all", page_number=1))

@app.route("/edit_video/<video_id>")
def edit_video(video_id):
    return render_template("edit_video.html",
                            video=mongo.db.videos.find_one({"_id": video_id}),
                            categories=mongo.db.categories.find(),
                            languages=mongo.db.languages.find(),
                            targetted_body_parts=mongo.db.targetted_body_parts.find())


@app.route("/update_video/<video_id>", methods=["POST"])
def update_video(video_id):
    id_input = get_video_id_from_url(request.form.get('video_url'))

    if mongo.db.videos.find_one({"_id": id_input}):
        mongo.db.videos.update({"_id": id_input}, { "$set" :{
            "video_url" : request.form.get("video_url"),
            "video_description": request.form.get("video_description"),
            "category_name": request.form.get("category_name"),
            "language_name":request.form.get("language_name"),
            "body_part_name":request.form.getlist('body_part_name'),
            "contributor_username":request.form.get("contributor_username")
        }})

    else:
        mongo.db.videos.remove({"_id": video_id})
        try:
            youtube_data = youtube_search(id_input)[0]
            new_video = {
                "_id":id_input,
                "video_url" : request.form.get("video_url"),
                "video_description": request.form.get("video_description"),
                "category_name": request.form.get("category_name"),
                "language_name":request.form.get("language_name"),
                "body_part_name":request.form.getlist('body_part_name'),
                "contributor_username":request.form.get("contributor_username"),

                "video_title" : youtube_data['video_title'],
                "youtuber":youtube_data['youtuber'],
                "published_at":youtube_data["published_at"],
                "YT_popularity":youtube_data["YT_popularity"],
                "duration":youtube_data["duration"],
                "thumbnails":youtube_data["thumbnails"]
            }

            try:
                mongo.db.videos.insert(new_video)
            except:
               print("There was a problem with mongoDB")

        except HttpError as e:
            print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))

    return redirect(url_for('get_videos', category="all", page_number=1))


if __name__ == "__main__":
    app.run(host= os.environ.get("IP"), 
            port = int(os.environ.get("PORT")),
            debug = True)