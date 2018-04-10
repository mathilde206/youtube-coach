import os
import json
import math
from urllib.parse import urlparse, parse_qs
from flask import Flask, render_template, url_for, request, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from get_video_info import youtube_search, get_video_id_from_url, get_channel_info
from googleapiclient.errors import HttpError


app = Flask(__name__)
app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)


#Functions that build the query from the form for the filtering functionality
def get_mongo_search_query(value, search_query):
    """
    This function takes the search criteria selected by the user and creates the appropriate query string for mongodb
    """
    if len(search_query) == 1:
        return {value: search_query[0]}
    else:
        arr = []
        for item in search_query:
            arr.append({value:item})
        return {'$or': arr}

def append_to_query(value, query_arr):
    """
    This function appends to a query string the values selected by the user to filter the search
    """
    if request.form.get(value):
            category_name_query = get_mongo_search_query(value, request.form.getlist(value))
            return query_arr.append(category_name_query)


#Functions that build the query from the form for the filtering functionality
def numb_of_videos(filter_name):
    """
    Gets the number of videos, aggregated by filter_name (category, body_part,..)
    """
    return mongo.db.videos.aggregate([
                            {
                                "$unwind": "$"+filter_name
                            },
                            {"$group": {
                                "_id": "$" + filter_name, 
                                "number_of_videos": {"$sum": 1}
                            }}, 
                            {"$sort":
                                {"number_of_videos":1}
                                
                            },
                            ])
    
def numb_of_likes(filter_name):
    """
    Gets the number of videos, aggregated by filter_name (category, body_part,..)
    """
    return mongo.db.videos.aggregate([
                            {
                                "$unwind": "$"+filter_name
                            },
                            {
                                "$group": {
                                    "_id": "$" + filter_name, 
                                    "number_of_likes": {"$sum": "$number_of_likes"}
                                    }
                            }, 
                            {
                                "$sort":{"number_of_likes":1}
                            }
                            ]) 

def get_youtube_views(filter_name):
    """
    Gets the number of videos, aggregated by filter_name (category, body_part,..)
    """
    return mongo.db.videos.aggregate([
                            {
                                "$unwind": "$"+filter_name
                            },
                            {
                                "$group": {
                                    "_id": "$" + filter_name, 
                                    "number_of_views": {"$sum": "$YT_popularity.view_count"}
                                    }
                            }, 
                            {
                                "$sort":{"number_of_views":1}
                            }
                            ]) 
                            
def get_duration(filter_name):
    """
    Gets the number of videos, aggregated by filter_name (category, body_part,..)
    """
    return mongo.db.videos.aggregate([
                            {
                                "$group": {
                                    "_id": "$" + filter_name, 
                                    "duration": {"$sum": "$duration.seconds"}
                                    }
                            }, 
                            {
                                "$sort":{"duration":1}
                            }
                            ]) 

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

# TODO:must be a better way to solve the macro problem than add twice...
    return render_template("get_videos.html",
                            videos=videos,
                            category=category,
                            categories= mongo.db.categories.find(),
                            categories2=mongo.db.categories.find(),
                            targetted_body_parts=mongo.db.targetted_body_parts.find(),
                            targetted_body_parts2=mongo.db.targetted_body_parts.find(),
                            languages=mongo.db.languages.find(),
                            languages2=mongo.db.languages.find(),
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
    # First we add the video if it doesn't exist yet 
    # TODO: Add some message to the user if video already exist (ex: they can update it?)
    video_id = get_video_id_from_url(request.form.get('video_url'))
    if not mongo.db.videos.find_one({'_id': video_id}): 
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

    # Next we try to add the youtuber if he doesn't exist yet
    new_video = mongo.db.videos.find_one({"_id":video_id})
    if not mongo.db.youtubers.find_one({'_id': new_video['youtuber']['channel_Id']}):
        try:
            new_youtuber = get_channel_info(new_video['youtuber']['channel_Id'])
            mongo.db.youtubers.insert(new_youtuber)
            
        except HttpError as e:
            print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))

    return redirect(url_for('get_videos', category="all", page_number=1))
    
@app.route('/get_detail/<video_id>')
def get_detail(video_id):
    return render_template("get_detail.html", video=mongo.db.videos.find_one({"_id": video_id}))
    
