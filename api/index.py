import os

from flask import Flask, request, jsonify

from langchain.agents import initialize_agent, Tool, load_tools
from langchain.llms import OpenAI
from langchain.utilities import GoogleSearchAPIWrapper


os.environ["GOOGLE_API_KEY"] = "AIzaSyACujhbTZfoeNbvNmkZ3nVNLHAs8kQXmhA"
os.environ["GOOGLE_CSE_ID"] = "56a78a900f119419b"
search = GoogleSearchAPIWrapper()
app = Flask(__name__)

def generate_response(prompt):
    return search.results(prompt, 5)

@app.route('/', methods=['GET', 'POST'])
def handle_request():
    if request.method == 'POST':
        assertion = request.json.get('assertion')
        response = generate_response(assertion)
        return jsonify(response)
    elif request.method == 'GET':
        return jsonify({'response': "GET REQUEST RECEIVED"})
