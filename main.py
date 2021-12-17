from flask import Flask
from maze_generator import make_maze
from spell_generator import make_spell

app = Flask(__name__)

@app.route('/maze', methods=['GET', 'POST'])
def generate_maze():
    return {
        'message': f'```\n{make_maze()}\n```'
    }

@app.route('/spell', methods=['GET', 'POST'])
def generate_spell():
    spells = [make_spell() for _ in range(20)]
    spells_str = "\n".join(spells)

    return {
        'message': f'```\n{spells_str}\n```'
    }
