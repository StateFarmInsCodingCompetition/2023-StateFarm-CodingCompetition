# This is the implementation of our simple API to interact with the JSON data files
# We enabled GET for every JSON. 1 to access all the data e.g: '/claims' (this can be used when displaying a list)
# and another one to see one sepcific data e.g: 'claim/claim_id' (this can be used when searching for a data and looking for details)
# We also created PUT and POST for disasters and claims, we thought it would make sense to enable the creation and update of those
# One could use '/disasters' as a POST to create a new disaster and '/disaster/disaster_id' as a PUT to update an existing one

from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# File paths
AGENTS_FILEPATH = 'data/sfcc_2023_agents.json'
CLAIM_HANDLERS_FILEPATH = 'data/sfcc_2023_claim_handlers.json'
CLAIMS_FILEPATH = 'data/sfcc_2023_claims.json'
DISASTERS_FILEPATH = 'data/sfcc_2023_disasters.json'

# Utility function to load data from a given filepath
def load_data(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

# Utility function to save data to a given filepath
def save_data(filepath, data):
    with open(filepath, 'w') as file:
        json.dump(data, file)

@app.route('/claims', methods=['GET'])
def get_claims():
    return jsonify(load_data(CLAIMS_FILEPATH))

@app.route('/claim/<int:claim_id>', methods=['GET'])
def get_claim_by_id(claim_id):
    claims = load_data(CLAIMS_FILEPATH)
    claim = next((claim for claim in claims if claim["id"] == claim_id), None)
    
    if claim:
        return jsonify(claim)
    else:
        return jsonify({"error": f"No claim found with ID {claim_id}"}), 404

@app.route('/claims', methods=['POST'])
def add_claim():
    claims = load_data(CLAIMS_FILEPATH)
    new_claim = request.json
    claims.append(new_claim)
    save_data(CLAIMS_FILEPATH, claims)
    return jsonify({"message": "New claim added successfully!"})

@app.route('/claims/<int:claim_id>', methods=['PUT'])
def update_claim(claim_id):
    claims = load_data(CLAIMS_FILEPATH)
    claim_to_update = next((claim for claim in claims if claim["id"] == claim_id), None)
    
    if claim_to_update:
        updated_data = request.json
        for key, value in updated_data.items():
            claim_to_update[key] = value
        save_data(CLAIMS_FILEPATH, claims)
        return jsonify({"message": f"Claim with ID {claim_id} updated successfully!"})
    else:
        return jsonify({"error": f"No claim found with ID {claim_id}"}), 404
    
@app.route('/claim_handlers', methods=['GET'])
def get_claim_handlers():
    return jsonify(load_data(CLAIM_HANDLERS_FILEPATH))

@app.route('/claim_handler/<int:handler_id>', methods=['GET'])
def get_claim_handler_by_id(handler_id):
    claim_handlers = load_data(CLAIM_HANDLERS_FILEPATH)
    handler = next((handler for handler in claim_handlers if handler["id"] == handler_id), None)
    
    if handler:
        return jsonify(handler)
    else:
        return jsonify({"error": f"No claim handler found with ID {handler_id}"}), 404
    
@app.route('/agents', methods=['GET'])
def get_agents():
    return jsonify(load_data(AGENTS_FILEPATH))

@app.route('/agent/<int:agent_id>', methods=['GET'])
def get_agent_by_id(agent_id):
    agents = load_data(AGENTS_FILEPATH)
    agent = next((agent for agent in agents if agent["id"] == agent_id), None)
    
    if agent:
        return jsonify(agent)
    else:
        return jsonify({"error": f"No agent found with ID {agent_id}"}), 404

@app.route('/disasters', methods=['GET'])
def get_disasters():
    return jsonify(load_data(DISASTERS_FILEPATH))

@app.route('/disaster/<int:disaster_id>', methods=['GET'])
def get_disaster_by_id(disaster_id):
    # Load existing disasters
    disasters = load_data(DISASTERS_FILEPATH)
    
    # Find the disaster with the specified ID
    disaster = next((disaster for disaster in disasters if disaster["id"] == disaster_id), None)
    
    if disaster:
        return jsonify(disaster)
    else:
        return jsonify({"error": f"No disaster found with ID {disaster_id}"}), 404

@app.route('/disasters', methods=['POST'])
def add_disaster():
    # Load existing disasters
    disasters = load_data(DISASTERS_FILEPATH)
    
    # Retrieve the new disaster data from the request
    new_disaster = request.json
    
    # Add the new disaster to the existing list
    disasters.append(new_disaster)
    
    # Save the updated disasters list back to the file
    save_data(DISASTERS_FILEPATH, disasters)
    
    return jsonify({"message": "New disaster added successfully!"})

@app.route('/disasters/<int:disaster_id>', methods=['PUT'])
def update_disaster(disaster_id):
    # Load existing disasters
    disasters = load_data(DISASTERS_FILEPATH)
    
    # Find the disaster to update
    disaster_to_update = next((disaster for disaster in disasters if disaster["id"] == disaster_id), None)
    
    if disaster_to_update:
        # Update the found disaster with data from the request
        updated_data = request.json
        for key, value in updated_data.items():
            disaster_to_update[key] = value
        
        # Save the updated disasters list back to the file
        save_data(DISASTERS_FILEPATH, disasters)
        
        return jsonify({"message": f"Disaster with ID {disaster_id} updated successfully!"})
    else:
        return jsonify({"error": f"No disaster found with ID {disaster_id}"}), 404


if __name__ == '__main__':
    app.run(debug=True)
