from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.cache import cache
from asgiref.sync import async_to_sync


class ServeConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.stnID = ''
        await self.accept()

    async def receive_json(self, content):
        token = content.get('tok')
        if token is not None:
            StationID = cache.get(token)
            self.stnID = StationID
            if StationID is not None:
                cache.set(StationID, self.channel_name)
                await self.send_json({'code': 'OK-200'})
            else:
                await self.send_json({'code': 'UNAUTHED-400'})
                await self.close()

    async def chat_message(self, event):
        await self.send_json(event['text'])

    async def disconnect(self, close_code):
        # Called when the socket
        cache.delete(self.stnID)
        await self.send_json({'code':'OUT-200'})
        print(close_code)
