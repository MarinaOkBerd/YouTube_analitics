import json
import os

from googleapiclient.discovery import build


class Channel:


    # создать специальный объект для работы с API


    def __init__(self, id):
        self.id = id

    def _get_channel_info(self):

        channel = Channel.youtube.channels().list(id=self.id, part='snippet,statistics').execute()
        return channel
api_key: str = os.getenv('YT_API_KEY')
print(api_key is None)
youtube = build('youtube', 'v3', developerKey=api_key)
vdud = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
vdud._get_channel_info()