import logging
from flask import Flask, render_template, jsonify, request, make_response
from flask_cors import CORS
app = Flask(__name__)
CORS(app, supports_credentials=True)

contents = [
  {
    'board_id': 1,
    'category': "talk",
    'title': "제목",
    'writer': "jane",
    'content': "Hi!!! How nice the weather!",
    'regdate': "2023-09-16",
  },
  {
    'board_id': 2,
    'category': "share",
    'title': "제목2",
    'writer': "Peter",
    'content': "I'm studying React now!!!",
    'regdate': "2023-09-12",
  },
  {
    'board_id': 3,
    'category': "question",
    'title': "제목3",
    'writer': "zenkins",
    'content': "What on earth is React?",
    'regdate': "2023-09-12",
  },
]

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
        return jsonify(contents)


app.logger.setLevel(logging.INFO)
app.logger.info("Flask app is running")
logging.basicConfig(filename='app.log', level=logging.INFO)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=True, ) 