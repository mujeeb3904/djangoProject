from mongoengine import Document, StringField, DateTimeField, ReferenceField
from User.models import User
import datetime

class Blog(Document):
    createdBy = ReferenceField(User, required=True)
    title = StringField(max_length=100, required=True)
    description = StringField(required=True)
    content = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {"collection": "Blogs"}
