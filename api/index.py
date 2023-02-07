
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI

from flask import Flask, request, jsonify

import os
os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPAPI_API_KEY"] = "684035001579d1e54d72e18206f5e7d46c1a7d30ddf0ee213e7314692b668a5f"
app = Flask(__name__)

def generate_response(assertion):
    llm = OpenAI(temperature=0)
    tools = load_tools(["serpapi"], llm=llm)
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

    response = agent.run("Find and quote an excerpt from an article from PubMed to support this assertion, once found state the authors, titles and source (Ask yourself if the found article excerpt actually supports the assertion, if you can't find it after a few searches, then there is none found): " + assertion)

    return response

@app.route('/', methods=['GET', 'POST'])
def handle_request():
    if request.method == 'POST':
        assertion = request.json.get('assertion')
        response = generate_response(assertion)
        return jsonify({'response': response})
    elif request.method == 'GET':
        return jsonify({'response': "GET REQUEST RECEIVED"})
