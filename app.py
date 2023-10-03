from flask import Flask, render_template, jsonify, request, make_response
from flask_cors import CORS
from db_connect import db
from models import Post
from sqlalchemy import select
from datetime import datetime

import logging

app = Flask(__name__)

# Database Settings
app.config.from_pyfile('./config.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Logger Settings
app.logger.setLevel(logging.INFO)
app.logger.info("Flask app is running")
logging.basicConfig(filename='app.log', level=logging.INFO)

# CORS
CORS(app, supports_credentials=True)

@app.route('/', methods=['GET', 'OPTIONS'])
def render_home() :
  return jsonify('Hello')

@app.route('/total', methods=['GET', 'OPTIONS'])
def render_contents():
  if request.method == 'OPTIONS':
    response = make_response()
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET') 
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response
  else:
    data = Post.query.order_by(Post.created_at.desc()).all()
    data_json = [{'author': post.author, 'title': post.title, 'content': post.content, 'created_at': post.created_at} for post in data]
    return jsonify(data_json)
  



#게시물 작성

@app.route('/post', methods=['POST'])
def create_post():
  req_data = request.get_json()

  author = req_data['author']
  title = req_data['title']
  content = req_data['content']
  post = Post(author, title, content)
  db.session.add(post)
  db.session.commit()
  return jsonify({'result' : 'success'})

#게시물 읽기
@app.route('/posts', methods=['GET'])
def read_post():
  data = Post.query.order_by(Post.created_at.desc()).all()
  post_list = []

  for post in data :
    post_data = {
      'id': post.board_id,
      'author': post.author,
      'title' : post.title,
      'content' : post.content,
      'created_at' : post.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }
    post_list.append(post_data)

  return jsonify(post_list)


#게시물 수정
@app.route('/post/<post_id>/', methods=['PUT'])
def update_post(post_id):
  req_data = request.get_json()
  print('updatepost')
  selected_post = Post.query.filter_by(board_id = post_id).first()
  print(selected_post)
  if 'author' in req_data :
    selected_post.author = req_data['author']
  if 'title' in req_data :
    selected_post.title = req_data['title']
  if 'content' in req_data :
    selected_post.content = req_data['content']
  selected_post.created_at = datetime.utcnow()
  db.session.add(selected_post)
  db.session.commit()
  return jsonify({'result' : 'update success'})

#게시물 삭제
@app.route('/post/<post_id>/', methods=['DELETE'])
def delete_post(post_id):
  selected_post = Post.query.filter_by(board_id = post_id).first()

  db.session.delete(selected_post)
  db.session.commit()
  return jsonify({'result' : 'delete success'})


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=True)
