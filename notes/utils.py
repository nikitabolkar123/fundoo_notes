import redis
import json
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0
)
print(redis_client)
class RedisStore:

    def set(self, key, value):
        return redis_client.set(key, value)

    def get(self, key):
        return redis_client.get(key)

class RedisCrud:
    def __init__(self):
        self.redis=RedisStore()

    def save(self,notes,user_id):
        notes_dict=self.redis.get(user_id)
        print(notes_dict)
        if notes_dict is None:
            notes_dict={}
        note_id=notes.get('id')
        notes_dict.update({note_id:notes})
        print(notes_dict)
        self.redis.set(user_id,json.dumps(notes_dict))