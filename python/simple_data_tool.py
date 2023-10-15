import json
import math

from statistics import mean
from datetime import datetime, timedelta




class SimpleDataTool:

    AGENTS_FILEPATH = 'data/sfcc_2023_agents.json'
    CLAIM_HANDLERS_FILEPATH = 'data/sfcc_2023_claim_handlers.json'
    CLAIMS_FILEPATH = 'data/sfcc_2023_claims.json'
    DISASTERS_FILEPATH = 'data/sfcc_2023_disasters.json'

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
        """Calculates the number of claims where that status is "Closed"

        Returns:
            int: number of closed claims
        """
        closed_claims = 0
        
        for object in self.get_claim_data():
            if object["status"] == "Closed":
                closed_claims += 1

        return closed_claims
        pass

    def get_num_claims_for_claim_handler_id(self, claim_handler_id):
        """Calculates the number of claims assigned to a specific claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            int: number of claims assigned to claim handler
        """
        
        claims_assigned = 0
        
        for object in self.get_claim_data():
            if object["claim_handler_assigned_id"] == claim_handler_id:
                claims_assigned += 1
        return claims_assigned
        pass

    def get_num_disasters_for_state(self, state):
        """Calculates the number of disasters for a specific state

        Args:
            state (string): name of a state in the United States of America,
                            including the District of Columbia

        Returns:
            int: number of disasters for state
        """
        
        state_disasters = 0
        
        for object in self.get_disaster_data():
            if object["state"] == state:
                state_disasters += 1
        return state_disasters
        pass

    # endregion

    # region Test Set Two

    def get_total_claim_cost_for_disaster(self, disaster_id):
        """Sums the estimated cost of a specific disaster by its claims

        Args:
            disaster_id (int): id of disaster

        Returns:
            float | None: estimate cost of disaster, rounded to the nearest hundredths place
                          returns None if no claims are found
        """
        
        damage_costs = 0
        
        for object in self.get_claim_data():
            if object["disaster_id"] == disaster_id:
                damage_costs += object["estimate_cost"]
                
        if damage_costs == 0: return None
        return damage_costs
        pass

    def get_average_claim_cost_for_claim_handler(self, claim_handler_id):
        """Gets the average estimated cost of all claims assigned to a claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            float | None : average cost of claims, rounded to the nearest hundredths place
                           or None if no claims are found
        """
        
        total_cost = 0
        num_claims = 0
        
        for object in self.get_claim_data():
            if object["claim_handler_assigned_id"] == claim_handler_id:
                total_cost += object["estimate_cost"]
                num_claims += 1
                
        if num_claims == 0: return None
        return round(total_cost / num_claims, 2)
        pass

    def get_state_with_most_disasters(self):
        """Returns the name of the state with the most disasters based on disaster data

        If two states have the same number of disasters, then sort by alphabetical (a-z)
        and take the first.

        Example: Say New Jersey and Delaware both have the highest number of disasters at
                 12 disasters each. Then, this method would return "Delaware" since "D"
                 comes before "N" in the alphabet. 

        Returns:
            string: single name of state
        """
        d = {}
        disaster_count = 0
        state = ""
        states = []
        
        # count the amount of disasters occured per state
        for object in self.get_disaster_data():
            if object["state"] in d:
                d[object["state"]] += 1
            else:
                d[object["state"]] = 1
                
        
        
        # find the highest amount of disasters recorded
        for key, value in d.items():
            if value > disaster_count:
                disaster_count = value
                state = key
                
        states.append(state)
        print(state)
        
        # if multiple states contain same amount, we add to list, sort, and return first
        for key, value in d.items():
            if value == disaster_count and key != state:
                states.append(key)
        
        if len(states) > 1: states.sort()
        return states[0]
        pass

    def get_state_with_least_disasters(self):
        """Returns the name of the state with the least disasters based on disaster data

        If two states have the same number of disasters, then sort by alphabetical (a-z)
        and take the first.

        Example: Say New Mexico and West Virginia both have the least number of disasters at
                 1 disaster each. Then, this method would return "New Mexico" since "N"
                 comes before "W" in the alphabet. 

        Returns:
            string: single name of state
        """
        d = {}
        disaster_count = 100000
        state = ""
        states = []
        
        # count the amount of disasters occured per state
        for object in self.get_disaster_data():
            if object["state"] in d:
                d[object["state"]] += 1
            else:
                d[object["state"]] = 1
                
        
        
        # find the least amount of disasters recorded
        for key, value in d.items():
            if value < disaster_count:
                disaster_count = value
                state = key
                
        states.append(state)
        print(state)
        
        # if multiple states contain same amount, we add to list, sort, and return first
        for key, value in d.items():
            if value == disaster_count and key != state:
                states.append(key)
        
        if len(states) > 1: states.sort()
        return states[0]
        pass
    
    def get_most_spoken_agent_language_by_state(self, state):
        """Returns the name of the most spoken language by agents (besides English) for a specific state

        Args:
            state (string): name of state

        Returns:
            string: name of language
                    or empty string if state doesn't exist
        """
        
        most_spoken_languages = {}
        count = 0
        language = ""
        
        for object in self.get_agent_data():
            if object["state"] == state:
                
                # primary spoken language that is not english
                if object["primary_language"] != "English":
                    if object["primary_language"] in most_spoken_languages:
                        most_spoken_languages[object["primary_language"]] += 1
                    else:
                        most_spoken_languages[object["primary_language"]] = 1
                
                # secondary spoken language that is not english
                if object["secondary_language"] != "English":
                    if object["secondary_language"] in most_spoken_languages:
                        most_spoken_languages[object["secondary_language"]] += 1
                    else:
                        most_spoken_languages[object["secondary_language"]] = 1
                        
                        
        for key, value in most_spoken_languages.items():
            if value > count:
                count = value
                language = key
                
        return language
        pass

    def get_num_of_open_claims_for_agent_and_severity(self, agent_id, min_severity_rating):
        """Returns the number of open claims for a specific agent and for a minimum severity level and higher

        Note: Severity rating scale for claims is 1 to 10, inclusive.
        
        Args:
            agent_id (int): ID of the agent
            min_severity_rating (int): minimum claim severity rating

        Returns:
            int | None: number of claims that are not closed and have minimum severity rating or greater
                        -1 if severity rating out of bounds
                        None if agent does not exist, or agent has no claims (open or not)
        """
        
        if min_severity_rating < 1 or min_severity_rating > 10: return -1
        agent_exists = False
        open_claims = 0
        total_claims = 0
        
        for object in self.get_claim_data():
            
            # calculate open claims under restriction
            if object["agent_assigned_id"] == agent_id and object["severity_rating"] >= min_severity_rating and object["status"] != "Closed":
                agent_exists = True
                open_claims += 1
            
            # calculate total claims no restriction
            if object["agent_assigned_id"] == agent_id:
                total_claims += 1
        
        if agent_exists == False: return None
        if total_claims == 0: return None
        return open_claims
        pass

    # endregion

    # region TestSetThree

    def get_num_disasters_declared_after_end_date(self):
        """Gets the number of disasters where it was declared after it ended

        Returns:
            int: number of disasters where the declared date is after the end date
        """
        
        total = 0
        
        for object in self.get_disaster_data():
            end_date = object["end_date"].split("-")
            end_date_ref = datetime(int(end_date[0]), int(end_date[1]), int(end_date[2]))
            
            declared_date = object["declared_date"].split("-")
            declared_date_ref = datetime(int(declared_date[0]), int(declared_date[1]), int(declared_date[2]))
            
            if declared_date_ref > end_date_ref: total += 1
            
            
        return total
        pass

    def build_map_of_agents_to_total_claim_cost(self):
        """Builds a map of agent and their total claim cost

        Hints:
            An agent with no claims should return 0
            Invalid agent id should have a value of None
            You should round your total_claim_cost to the nearest hundredths

        Returns:
            dict: key is agent id, value is total cost of claims associated to the agent
        """
        
        agents_costs = {}
        
        # setup map with agents
        for object in self.get_agent_data():
            agents_costs[object["id"]] = 0
            
        # sum up agent costs. if not found, set to none
        for object in self.get_claim_data():
            if object["agent_assigned_id"] in agents_costs:
                agents_costs[object["agent_assigned_id"]] += object["estimate_cost"]
            else:
                agents_costs[object["agent_assigned_id"]] = None
        
        # round all sums
        for key, value in agents_costs.items():
            agents_costs[key] = round(value, 2)
                
        return agents_costs
        pass

    def calculate_disaster_claim_density(self, disaster_id):
        """Calculates density of a diaster based on the number of claims and impact radius

        Hints:
            Assume uniform spacing between claims
            Assume disaster impact area is a circle

        Args:
            disaster_id (int): id of diaster

        Returns:
            float: density of claims to disaster area, rounded to the nearest thousandths place
                   None if disaster does not exist
        """
        disaster = next((d for d in self.get_disaster_data() if d['id'] == disaster_id), None)
        if not disaster: return None
        
        radius = disaster['radius_miles']
        
        claims = [claim for claim in self.get_claim_data() if claim['disaster_id'] == disaster_id]

        density = len(claims) / (math.pi * radius**2)

        density_rounded = round(density, 5)

        return density_rounded
        pass

    # endregion

    # region TestSetFour

    def get_top_three_months_with_highest_num_of_claims_desc(self):
        """Gets the top three months with the highest total claim cost

        Hint:
            Month should be full name like 01 is January and 12 is December
            Year should be full four-digit year
            List should be in descending order

        Returns:
            list: three strings of month and year, descending order of highest claims
        """
        
        def custom_sort(item):
            month, year = item.split()
            return (int(year), month_order[month])
        
        month_order = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,"July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}
        
        total_claim_by_month = {}

        # Iterate through the claims data
        for claim in self.get_claim_data():
            disaster_id = claim.get("disaster_id")
            hazard = next((h for h in self.get_disaster_data() if h.get("id") == disaster_id), None)

            if hazard:
                start_date = datetime.strptime(hazard["start_date"], "%Y-%m-%d")
                month_year_key = start_date.strftime("%m-%Y")
                total_claim_by_month[month_year_key] = total_claim_by_month.get(month_year_key, 0) + claim["estimate_cost"]

        sorted_months = sorted(total_claim_by_month.items(), key=lambda x: (x[1], datetime.strptime(x[0], "%m-%Y")), reverse=True)
        top_three_months = sorted_months[:3]
        result = [datetime.strptime(month_year, "%m-%Y").strftime("%B %Y") for month_year, _ in top_three_months]
        print(sorted(result, key=custom_sort, reverse=True))
        
        return sorted(result, key=custom_sort, reverse=True)
        pass

    # endregion