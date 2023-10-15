import simple_data_tool
import helpers
import plotly.express as px
import pandas as pd

disaster_data = simple_data_tool.SimpleDataTool.load_json_from_file(None, "data/sfcc_2023_disasters.json")
claims_data = simple_data_tool.SimpleDataTool.load_json_from_file(None, "data/sfcc_2023_claims.json")

def map_to_key_index(map):
    map_keys = list(map.keys())
    map_by_index = {}
    for index in range(len(map_keys)):
        values = [map_keys[index]]
        keys_value = map[map_keys[index]]
        if isinstance(keys_value, list):
            values.extend(keys_value)
        else:
            values.extend([keys_value])
        map_by_index[index] = values
    return map_by_index


disaster_to_state = {}
for disaster in disaster_data:
    disaster_to_state[disaster["id"]] = helpers.state_to_abbreviation[disaster["state"]]
state_to_claims_cost = {}
for claim in claims_data:
    state = disaster_to_state[claim["disaster_id"]]
    state_to_claims_cost[state] = state_to_claims_cost.get(state,0) + claim["estimate_cost"]
disasters_by_state_df = pd.DataFrame.from_dict(map_to_key_index(state_to_claims_cost), orient="index", columns=["state", "total claims cost"])
fig = px.choropleth(disasters_by_state_df,locations="state", locationmode="USA-states", color="total claims cost", scope="usa")
fig.show()


disaster_to_type = {}
for disaster in disaster_data:
    disaster_to_type[disaster["id"]] = disaster["type"]
type_to_impact = {}
for claim in claims_data:
    type = disaster_to_type[claim["disaster_id"]]
    cost = claim["estimate_cost"]
    life_lost = claim["loss_of_life"]
    type_to_impact[type] = type_to_impact.get(type,[0,0])
    type_to_impact[type] = [type_to_impact[type][0] + cost, type_to_impact[type][1] + life_lost]
disasters_by_cost_df = pd.DataFrame.from_dict(map_to_key_index(type_to_impact), orient="index", columns=["type of disaster", "total cost", "loss of life claims"])
fig = px.bar(disasters_by_cost_df, x="type of disaster", y="total cost", color="loss of life claims", title="Total Cost of Disasters")
fig.show()