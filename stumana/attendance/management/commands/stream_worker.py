from django.core.management.base import BaseCommand
import redis
import asyncio
import json
from channels.layers import get_channel_layer

class Command(BaseCommand):
    help = "Run Redis stream worker for attendance"

    async def run_worker(self):
        try:
            r = redis.Redis(host="localhost", port=6379, decode_responses=True)
            stream_key = "attendance_events"
            last_id = "0-0"
            channel_layer = get_channel_layer()

            self.stdout.write(self.style.SUCCESS("Listening for Redis stream events..."))

            while True:
                try:
                    events = r.xread({stream_key: last_id}, block=2000, count=10)
                    
                    if events:
                        for stream, messages in events:
                            for message_id, data in messages:
                                print(f"Processing message {message_id}: {data}")
                                
                                # Send to WebSocket group
                                await channel_layer.group_send(
                                    "attendance_group",
                                    {
                                        "type": "attendance_event",
                                        "data": data,
                                        "message_id": message_id,  # Optional: include message ID
                                    }
                                )
                                
                                print("Sent to group:", data)
                                last_id = message_id
                                
                except redis.RedisError as e:
                    print(f"Redis error: {e}")
                    await asyncio.sleep(5)  # Wait before retrying
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    await asyncio.sleep(1)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to start worker: {e}"))

    def handle(self, *args, **kwargs):
        try:
            asyncio.run(self.run_worker())
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS("Worker stopped by user"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Worker failed: {e}"))