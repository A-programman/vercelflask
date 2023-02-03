from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        question = request.form.get('question')
        history = request.form.get('history')
        response = {'question': question, 'history': history}
        return jsonify(response)
    else:
        # handle GET request
        response = {'message': 'GET request received'}
        return jsonify(response)