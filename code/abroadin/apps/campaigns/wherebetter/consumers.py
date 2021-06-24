import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Participant


class GameConsumer(AsyncWebsocketConsumer):

    async def check_is_participant(self, user):
        return await database_sync_to_async(Participant.objects.filter(user=user).exists)()

    async def connect(self):
        # has_participant_account = await self.check_is_participant(self.scope["user"])
        # print(has_participant_account)
        print(self.scope['user'])
        await self.accept()
        print(self.scope['user'])


    # async def receive(self, text_data=None, bytes_data=None):

