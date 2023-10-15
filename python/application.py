print("I'm working")
from simple_data_tool import SimpleDataTool as sdt;

sd = sdt()

from flask import Flask

app = Flask(__name__)

# Define a route that takes an argument in the URL
@app.route('/')
def main():
    return Flask.redirect('/home')

# Define a route that takes an argument in the URL
@app.route('/claimHandler/<id>')
def hello(id):
    return "number of claims for this handler is: " + str(sd.get_num_claims_for_claim_handler_id(id)) + "<br>avergae cost of claims is: " + str(sd.get_average_claim_cost_for_claim_handler(id))

@app.route('/home')
def home():
    return "number of closed claims: " + str(sd.get_num_closed_claims()) + "<br>state with the most disasters: " + str(sd.get_state_with_most_disasters()) + "<br>state with the least disasters: " + str(sd.get_state_with_least_disasters()) + "<br>number of claims delcared after it already ended: " + str(sd.get_num_disasters_declared_after_end_date())+ "<br><br>All agents and their total cost: " + str(sd.build_map_of_agents_to_total_claim_cost())

if __name__ == '__main__':
    app.run(debug=True)
