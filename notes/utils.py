import redis
import json
from django.shortcuts import get_object_or_404, redirect
import user

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

    def save(self, notes, user_id):
        notes_dict = self.redis.get(user_id)
        if notes_dict is None:
            notes_dict = {}
        else:
            notes_dict = json.loads(notes_dict)
        note_id = notes.get('id')
        notes_dict.update({note_id: notes})
        self.redis.set(user_id, json.dumps(notes_dict))

    def put(self, note_id, new_note, user_id):
        notes_dict = self.redis.get(str(user_id))
        if notes_dict is None:
            return {}
        else:
            notes_dict = json.loads(notes_dict)
            n_id = str(note_id)
            if n_id in notes_dict.keys():
                notes_dict.update({n_id: new_note})
                self.redis.set(user_id, json.dumps(notes_dict))
                return True
        return False
    def retrieve(self, user):
        user_id = user.id
        notes_dict = json.loads(self.redis.get(str(user_id)))
        if notes_dict is None:
            return None
        return notes_dict.values()


    def delete(self, note_id, user):
        user_id = str(user.id)
        notes_dict = self.redis.get(user_id)
        if notes_dict is not None:
            notes_dict = json.loads(notes_dict)
            note = notes_dict.get(str(note_id))
            if note:
                notes_dict.pop(str(note_id))
                self.redis.set(user_id, json.dumps(notes_dict))