@app.route('/get_youtuber_detail/<channel_id>')
def get_youtuber_detail(channel_id):
    youtuber_videos = mongo.db.videos.find({"youtuber.channel_Id": channel_id})
    
    return render_template("get_youtuber_detail.html", 
                            youtuber=mongo.db.youtubers.find_one({"_id": channel_id}),
                            youtuber_videos=youtuber_videos,
                            total_videos=youtuber_videos.count())

@app.route('/get_contributor_detail/<contributor_username>')
def get_contributor_detail(contributor_username):
    contributor_videos = mongo.db.videos.find({"contributor_username": contributor_username})
    
    return render_template("get_contributor_detail.html",
                            contributor_username=contributor_username,
                            contributor_videos=contributor_videos,
                            total_videos=contributor_videos.count())
    

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


@app.route("/get_stats")
def get_stats():
    # The first 3 variables get top 3 data 
    top_contributors = mongo.db.videos.aggregate([
                            {"$group": {"_id": "$contributor_username", "number_of_videos": {"$sum": 1}}}, 
                            {"$sort":{"number_of_videos":-1}},
                            {"$limit": 3}
                            ])
                            
    top_liked_videos = mongo.db.videos.find().sort( "number_of_likes", -1).limit(3)
    
    top_youtubers = mongo.db.videos.aggregate([
                            {"$group": {"_id": "$youtuber.title", "number_of_videos": {"$sum": 1}}}, 
                            {"$sort":{"number_of_videos":-1}},
                            {"$limit": 3},
                            {"$lookup":
                                {
                                    "from": "youtubers",
                                    "localField": "youtuber[channel_Id]",
                                    "foreignField": "videos.channel_id",
                                    "as": "youtuber_info"
                                }
                            },
                            {
                                "$unwind": { "path": "$youtuber_info" }
                            },
                            {
                                "$project" : { 
                                    "_id" : 1, 
                                    "number_of_videos": 1,
                                    "youtuber_info": 1,
                                    "areIdsSame": {"$eq" : [ "$_id", "$youtuber_info.channel_title" ]}
                                }
                            },
                            { "$match" : { "areIdsSame" : True } } 
                            ])
                            

    # Gather the data for the graphs
    videos_by_category = numb_of_videos('category_name')
    videos_by_body_part = numb_of_videos('body_part_name')
    videos_by_language = numb_of_videos('language_name')
    
    likes_by_category = numb_of_likes('category_name')
    likes_by_body_part = numb_of_likes('body_part_name')
    likes_by_language = numb_of_likes('language_name')
    
    youtube_views_by_category = get_youtube_views('category_name')
    youtube_views_by_body_part = get_youtube_views('body_part_name')
    youtube_views_by_language = get_youtube_views('language_name')
    
    duration_by_category = get_duration('category_name')
    duration_by_body_part = get_duration('body_part_name')
    duration_by_language= get_duration('language_name')
                            
    def get_json_for_d3(data):
        arr = []
        for document in data:
            arr.append(document)
        return arr
        
    return render_template('get_stats.html', 
                            top_contributors = top_contributors,
                            top_liked_videos=top_liked_videos,
                            top_youtubers=top_youtubers,
                            videos_by_category=get_json_for_d3(videos_by_category),
                            videos_by_body_part=get_json_for_d3(videos_by_body_part),
                            videos_by_language=get_json_for_d3(videos_by_language),
                            likes_by_category=get_json_for_d3(likes_by_category),
                            likes_by_body_part=get_json_for_d3(likes_by_body_part),
                            likes_by_language = get_json_for_d3(likes_by_language),
                            youtube_views_by_category =get_json_for_d3(youtube_views_by_category),
                            youtube_views_by_body_part = get_json_for_d3(youtube_views_by_body_part),
                            youtube_views_by_language = get_json_for_d3(youtube_views_by_language),
                            duration_by_category = get_json_for_d3(duration_by_category),
                            duration_by_body_part = get_json_for_d3(duration_by_body_part),
                            duration_by_language=get_json_for_d3(duration_by_language))

@app.route('/about')
def about():
    return render_template('about.html')
 
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    


if __name__ == "__main__":
    app.run(host= os.environ.get("IP"), 
            port = int(os.environ.get("PORT")))