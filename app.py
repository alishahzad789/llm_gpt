from dotenv import load_dotenv

from flask import Flask, request, jsonify

from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_community.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
import pandas as pd


import os

load_dotenv()

OPEN_AI_KEY = os.getenv('OPEN_AI_KEY')


app = Flask(__name__)

df = pd.read_csv('sales_performance_data.csv')


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/api/rep_performance', methods=['GET'])
def individual_sale_analysis():
    rep_id = request.args.get('rep_id')
    agent = create_pandas_dataframe_agent(
        ChatOpenAI(temperature=0, model="gpt-4",api_key=OPEN_AI_KEY),
        df,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        allow_dangerous_code=True
    )
    result = agent.run(f'quantitative performance review and feedback of employee_id = {rep_id} ?')
    return jsonify(result)  


@app.route('/api/team_performance', methods=['GET'])
def team_peformance_analysis():
    agent = create_pandas_dataframe_agent(
        ChatOpenAI(temperature=0, model="gpt-4",api_key=OPEN_AI_KEY),
        df,
        verbose=True,
        allow_dangerous_code=True,
        agent_type=AgentType.OPENAI_FUNCTIONS
    )
    # Now you can use the agent to interact with the dataframe
    result = agent.run('Calculate mean, median, standard deviation, minimum, and maximum for each numerical column in the DataFrame. Exclude employee_id column')
    return jsonify(result)      




@app.route('/api/performance_trends', methods=['GET'])
def performance_trends():
    time_period = request.args.get('time_period')
    agent = create_pandas_dataframe_agent(
        ChatOpenAI(temperature=0.5, model="gpt-4",api_key=OPEN_AI_KEY),
        df,
        verbose=True,
        agent_type="openai-tools",
        allow_dangerous_code=True,
    )
    result  = ""
    if time_period == 'monthly':
        result = agent.run('Analyse data to identify trends monthly. Use dated column to fetch months. Exclude employee_id column')
    if time_period == 'quarterly':
        result = agent.run('Analyse data to identify trends quarterly. Use dated column to fetch months. Exclude employee_id column')

    forecast_result = agent.run('Analyse data to forecast future performance. Use dated column to fetch month wise')
    result = result + '\n' +forecast_result  
    return jsonify(result)  