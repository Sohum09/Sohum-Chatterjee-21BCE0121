from flask import Flask, send_file, jsonify
from flask_socketio import SocketIO, emit
from game import Game

app = Flask(__name__)
socketio = SocketIO(app)
game = Game()

@app.route('/')
def index():
    return send_file(r'C:\Users\USER\OneDrive\Documents\Programs\C Cpp programs\Test\21BCE0121_SohumChatterjee_HitWicket\Client\index.html')

@app.route('/get_game_state')
def get_game_state():
    board_state = [[cell.to_dict() if cell else None for cell in row] for row in game.board]
    return jsonify({'state': board_state})

@socketio.on('connect')
def handle_connect(*args, **kwargs):
    print('Client connected')
    board_state = [[cell.to_dict() if cell else None for cell in row] for row in game.board]
    emit('game_state_update', {'board': board_state})

@socketio.on('player_move')
def handle_player_move(data):
    print(f"Move received: {data}")
    command = data.get('command')
    if game.move_character(command):
        new_state = {'board': [[cell.to_dict() if cell else None for cell in row] for row in game.board]}
        emit('game_state_update', new_state, broadcast=True)
    else:
        emit('invalid_move', {'message': 'Invalid move'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)
