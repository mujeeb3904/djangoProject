
from mongoengine import Document, StringField, EmailField, DateTimeField
import datetime

class User(Document):
    name = StringField(max_length=100, required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(max_length=100, required=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {"collection": "user"} 