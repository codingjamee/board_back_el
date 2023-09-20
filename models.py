from db_connect import db
from datetime import datetime

class Post(db.Model):
  __tablename__='post'
  board_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
  author = db.Column(db.String(50), nullable=False)
  title = db.Column(db.String(50), nullable=False)
  content = db.Column(db.Text, nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  like = db.Column(db.Integer, default=0)

  def __init__(self, author, title, content):
    self.author = author
    self.title = title
    self.content = content
