import os
import json
from urllib.parse import urlparse, parse_qs
from flask import Flask, render_template, url_for, request, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from get_video_info import youtube_search, get_video_id_from_url
from googleapiclient.errors import HttpError

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'fitness-vids-db'
app.config['MONGO_URI'] = os.getenv('MONGO_URI')

mongo = PyMongo(app)

@app.route("/get_videos")
def get_videos():
    return render_template("get_videos.html", videos=mongo.db.videos.find())

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
        
    return redirect('get_videos')
    

@app.route('/get_detail/<video_id>')
def get_detail(video_id):
    return render_template("get_detail.html", video=mongo.db.videos.find_one({"_id": video_id}))




if __name__ == "__main__":
    app.run(host= os.environ.get("IP"), 
            port = int(os.environ.get("PORT")),
            debug = True)