import redis
import time

HOST = 'localhost'
PORT = 6379
STREAM_KEY = 'attendance_events'

r = redis.Redis(host=HOST, port=PORT, decode_responses=True)

# Bắt đầu từ tin nhắn mới nhất ("$")
last_id = "0-0"  

print("Consumer started. Waiting for events...\n")

while True:
    try:
        # Đọc stream, block 2 giây
        events = r.xread({STREAM_KEY: last_id}, block=0, count=1)

        if events:
            for stream, messages in events:
                for message_id, data in messages:
                    print(f"[{message_id}] {data}")
                    last_id = message_id
    except Exception as e:
        print("Error:", e)
        time.sleep(1)
