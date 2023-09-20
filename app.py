from flask import Flask, render_template, jsonify, request, make_response
from sqlalchemy import create_engine, text
from flask_cors import CORS
from db_connect import db
from models import Post

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

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=True)
