import json
import redis

redis_client = redis.Redis(host="redis", port=6379, db=0)

def publish_event(event_name: str, payload: dict):

    event = {
        "event_name": event_name,
        "payload": payload,
    }
    redis_client.publish("domain_events", json.dumps(event))

