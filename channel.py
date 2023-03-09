import json
import os

from googleapiclient.discovery import build


class Channel:
    def __init__(self, id):
        self.__id = id
        self.title = Channel.get_channel_info(self)["items"][0]["snippet"]["title"]
        self.description = Channel.get_channel_info(self)["items"][0]["snippet"]["description"]
        self.path = f"https://www.youtube.com/channel/{self.__id}"
        self.subscriber_count = Channel.get_channel_info(self)["items"][0]["statistics"]["subscriberCount"]
        self.video_count = Channel.get_channel_info(self)["items"][0]["statistics"]["videoCount"]
        self.view_count = Channel.get_channel_info(self)["items"][0]["statistics"]["viewCount"]

    @property
    def id(self):
        return self.__id

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('API KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def get_channel_info(self):
        channel = Channel.get_service().channels().list(id=self.id, part='snippet,statistics').execute()
        return channel

    def to_json(self, file_name):
        info = {"title": self.title}
        with open(file_name, "w", encoding='windows-1251') as f:
            json.dump(info, f, indent=2, ensure_ascii=False)

    def __str__(self):
        return f"Youtube-канал: {self.title}"

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __lt__(self, other):
        return self.subscriber_count > self.subscriber_count


class Video:
    def __init__(self, id):
        self.video_id = id
        self.video_name = Video.get_video_info(self)["items"][0]["snippet"]["title"]
        self.video_count = Video.get_video_info(self)["items"][0]["statistics"]["viewCount"]
        self.like_count = Video.get_video_info(self)["items"][0]["statistics"]["likeCount"]

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('API KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def get_video_info(self):
        video = Video.get_service().videos().list(id=self.video_id, part='snippet,statistics').execute()
        return video

    def __str__(self):
        return f"Видео: {self.video_name}"


class PLVideo(Video):
    def __init__(self, id, playlist_id):
        super().__init__(id)
        self.playlist_id = playlist_id
        self.playlist_name = Video.get_video_info(self)["items"][0]["snippet"]["title"]

    def __str__(self):
        return f"Название видео: {self.video_name}. Название плейлиста: {self.playlist_name}"



video1 = Video('9lO06Zxhu88')
video2 = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
print(video1)

print(video2)
