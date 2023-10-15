from flask import Flask, jsonify, request
from flask_cors import CORS
from simple_data_tool import SimpleDataTool

# Create Flask App
app = Flask(__name__)

# Enable CORS for the Flask app
CORS(app, supports_credentials=True)

# Create Simple Data Tool
data_tool = SimpleDataTool()

# Test Set One
@app.route('/disasters/count', methods=['GET'])
def get_disaster_count_by_state():
    state = request.args.get('state')
    count = data_tool.get_disaster_count_by_state(state)
    return jsonify({'count': count})

# Test Set Two
@app.route('/disasters/total-claim-cost', methods=['GET'])
def get_total_claim_cost_for_disaster():
    disaster_id = request.args.get('disaster_id')
    total_claim_cost = data_tool.get_total_claim_cost_for_disaster(disaster_id)
    return jsonify({'total_claim_cost': total_claim_cost})

@app.route('/claims/average-claim-cost', methods=['GET'])
def get_average_claim_cost_for_claim_handler():
    claim_handler_id = request.args.get('claim_handler_id')
    average_claim_cost = data_tool.get_average_claim_cost_for_claim_handler(claim_handler_id)
    return jsonify({'average_claim_cost': average_claim_cost})

@app.route('/disasters/most', methods=['GET'])
def get_state_with_most_disasters():
    state = data_tool.get_state_with_most_disasters()
    return jsonify({'state': state})

@app.route('/disasters/least', methods=['GET'])
def get_state_with_least_disasters():
    state = data_tool.get_state_with_least_disasters()
    return jsonify({'state': state})

@app.route('/agents/most-spoken-language', methods=['GET'])
def get_most_spoken_agent_language_by_state():
    state = request.args.get('state')
    language = data_tool.get_most_spoken_agent_language_by_state(state)
    return jsonify({'language': language})

@app.route('/claims/open-count', methods=['GET'])
def get_num_of_open_claims_for_agent_and_severity():
    agent_id = request.args.get('agent_id')
    min_severity_rating = request.args.get('min_severity_rating')
    num_of_open_claims = data_tool.get_num_of_open_claims_for_agent_and_severity(agent_id, min_severity_rating)
    return jsonify({'num_of_open_claims': num_of_open_claims})

@app.route('/disasters/declared-after-end-date-count', methods=['GET'])
def get_num_disasters_declared_after_end_date():
    count = data_tool.get_num_disasters_declared_after_end_date()
    return jsonify({'count': count})

@app.route('/agents/total-claim-cost', methods=['GET'])
def build_map_of_agents_to_total_claim_cost():
    agent_total_claim_cost = data_tool.build_map_of_agents_to_total_claim_cost()
    return jsonify(agent_total_claim_cost)

@app.route('/disasters/claim-density', methods=['GET'])
def calculate_disaster_claim_density():
    disaster_id = request.args.get('disaster_id')
    claim_density = data_tool.calculate_disaster_claim_density(disaster_id)
    return jsonify({'claim_density': claim_density})

# Test Set Four
@app.route('/claims/top-three-months', methods=['GET'])
def get_top_three_months_with_highest_num_of_claims_desc():
    top_three_months = data_tool.get_top_three_months_with_highest_num_of_claims_desc()
    return jsonify({'top_three_months': top_three_months})

if __name__ == '__main__':
    app.run(debug=True)