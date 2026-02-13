import redis
import json

redis_client = redis.Redis(host="redis", port=6379, db=0)

def listen_events():
    pubsub = redis_client.pubsub()
    pubsub.subscribe("domain_events")

    print("Listening for domain events...")
    for message in pubsub.listen():
        if message["type"] == "message":
            event = json.loads(message["data"])
            print(f"Consumed event: {event}")

