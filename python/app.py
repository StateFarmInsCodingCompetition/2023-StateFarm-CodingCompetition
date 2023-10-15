from flask import Flask, render_template
from simple_data_tool import SimpleDataTool

app = Flask(__name__)
data_tool = SimpleDataTool()

@app.route('/agents', methods=['GET'])
def get_agents_table():
    agents = data_tool.get_agent_data()
    return render_template('agents_table.html', agents=agents)

@app.route('/claims', methods=['GET'])
def get_claims_table():
    claims = data_tool.get_claim_data()
    return render_template('claims_table.html', claims=claims)

@app.route('/disasters', methods=['GET'])
def get_disasters_table():
    disasters = data_tool.get_disaster_data()
    return render_template('disasters_table.html', disasters=disasters)

@app.route('/disaster/<int:disaster_id>', methods=['GET'])
def get_disaster(disaster_id):
    disaster = data_tool.get_disaster_by_id(disaster_id)  
    return render_template('disasters_table.html', disasters=[disaster])

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
