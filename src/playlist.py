from src.channel import Channel
import datetime
import isodate


class PlayList:

    def __init__(self, playlist_id):
        youtube_obj = Channel.get_service()

        playlists = youtube_obj.playlists().list(id=playlist_id,
                                                 part='contentDetails,snippet',
                                                 maxResults=50,
                                                 ).execute()

        playlist_videos = youtube_obj.playlistItems().list(playlistId=playlist_id,
                                                           part='contentDetails',
                                                           maxResults=50,
                                                           ).execute()

        video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        self.video_response = youtube_obj.videos().list(part='contentDetails,statistics',
                                                        id=','.join(video_ids)
                                                        ).execute()['items']

        self.title = playlists['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={playlist_id}"

    @property
    def total_duration(self):
        videos = [item['contentDetails']['duration'] for item in self.video_response]
        time = sum([isodate.parse_duration(i).seconds for i in videos])
        return datetime.timedelta(seconds=time)

    def show_best_video(self):
        max_likes = max([int(item['statistics']['likeCount']) for item in self.video_response])
        max_likes_video = [video['id'] for video in self.video_response if
                           video['statistics']['likeCount'] == str(max_likes)][0]
        return f"https://youtu.be/{max_likes_video}"
