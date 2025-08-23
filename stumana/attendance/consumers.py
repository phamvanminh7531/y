import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AttendanceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("attendance_group", self.channel_name)
        await self.accept()
        print("Client connected!")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("attendance_group", self.channel_name)
        print("Client disconnected!")

    async def attendance_event(self, event):
        # Debug: Print the entire event to see the structure
        print("Full event received:", event)
        
        # Extract data from the event
        data = event.get("data", {})
        print("Consumer received data:", data)
        
        # Send data to WebSocket client
        try:
            await self.send(text_data=json.dumps(data))
            print("Data sent to client successfully")
        except Exception as e:
            print(f"Error sending data to client: {e}")

    # Optional: Handle direct WebSocket messages from client
    async def receive(self, text_data):
        print("Received message from client:", text_data)