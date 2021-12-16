from flask import Flask, request, jsonify
from maze_generator import make_maze
from meme_image import make_image

app = Flask(__name__)

@app.route('/maze', methods=['GET', 'POST'])
def generate_maze():
    return {
        'message': f'```\n{make_maze()}\n```'
    }

@app.route('/meme', methods=['POST'])
def meme_image():
    image_url = request.json['arguments']

    make_image(image_url)

    return {
        'message': image_url
    }
