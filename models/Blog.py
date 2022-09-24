from db import db
from sqlalchemy.sql import func
from dateutil import tz
from datetime import datetime

class BlogModel(db.Model):
    __tablename__ = 'blog'

    blogid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    title = db.Column(db.String(100))
    content = db.Column(db.String(2000))
    addeddate = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updatedate = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())


    def __init__(self, username, title, content):
        self.username = username
        self.title = title
        self.content = content

    def json(self):
        return {
            'blogId': self.blogid,
            'username': self.username, 
            'title': self.title, 
            'content': self.content, 
            'addedDate': convertUtcToLocal(str(self.addeddate)),
            'updateDate': convertUtcToLocal(str(self.updatedate))
        }

    @classmethod
    def find_by_blogid(cls, blogid):
        return cls.query.filter_by(blogid=blogid).first()

    @classmethod
    def find_blog_by_username(cls, username):
        return cls.query.filter_by(username=username)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_from_db(self):
        db.session.add(self)
        db.session.commit()
    
def convertUtcToLocal(utcTime):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    utc = datetime.strptime(utcTime, '%Y-%m-%d %H:%M:%S')
    utc = utc.replace(tzinfo=from_zone)
    central = utc.astimezone(to_zone)
    return str(central);