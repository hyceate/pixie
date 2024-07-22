from db import db
from datetime import datetime

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(255))
  image_url = db.Column(db.String(255))
  author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now)
  updated_at = db.Column(db.DateTime, default=datetime.now)