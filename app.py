import json
import random
from flask import Flask, jsonify, render_template

app = Flask(__name__)

with open('data/fields.json') as f:
    ALL_FIELDS = json.load(f)


@app.route('/schema')
def schema():
    fields = ALL_FIELDS[:]
    random.shuffle(fields)
    count = random.randint(1, len(fields))
    return jsonify(fields[:count])


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
