from mongoengine import Document, StringField


class Url(Document):
    base_url = StringField()
    tiny_url = StringField()
