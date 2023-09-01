import os
import json
from googleapiclient.discovery import build
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

api_key: str = os.getenv('YT_API_KEY')


class Channel:
    """Класс для ютуб-канала"""
    __youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        youtube_obj = self.get_service()

        data = youtube_obj.channels().list(id=channel, part='snippet,statistics').execute()

        self.__channel_id = data["items"][0]["id"]
        self.title = data["items"][0]["snippet"]["title"]
        self.description = data["items"][0]["snippet"]["description"]
        self.url = f'https://www.youtube.com/channel/{self.channel_id}'
        self.subscriber_count = int(data["items"][0]["statistics"]["subscriberCount"])
        self.video_count = data["items"][0]["statistics"]["videoCount"]
        self.view_count = data["items"][0]["statistics"]["viewCount"]

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        return self.subscriber_count - other.subscriber_count

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __eq__(self, other):
        return self.subscriber_count == other.subscriber_count

    @property
    def email(self):
        """Возвращает email сотрудника. К атрибуту можно обращаться без ()."""
        return self.__email

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube_obj = self.get_service()
        channel = youtube_obj.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        return cls.__youtube

    def to_json(self, json_file):
        json_data = {
            "channel_id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }
        with open(json_file, 'w') as file:
            file.write(json.dumps(json_data, indent=2, ensure_ascii=False))