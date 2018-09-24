import isodate
from datetime import datetime, timedelta
from humanize import intcomma
import re

from googleapiclient.discovery import build
from urllib.parse import parse_qs, urlparse
from googleapiclient.errors import HttpError

DEVELOPER_KEY = os.environ.get('DEVELOPER_KEY')
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)


def youtube_search(vid_id):
    video_response = youtube.videos().list(
        id=vid_id,
        part='contentDetails,snippet,statistics'
    ).execute()

    result = {
        'id': vid_id,
        'duration': {
            'seconds': isodate.parse_duration(
                video_response['items'][0]['contentDetails']['duration']).total_seconds(),
            'human_readable': str(timedelta(seconds=isodate.parse_duration(
                video_response['items'][0]['contentDetails']['duration']).total_seconds()))
        },
        'published_at': isodate.parse_date(
            video_response['items'][0]['snippet']['publishedAt']).isoformat(),
        'video_title': video_response['items'][0]['snippet']['title'],
        'youtuber': {
            'title': video_response['items'][0]['snippet']['channelTitle'],
            'channel_Id': video_response['items'][0]['snippet']['channelId']
        },
        'thumbnails': {
            'small': video_response['items'][0]['snippet']['thumbnails']['default']['url'],
            'large': video_response['items'][0]['snippet']['thumbnails']['high']['url']
        },
        'YT_popularity': {
            'like_count': int(float(video_response['items'][0]['statistics']['likeCount'])),
            'view_count': int(float(video_response['items'][0]['statistics']['viewCount'])),
            'view_count_human_readable': intcomma(
                video_response['items'][0]['statistics']['viewCount'])
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


def get_channel_info(channel_Id):
    channel_response = youtube.channels().list(
        id=channel_Id,
        part='contentDetails,snippet,statistics'
    ).execute()

    result = {
        '_id': channel_response['items'][0]['id'],
        'channel_title': channel_response['items'][0]['snippet']['title'],
        'channel_description': channel_response['items'][0]['snippet']['description'],
        'channel_url': 'https://www.youtube.com/channel/' + channel_response['items'][0]['id'],
        'thumbnails': channel_response['items'][0]['snippet']['thumbnails']['default']['url'],
        'stats': {
            'view_count': channel_response['items'][0]['statistics']['viewCount'],
            'video_count': channel_response['items'][0]['statistics']['videoCount']
        }

    }
    return result


if __name__ == '__main__':

    try:
        result = get_channel_info('UCIJwWYOfsCfz6PjxbONYXSg')
        print(result)
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
