# My Youtube Coach

There are so many fitness videos on youtube, not all of them are good and it's sometimes hard to decide what to do. This app is meant to provide a curated list of fitness videos and lets users choose a video according to what they want to do (how much time they have, what body part they want to target..)
It gives the possibility to add videos, to view them and to get access to some statistics about the videos available on the site.
 
## UX

Typical users would be: 
- people who like to do fitness videos at home and who tend to just bookmark videos and then forget about them and always return to the same things because they don't know what to do. They want to be able save their workouts and find them easily the next times.
- people who want to get more variety. Some apps exist but they tend to be developped by one brand or one youtuber and therefore are not very varied. The user can here discover new workouts and adapt to their needs and time. 
- people who like to share their prefered workouts with their friends, because they can easily add videos and others will see what they add.  

The mockups can be found [here](https://github.com/mathilde206/youtube-coach/blob/master/Mockups%20Youtube%20Coach.pdf)

## Features
 
### Existing Features
- Possibility to add new videos
- Use the API from Youtube to fill the database (more information about the videos and information about the youtubers)
- Possibility to edit a video, to like it, and to delete it.
- Possibility to view information about a video and to play it on the video's page
- Possibility to filter videos according to criterias like targetted body part, or language
- Possibility to view all the videos added by a specific user
- Possibility to view all the videos corresponding to one specific youtuber (like a youtube channel)
- Possibility to explore some statistics about the videos on the site

### Features Left to Implement
- Have a message to the user when he's adding a video that's already on the site
#### Nice to have:
- Add authentication
- Make the chart more interactive by adding the possibility to go to the filtering criteria by clicking on the chart directly.

## Technologies Used

- [Flask](http://flask.pocoo.org/)
    - I use **Flask** to handle page routing and other backend functions
- [MongoDB](https://www.mongodb.com/fr) 
    - I use **MongoDB** for the database and db queries
- [Materialize](http://materializecss.com/)
    - I use **Materialize** to give the project a simple, responsive layout
- [Youtube/Google Developer API](https://developers.google.com/youtube/)
    - I use **Youtube**'s developer tools to get the data from Youtube.
- [JQuery Form Validation](https://jqueryvalidation.org/)
    - I use **JQuery Validation Plugin** to validate the form's data.

## Testing
- I'm expecting the Flask-Pymongo functions to be already tested..
- My own functions are tested in tests.py
- Documentation for the user testing can be found there : [User Tests](https://github.com/mathilde206/youtube-coach/blob/master/user_testing.pdf)


## Deployment
### Local: 
1. Firstly you will need to clone this repository by running the ```git clone https://github.com/mathilde206/youtube-coach``` command
2. Then you need to install all the dependencies from the requirements.txt file:
  ```
  pip install -r requirements.txt

  ```
4. Create a bashrc with the following variables: 
- DEVELOPER_KEY (from google for the youtube API)
- IP : 0.0.0.0
- PORT: 5000
- MONGO_DBNAME: fitness-vids-db
- MONGO_URI: your own mongo db uri.
3. To start the application : ```python3 app.py```

### Heroku
To deploy on heroku I simply connected heroku to the github repository. 
- DEVELOPER_KEY (from google for the youtube API)
- IP : 0.0.0.0
- PORT: 5000
- MONGO_DBNAME: fitness-vids-db
- MONGO_URI: the mongo uri that I added through Heroku.


## Credits

### Content
- Some of the content (video description) is copied from the video's description of youtube (for lack of imagination) 

### Media
- The photos used in the sites come from unsplash and are free of rights.
