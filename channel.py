
import json
import os

from datetime import timedelta, datetime

from googleapiclient.discovery import build

class MixinYouTube:
    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('API KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


class Channel(MixinYouTube):
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
        return self.subscriber_count > other.subscriber_count

    def __gt__(self, other):
        return self.subscriber_count < other.subscriber_count


class Video(MixinYouTube):
    def __init__(self, id):
        self.video_id = id
        self.video_name = Video.get_video_info(self)["items"][0]["snippet"]["title"]
        self.video_count = Video.get_video_info(self)["items"][0]["statistics"]["viewCount"]
        self.like_count = Video.get_video_info(self)["items"][0]["statistics"]["likeCount"]

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


class PlayList(MixinYouTube):
    def __init__(self, id):
        super().__init__()
        self.id = id

    def get_pl_info(self):
        playlist = PlayList.get_service().playlists().list(id=self.id, part='snippet').execute()
        return playlist

    @property
    def get_title(self):
        playlist_name = PlayList.get_pl_info(self)["items"][0]["snippet"]["title"]
        return playlist_name
    @property
    def get_path(self):
        return f"https://www.youtube.com/playlist?list={self.id}"

    def get_videos_list(self):
        play_list = PlayList.get_service().playlistItems().list(playlistId=self.id, part='contentDetails', maxResults=50).execute()
        videolist = []
        for i in play_list["items"]:
            videolist.append(i['contentDetails']['videoId'])
        return videolist


    @property
    def total_duration(self):
        videolist = self.get_videos_list()
        total_duration = timedelta()
        for video in videolist:
                duration = video["items"][0]["contentDetails"]["duration"]
                time_duration = datetime.strptime(duration, "PT%HH%MM%SS") - datetime.strptime("00:00:00", "%H:%M:%S")
                total_duration += time_duration
        return total_duration

    def show_best_video(self):
        videolist = self.get_videos_list()
        best_video = None
        likes = 0
        for video in videolist:
            if int(video["statistics"]["likeCount"]) > likes:
                best_video = video
                likes = int(video["statistics"]["likeCount"])
        return f"https://youtu.be/{best_video['id']}"





#video1 = Video('9lO06Zxhu88')
#video2 = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
#print(video1)
#print(video2)
pl = PlayList('PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb')
print(pl)
print(pl.get_path)

print(pl.total_duration())
print(pl.show_best_video())