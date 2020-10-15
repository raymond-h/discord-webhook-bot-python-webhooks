from flask import Flask, request, jsonify
from maze_generator import make_maze

app = Flask(__name__)

@app.route('/maze', methods=['GET', 'POST'])
def generate_maze():
    return {
        'message': f'```\n{make_maze()}\n```'
    }
