import os

from flask import Flask, request, jsonify

from langchain.agents import initialize_agent, Tool, load_tools
from langchain.llms import OpenAI
from langchain.utilities import GoogleSearchAPIWrapper

llm = OpenAI(temperature=0)
tools = load_tools(["serpapi"], llm=llm)
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)


search = GoogleSearchAPIWrapper()
app = Flask(__name__)

def generate_reference(prompt):
    return agent.run("Find an excerpt from an article from PubMed to support this assertion, (Ask yourself if the found article excerpt actually supports the assertion, if you can't find it after a few searches, then reply with NONE FOUND): " + prompt)

def generate_response(prompt):
    return search.results(prompt, 1)

def generate_revision(prompt):
    return agent.run("Revise this statement to be accurate to medical information from PubMed:" + prompt)

@app.route('/', methods=['GET', 'POST'])
def handle_request():
    if request.method == 'POST':
        assertion = request.json.get('assertion')
        reference = generate_reference(assertion)
        print("REFERENCE: " + reference)
        if reference == "NONE FOUND":
            revision = generate_revision(assertion)
            return jsonify([{"title": "Revision", "revision": revision}])
        else:
            response = generate_response(reference)
            return jsonify(response)
    elif request.method == 'GET':
        return jsonify({'response': "GET REQUEST RECEIVED"})