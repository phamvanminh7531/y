from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import redis
import json

class Event(BaseModel):
    code: str
    timestamp: float | None = None

HOST = 'localhost'
PORT = 6379
STREAM_KEY = 'attendance_events'

# Kết nối Redis
r = redis.Redis(host=HOST, port=PORT, decode_responses=True)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Attendance Event API using Redis Stream"}

@app.post("/event/")
async def create_event(event: Event):
    # Ghi timestamp hiện tại
    event.timestamp = datetime.now().timestamp()

    # Thêm event vào Redis Stream
    event_dict = event.model_dump()
    r.xadd(STREAM_KEY, event_dict)

    return {"status": "published", "event": event_dict}
