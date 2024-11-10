from channels.generic.websocket import AsyncWebsocketConsumer
import json

class TaskNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'task_notifications'
        self.room_group_name = f"task_{self.room_name}"

        # Join the group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive task completion result from Celery task
    async def send_task_result(self, event):
        result = event['result']
        # Send the result to WebSocket client
        await self.send(text_data=json.dumps({
            'type': 'task_complete',
            'result': result
        }))

