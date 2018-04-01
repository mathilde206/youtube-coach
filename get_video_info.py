import isodate
from datetime import datetime, timedelta
from humanize import intcomma
import re

from googleapiclient.discovery import build
from urllib.parse import parse_qs, urlparse
from googleapiclient.errors import HttpError


DEVELOPER_KEY = 'AIzaSyA-HP_X6A6Gp15rbv4VGSnJJSg_9UdUPG0'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(vid_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)
    
    video_response = youtube.videos().list(
        id=vid_id,
        part='contentDetails,snippet,statistics'
    ).execute()
    
    result = {
        'id':vid_id,
        'duration':{
            'seconds': isodate.parse_duration(video_response['items'][0]['contentDetails']['duration']).total_seconds(),
            'human_readable': str(timedelta(seconds = isodate.parse_duration(video_response['items'][0]['contentDetails']['duration']).total_seconds()))
            },
        'published_at':isodate.parse_date(video_response['items'][0]['snippet']['publishedAt']).isoformat(),
        'video_title': video_response['items'][0]['snippet']['title'],
        'youtuber': video_response['items'][0]['snippet']['channelTitle'],
        'thumbnails': { 
            'small': video_response['items'][0]['snippet']['thumbnails']['default']['url'],
            'large': video_response['items'][0]['snippet']['thumbnails']['high']['url']
            },
        'YT_popularity': {
            'like_count': video_response['items'][0]['statistics']['likeCount'],
            'view_count':intcomma(video_response['items'][0]['statistics']['viewCount'])
            }
        }, 
    
    return result;

def get_video_id_from_url(url):
    parsed_url = urlparse(url)
    if not parsed_url.query:
        if 'embed/' in parsed_url.path:
            video_id = parsed_url.path[7:]
        else:
            video_id = parsed_url.path[1:]
    else:
        video_id = parse_qs(parsed_url.query)['v'][0]
    
    return video_id

if __name__ == '__main__':

  try:
    result = youtube_search('pyFNz8zJSdw')
    print(result)
  except HttpError as e:
    print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
