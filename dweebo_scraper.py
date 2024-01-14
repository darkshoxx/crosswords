# External imports
from datetime import datetime
from googleapiclient.discovery import build
import json
# Local Imorts
from secrety_secrets import API_KEY, CHANNEL_ID

# Be sure to put your API key in secrety_secrets.py, see README.MD
api_key = API_KEY


# Get a list of all videos on the channel
def get_channel_videos(channel_id):
    videos = []
    next_page_token = None

    youtube = build('youtube', 'v3', developerKey=api_key)
    while True:
        request = youtube.channels().list(
            part='contentDetails',
            id=channel_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        response_details = response['items'][0]['contentDetails']
        playlist_id = response_details['relatedPlaylists']['uploads']

        playlist_request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        playlist_response = playlist_request.execute()

        videos.extend(playlist_response['items'])

        next_page_token = playlist_response.get('nextPageToken')

        if not next_page_token:
            break

    return videos


def filter_videos(videos):
    filtered_videos = {}
    for video in videos:
        title = video['snippet']['title']
        video_id = video['snippet']['resourceId']['videoId']
        published_at_str = video['snippet']['publishedAt']

        if 'cryptic' in title.lower() and 'mephisto' not in title.lower():
            # Extract the date from the publishedAt string
            published_date = datetime.strptime(
                published_at_str, "%Y-%m-%dT%H:%M:%S%z"
            ).date().strftime('%Y-%m-%d')

            # Use the date as the key for the dictionary
            filtered_videos[published_date] = (
                f'https://www.youtube.com/watch?v={video_id}'
            )

    return filtered_videos


# Main script
if __name__ == "__main__":
    channel_id = CHANNEL_ID  # Replace with the actual channel ID
    videos = get_channel_videos(channel_id)
    filtered_videos = filter_videos(videos)

    # Save the dictionary with puzzle numbers and video URLs as JSON
    json_filename = 'puzzle_videos_dict.json'
    with open(json_filename, 'w') as json_file:
        json.dump(filtered_videos, json_file, indent=2)
