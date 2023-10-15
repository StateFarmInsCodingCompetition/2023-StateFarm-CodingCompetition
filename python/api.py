import flask
from simple_data_tool import SimpleDataTool
from flask import request, jsonify


app = flask.Flask(__name__)
app.config["DEBUG"] = True

def controller():
    return SimpleDataTool()


@app.route('/', methods=['GET'])
def home():
    return "<h1>Disaster Info API</h1><p>This site is an API for getting info about disaster info.</p>"


# Return all claim entries of given params
@app.route('/api/v1/claims', methods=['GET'])
def api_claims_params():
    # Check if any param is provided as part of the URL.
    # If no param is provided, display all data
    params = [
        "id",
        "disaster_id",
        "status",
        "total_loss",
        "loss_of_life",
        "type",
        "severity_rating",
        "estimate_cost",
        "agent_assigned_id",
        "claim_handler_assigned_id",
    ]
    param_dict = {key: None for key in params}
    for param in params:
        if param in request.args:
            val = request.args[param]
            param_dict[param] = val.lower()
            
    
    # return corresponding claim data
    claim_data_df = controller().get_claim_data_df()
    for key, value in param_dict.items():
        if value != None:
            claim_data_df = claim_data_df[(claim_data_df[key].astype(str).str.lower()  == value)]

    return claim_data_df.to_json(orient = "records", lines = True)



# Return all agent entries of given params
@app.route('/api/v1/agents', methods=['GET'])
def api_agents_params():
    # Check if any param is provided as part of the URL.
    # If no param is provided, display all data
    params = [
        "id",
        "first_name",
        "last_name",
        "state",
        "region",
        "primary_language",
        "secondary_language",
        "years_active"
    ]
    param_dict = {key: None for key in params}
    for param in params:
        if param in request.args:
            val = request.args[param]
            param_dict[param] = val.lower()
            
    
    # return corresponding agent data
    agent_data_df = controller().get_agent_data_df()
    for key, value in param_dict.items():
        if value != None:
            agent_data_df = agent_data_df[(agent_data_df[key].astype(str).str.lower()  == value)]

    return agent_data_df.to_json(orient = "records", lines = True)



# Return all disaster entries of given params
@app.route('/api/v1/disasters', methods=['GET'])
def api_disasters_params():
    # Check if any param is provided as part of the URL.
    # If no param is provided, display all data
    params = [
        "id",
        "type",
        "state",
        "name",
        "description",
        "start_date",
        "end_date",
        "declared_date",
        "lat",
        "long",
        "radius_miles"
    ]
    param_dict = {key: None for key in params}
    for param in params:
        if param in request.args:
            val = request.args[param]
            param_dict[param] = val.lower()
            
    
    # return corresponding disaster data
    disaster_data_df = controller().get_disaster_data_df()
    for key, value in param_dict.items():
        if value != None:
            disaster_data_df = disaster_data_df[(disaster_data_df[key].astype(str).str.lower()  == value)]

    return disaster_data_df.to_json(orient = "records", lines = True)


# Return all claim handlers entries of given params
@app.route('/api/v1/claim_handlers', methods=['GET'])
def api_claim_handlers_params():
    # Check if any param is provided as part of the URL.
    # If no param is provided, display all data
    params = [
        "first_name",
        "last_name",
        "id"
    ]
    param_dict = {key: None for key in params}
    for param in params:
        if param in request.args:
            val = request.args[param]
            param_dict[param] = val.lower()
            
    
    # return corresponding claim handler data
    claim_handler_data_df = controller().get_claim_handler_data_df()
    for key, value in param_dict.items():
        if value != None:
            claim_handler_data_df = claim_handler_data_df[(claim_handler_data_df[key].astype(str).str.lower()  == value)]

    return claim_handler_data_df.to_json(orient = "records", lines = True)


app.run()