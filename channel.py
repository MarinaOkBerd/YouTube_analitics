import json
import os

from googleapiclient.discovery import build
from pprint import pprint


class Channel:

    def __init__(self, id):
        self.id = id

    def _get_channel_info(self):
        api_key: str = os.getenv('API KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.id, part='snippet,statistics').execute()
        return pprint(json.dumps(channel, indent=2, ensure_ascii=False))


vdud = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
vdud._get_channel_info()
