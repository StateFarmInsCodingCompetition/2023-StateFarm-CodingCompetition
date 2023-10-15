import json
import random

agent_file_name = '../data/sfcc_2023_agents.json'
claim_file_name = '../data/sfcc_2023_claims.json'
claim_handlers_file_name = '../data/sfcc_2023_claim_handlers.json'
disaster_file_name = '../data/sfcc_2023_disasters.json'

list_of_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
                  'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas',
                  'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
                  'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
                  'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
                  'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah',
                  'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

west = 'Alaska,Hawaii,Washington,Oregon,California,Montana,Idaho,Wyoming,Nevada,Utah,Colorado,Arizona,New Mexico'
midwest = 'North Dakota,South Dakota,Minnesota,Wisconsin,Michigan,Nebraska,Iowa,Illinois,Indiana,Ohio,Missouri,Kansas'
south = 'Oklahoma,Texas,Arkansas,Louisiana,Kentucky,Tennessee,Mississippi,Alabama,West Virginia,Virginia,North Carolina,South Carolina,Georgia,Florida'
northeast = 'Maryland,Delaware,District of Columbia,Pennsylvania,New York,New Jersey,Connecticut,Massachusetts,Vermont,New Hampshire,Rhode Island,Maine'


def read_json(file_name):
    with open(file_name, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def write_json(file_name, json_data):

    json_object = json.dumps(json_data, indent=4)

    with open(file_name, 'w', encoding='utf-8') as json_file:
        json_file.write(json_object)


def main():
    claims_data = read_json(claim_file_name)
    agents_data = read_json(agent_file_name)
    disasters_data = read_json(disaster_file_name)
    claim_handlers_data = read_json(claim_handlers_file_name)

    #     random_state = list_of_states[random.randint(0, 50)]
    #     aregion = 'broken'

    #     if random_state in west:
    #         aregion = 'West'
    #     elif random_state in midwest:
    #         aregion = "Midwest"
    #     elif random_state in south:
    #         aregion = "South"
    #     elif random_state in northeast:
    #         aregion = "Northeast"
    #     else:
    #         print(state, aregion)

    #     agent['state'] = random_state
    #     agent['region'] = aregion

    # write_json(agent_file_name, agents_data)

    # agents_by_state = {}

    # for agent in agents_data:
    #     agents_state = agent['state']

    #     if agents_state in agents_by_state:
    #         agents_by_state[agents_state].append(agent)
    #     else:
    #         agents_by_state[agents_state] = [agent]

    # Next assign claims to disasters and a random agent in that state

    for claim in claims_data:
        new_cost = round(claim['estimate_cost'] / 100 + random.random(), 2)
        claim['estimate_cost'] = new_cost
    #     disaster_id = claim['disaster_id']

    #     disaster = [
    #         disaster for disaster in disasters_data if disaster['fema_disaster_id'] == disaster_id
    #     ][0]

    #     disaster_state = disaster['state']

    #     num_agents_in_state = len(agents_by_state[disaster_state])
    #     random_agent_index = random.randint(0, num_agents_in_state - 1)
    #     selected_agent = agents_by_state[disaster_state][random_agent_index]

    #     del claim['agent_assigned']
    #     claim['agent_assigned_id'] = selected_agent['id']

    write_json(claim_file_name, claims_data)

    # claim_handlers_data = []
    # claim_handlers_counter = 1

    # for claim in claims_data:
    #     claim_handler_name = claim['claims_handler_assigned']

    #     if random.randint(1, 100) > 85:
    #         claim_handler_name_array = claim_handler_name.split(' ')
    #         claims_handler = {
    #             'first_name': claim_handler_name_array[0],
    #             'last_name': claim_handler_name_array[1],
    #             'id': claim_handlers_counter
    #         }
    #         claim_handlers_data.append(claims_handler)
    #         claim_handlers_counter += 1

    # write_json(claim_handlers_file_name, claim_handlers_data)

    # for claim in claims_data:
    #     claim_handler_index = random.randint(1, len(claim_handlers_data))

    #     claim['claim_handler_assigned_id'] = claim_handler_index

    # write_json(claim_file_name, claims_data)


main()
