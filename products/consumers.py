from channels.generic.websocket import AsyncWebsocketConsumer
import json


class StockAlertConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("stock_alerts", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("stock_alerts", self.channel_name)

    async def stock_alert(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({
            'message': message
        }))
