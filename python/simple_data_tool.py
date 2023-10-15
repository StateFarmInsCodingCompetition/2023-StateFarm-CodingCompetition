import json
import math
import typing
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt

from statistics import mean



class SimpleDataTool:

    AGENTS_FILEPATH = 'data/sfcc_2023_agents.json'
    CLAIM_HANDLERS_FILEPATH = 'data/sfcc_2023_claim_handlers.json'
    CLAIMS_FILEPATH = 'data/sfcc_2023_claims.json'
    DISASTERS_FILEPATH = 'data/sfcc_2023_disasters.json'

    STATES = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
              'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
              'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
              'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey',
              'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
              'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah',
              'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
              ]

    REGION_MAP = {
        'west': 'Alaska,Hawaii,Washington,Oregon,California,Montana,Idaho,Wyoming,Nevada,Utah,Colorado,Arizona,New Mexico',
        'midwest': 'North Dakota,South Dakota,Minnesota,Wisconsin,Michigan,Nebraska,Iowa,Illinois,Indiana,Ohio,Missouri,Kansas',
        'south': 'Oklahoma,Texas,Arkansas,Louisiana,Kentucky,Tennessee,Mississippi,Alabama,West Virginia,Virginia,North Carolina,South Carolina,Georgia,Florida',
        'northeast': 'Maryland,Delaware,District of Columbia,Pennsylvania,New York,New Jersey,Connecticut,Massachusetts,Vermont,New Hampshire,Rhode Island,Maine'
    }

    def __init__(self):
        self.__agent_data = self.load_json_from_file(self.AGENTS_FILEPATH)
        self.__claim_handler_data = self.load_json_from_file(
            self.CLAIM_HANDLERS_FILEPATH)
        self.__claim_data = self.load_json_from_file(self.CLAIMS_FILEPATH)
        self.__disaster_data = self.load_json_from_file(
            self.DISASTERS_FILEPATH)

    # Helper Methods

    def load_json_from_file(self, filename):
        data = None

        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return data

    def get_agent_data(self):
        return self.__agent_data

    def get_claim_handler_data(self):
        return self.__claim_handler_data

    def get_disaster_data(self):
        return self.__disaster_data

    def get_claim_data(self):
        return self.__claim_data

    # Unit Test Methods

    # region Test Set One

    def get_num_closed_claims(self):
        # Holds the total number of claims that are closed
        num_closed = 0

        for claim in self.get_claim_data():
            if claim["status"] == "Closed":
                num_closed += 1

        return num_closed

    def get_num_claims_for_claim_handler_id(self, claim_handler_id):
        # Holds the total number of claims for a specific claim handler id
        num_claims = 0
        for claim in self.get_claim_data():
            if claim["claim_handler_assigned_id"] == claim_handler_id:
                num_claims += 1
        return num_claims

    def get_num_disasters_for_state(self, state):
        # Holds the total number of disasters in the given state
        num_disasters = 0

        for disaster in self.get_disaster_data():
            if disaster["state"] == state:
                num_disasters += 1

        return num_disasters

    # endregion

    # region Test Set Two

    def get_total_claim_cost_for_disaster(self, disaster_id):
        # Holds the total cost of claims with the disaster id
        total_cost = 0.0

        for claim in self.get_claim_data():
            if claim["disaster_id"] == disaster_id:
                total_cost += claim["estimate_cost"]

        # If there were no claims with that disaster id return None
        if total_cost == 0.0:
            return None
        return total_cost

    def get_average_claim_cost_for_claim_handler(self, claim_handler_id):
        num_claims = 0
        tot_claim_cost = 0.0

        for claim in self.get_claim_data():
            if claim["claim_handler_assigned_id"] == claim_handler_id:
                num_claims += 1
                tot_claim_cost += claim["estimate_cost"]

        if num_claims == 0:
            return None
        return round(tot_claim_cost/num_claims, 2)


    def get_state_with_most_disasters(self):
        disaster_dict = defaultdict(int)

        for disaster in self.get_disaster_data():
            disaster_dict[disaster["state"]] += 1

        # Default initiliazing if there are no disasters
        # (First alphabetical state, no disasters)
        max_state = "Alabama"   # State with most disasters
        max_disasters = 0       # Number of most disasters

        for state in self.STATES:
            if disaster_dict[state] > max_disasters:
                max_state = state
                max_disasters = disaster_dict[state]

        return max_state
            
    # Returns the name of the state with the least disasters provided the state has at least 1 disaster.
    # If multiple states have the same minimum number of disasters, the lexicographically smallest state is returned
    def get_state_with_least_disasters(self):

        # Key: (str) State name
        # Val: (int) Number of disasters of the state
        disaster_dict = defaultdict(int)

        for disaster in self.get_disaster_data():
            disaster_dict[disaster["state"]] += 1

        # Default initializing if there are no disasters
        # (First alphabetical state, no disasters)
        min_state = ""  # State with least disasters
        min_disasters = float('inf')  # Infinity

        for state in self.STATES:
            # If the state has 0 disasters, ignore the state
            if state not in disaster_dict:
                continue
            if disaster_dict[state] < min_disasters:
                min_state = state
                min_disasters = disaster_dict[state]

        # If no states are in the data
        if min_state == '':
            return None
        return min_state

    def get_most_spoken_agent_language_by_state(self, state):
        language_dict = defaultdict(int)

        for agent in self.get_agent_data():
            if agent["state"] == state:
                if not (agent["primary_language"] == "English" or agent["primary_language"] == None):
                    language_dict[agent["primary_language"]] += 1
                if not (agent["secondary_language"] == "English" or agent["secondary_language"] == None):
                    language_dict[agent["secondary_language"]] += 1
        
        max_language = ""
        max_agent = 0

        for language in language_dict.keys():
            if language_dict[language] > max_agent:
                max_language = language

        print(max_language)
        return max_language

    def get_num_of_open_claims_for_agent_and_severity(self, agent_id: int, min_severity_rating: int):

        # Checks if min_severity_rating is in bounds 1 to 10 inclusive
        if min_severity_rating < 1 or min_severity_rating > 10:
            return -1

        # Holds number of open claims for given agent that have at least min_severity_rating
        num_open_claims: int = 0

        # Iterates through claims, checking if agent_id matches, claim is not closed, and severity_rating matches
        for claim in self.get_claim_data():
            if claim['agent_assigned_id'] == agent_id:
                if claim['status'] != 'Closed':
                    if claim['severity_rating'] >= min_severity_rating:
                        num_open_claims += 1

        if num_open_claims == 0:
            return None

        return num_open_claims

    # endregion

    # region TestSetThree

    def get_num_disasters_declared_after_end_date(self):
        # Total number of disasters declared after end date
        num_disasters = 0
        
        for disaster in self.get_disaster_data():
            if disaster["declared_date"] > disaster["end_date"]:
                num_disasters += 1

        return num_disasters

    def build_map_of_agents_to_total_claim_cost(self):

        agents_to_total_claim_cost = {}

        for agent in self.get_agent_data():
            agents_to_total_claim_cost[agent['id']] = 0

        for claim in self.get_claim_data():
            agent_id = claim['agent_assigned_id']
            claim_cost = float(claim['estimate_cost'])

            # Check for invalid agent_id
            if agent_id not in agents_to_total_claim_cost:
                continue

            agents_to_total_claim_cost[agent_id] += claim_cost

        for agent in agents_to_total_claim_cost:
            agents_to_total_claim_cost[agent] = round(agents_to_total_claim_cost[agent],2)
        return agents_to_total_claim_cost


    def calculate_disaster_claim_density(self, disaster_id):
        area = 0
        radius = 0
        num_claims = 0

        for disaster in self.get_disaster_data():
            if disaster["id"] == disaster_id:
                radius = disaster["radius_miles"]

        if radius == 0:
            return None
        
        for claim in self.get_claim_data():
            if claim["disaster_id"] == disaster_id:
                num_claims += 1

        area = (math.pi * radius * radius)
        return round(num_claims/area, 5) # Instructions say to round to the thousanths place, 

    # endregion

    # region TestSetFour

    def get_top_three_months_with_highest_num_of_claims_desc(self):

        INT_MONTH_TO_STR_MONTH = {
            1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December'
        }

        disaster_to_date = {}
        for disaster in self.get_disaster_data():
            # Extract year, month and day from disaster
            [year, month, day] = [int(i) for i in disaster['declared_date'].split('-')]
            disaster_to_date[disaster['id']] = (year, month)

        date_to_cost = defaultdict(int)

        for claim in self.get_claim_data():
            disaster_id = claim['disaster_id']
            cost = claim['estimate_cost']
            date = disaster_to_date[disaster_id]
            date_to_cost[date] += cost

        dates_and_cost = []
        for date in date_to_cost:
            cost = date_to_cost[date]
            dates_and_cost.append((date, cost))
        dates_and_cost.sort(key=lambda x: x[1], reverse=True)

        top_three_months = []
        print(dates_and_cost)
        for i in range(3):
            date = dates_and_cost[i][0]
            year, month = date
            month_and_year = INT_MONTH_TO_STR_MONTH[month] + ' ' + str(year)
            top_three_months.append(month_and_year)
        return top_three_months
# endregion