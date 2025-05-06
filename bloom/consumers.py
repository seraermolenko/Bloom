import json
from channels.generic.websocket import AsyncWebsocketConsumer

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GardenConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.garden_id = self.scope['url_route']['kwargs']['garden_id']
        self.room_group_name = f"garden_{self.garden_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        updated_plant = text_data_json['updated_plant']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'plant_status_update',
                'updated_plant': updated_plant
            }
        )

    async def plant_status_update(self, event):
        updated_plant = event['updated_plant']

        await self.send(text_data=json.dumps({
            'updated_plant': updated_plant,
        }))
