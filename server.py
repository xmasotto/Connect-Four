from flask import Flask, request
import random
import json
from minimax import *
from connect4_utils import *

app = Flask(__name__)

# all of the AI state is stored here!
session_dict = {}

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/builder')
def shapes():
    return app.send_static_file('shapes.html')

# @app.route('/init_game', methods=['POST'])
# def init_game():
#     print("INIT GAME!")
#     session = {}

#     yellow_code = request.form['yellow_code']
#     red_code = request.form['red_code']

#     if yellow_code:
#         try:
#             session['yellow'] = Minimax(Eval(yellow_code))
#         except e:
#             return "ERROR Yellow AI is invalid!"

#     if red_code:
#         try:
#             session['red'] = Minimax(Eval(red_code))
#         except e:
#             return "ERROR Red AI is invalid!"

#     # save the session to a global variable
#     global session_dict;
#     while True:
#         key = str(random.random())
#         if key not in session_dict:
#             session_dict[key] = session
#             break
#     return key

@app.route('/get_move', methods=['POST'])
def get_move():
    board = request.form['board']
    color = request.form['color']
    code = request.form['code']

    try:
        ai = Minimax(Eval(code))
        result = ai.bestMove(
            2,
            list(reversed(json.loads(board))),
            "x" if color == "yellow" else "o"
        )
        return result
    except Exception as e:
        raise
        # return str(e)

if __name__ == '__main__':
    # app.run(processes=8)
    app.run(debug=True)
