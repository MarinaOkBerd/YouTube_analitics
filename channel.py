import json
import os

from googleapiclient.discovery import build



class Channel:

    def __init__(self, id):
        self.__id = id
        self.title = Channel.get_channel_info["items"][0]["snipper"]["title"]
        self.description = Channel.get_channel_info(self)["items"][0]["snipper"]["description"]
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

    def get_channel_info(self):
        channel =Channel.get_service().channels().list(id=self.id, part='snippet,statistics').execute()
        return channel

    def to_json(self, file_name):
        info = {"title": self.title}
        with open(file_name, "w", encoding='windows-1251') as f:
            json.dump(info, f, indent=2, ensure_ascii=False)



#vdud = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
#vdud.get_channel_info()
#print(vdud.title)
#print(vdud.video_count)
#print(Channel.get_service())
