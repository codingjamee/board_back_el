from db_connect import db
from datetime import datetime

class Post(db.Model):
  __tablename__='post'
  id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
  author = db.Column(db.String(256), nullable=False)
  content = db.Column(db.Text, nullable=False)
  like = db.Column(db.Integer, default=0)
  create_at = db.Column(db.Datetime, default=datetime.utcnow)

  def __init__(self, author, content):
    self.author = author
    self.content = content
