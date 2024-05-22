from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ProgressUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.uuid = self.scope['url_route']['kwargs']["uuid"]
        await self.channel_layer.group_add(self.uuid, self.channel_name)
        await self.accept()

    async def update_type(self, event):
        await self.send(text_data = event["msg"])