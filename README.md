# The Youtube Coach
 
## Overview

### What is this app for?

This app is meant to be a personal Youtube Coach, to get access to a curated list of fitness videos.  

### What does it do?
It gives the possibility to add videos, to view them and to get access to some statistics about the videos available on the site.


### How does it work
It's using the youtube API to gather additional information when a user enters a new video and to play it directly on the site.

## Features

### Existing Features

-General Features
  - Possibility to add new videos 
  - Use the API from Youtube to fill the database (more information about the videos and information about the youtubers)
  - Possibility to edit a video, to like it, and to delete it.
  - Possibility to view information about a video and to play it on the video's page
  - Possibility to filter videos according to criterias like targetted body part, or language
  - Possibility to view all the videos added by a specific user
  - Possibility to view all the videos corresponding to one specific youtuber (like a youtube channel)
  - Possibility to explore some statistics about the videos on the site

### Features to Implement
  - Have a message to the user when he's adding a video that's already on the site
  - Nice to have:
    - Add authentication
    - Make the chart more interactive by adding the possibility to go to the filtering criteria by clicking on the chart directly.
 
## Tech Used
### Some the tech used includes:
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

## Contributing
### Getting the code up and running
1. Firstly you will need to clone this repository by running the ```git clone https://github.com/mathilde206/youtube-coach``` command
2. Then you need to install all the dependencies from the requirements.txt file:
  ```
  pip install -r requirements.txt

  ```
3. To start the application : ```python3 app.py```
4. Make changes to the code and if you think it belongs in here then just submit a pull request

### Add more videos 
Feel free to add more fitness related videos.