import json
from flask import Flask, render_template, request

app = Flask(__name__)

# Define the function to filter agents and claim handlers
def filter_agents_claim_handlers(agents, claim_handlers, region=None, language=None):
    """
    Filters agents and claim handlers based on provided criteria.
    
    :param agents: List of agents with their details.
    :param claim_handlers: List of claim handlers with their details.
    :param region: The region to filter by (applies only to agents).
    :param language: The language to filter by (applies to both agents and claim handlers).
    :return: Filtered list of agents and claim handlers.
    """

    def apply_region_filter(data, region):
        if region:
            return [d for d in data if d.get('region') == region]
        return data

    def apply_language_filter(data, language):
        if language:
            return [d for d in data if language in [d.get('primary_language'), d.get('secondary_language')]]
        return data

    # Apply region filter only to agents
    filtered_agents = apply_region_filter(agents, region)
    # Apply language filter to both agents and claim handlers
    filtered_agents = apply_language_filter(filtered_agents, language)
    filtered_claim_handlers = apply_language_filter(claim_handlers, language)

    return filtered_agents, filtered_claim_handlers



# Function to load JSON data
def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Paths to your JSON files (update these paths to the correct ones on your system)
path_to_agents_json = '/Users/yashsarkar/2023-StateFarm-CodingCompetition/python/data/sfcc_2023_agents.json'
path_to_claim_handlers_json = '/Users/yashsarkar/2023-StateFarm-CodingCompetition/python/data/sfcc_2023_claim_handlers.json'

# Load data from JSON files
agents = load_json_data(path_to_agents_json)
claim_handlers = load_json_data(path_to_claim_handlers_json)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        region = request.form.get('region')
        language = request.form.get('language')
        filtered_agents, filtered_claim_handlers = filter_agents_claim_handlers(
            agents, claim_handlers, region, language
        )
        return render_template('index.html', agents=filtered_agents, claim_handlers=filtered_claim_handlers)
    return render_template('index.html', agents=[], claim_handlers=[])


if __name__ == '__main__':
    app.run(debug=True)
