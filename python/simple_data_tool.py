import json
import math

from statistics import mean
from datetime import datetime


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
        # Get the claims.json file
        claim_data = self.get_claim_data()
        # Set the number of closed claims to 0
        num_closed_claim = 0
        # Access through each item in json file
        for i in claim_data:
            ''' Add 1 to the number of closed claims
                if status of the claim is "Closed" in the item'''
            if i["status"] == "Closed":
                num_closed_claim += 1
        return num_closed_claim

    def get_num_claims_for_claim_handler_id(self, claim_handler_id):
        """Calculates the number of claims assigned to a specific claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            int: number of claims assigned to claim handler
        """
        # Get the claims.json file
        claim_data = self.get_claim_data()
        # Set the number of claims assigned to a specific claim handler id to 0
        num_claims_for_ch_id = 0
        # Access through each item in json file
        for i in claim_data:
            ''' Add 1 to the number of claims assigned to the claim handler
                if the claim handler id in the argument is the same as the 
                claim handler id in the item'''
            if i["claim_handler_assigned_id"] == claim_handler_id:
                num_claims_for_ch_id += 1
        return num_claims_for_ch_id

    def get_num_disasters_for_state(self, state):
        """Calculates the number of disasters for a specific state

        Args:
            state (string): name of a state in the United States of America,
                            including the District of Columbia

        Returns:
            int: number of disasters for state
        """
        # Get the disaster.json file
        disaster_data = self.get_disaster_data()
        # Set the number of disasters for state to 0
        num_disaster_for_state = 0
        # Access through each item in json file
        for i in disaster_data:
            ''' Add 1 to the number of disasters for state
                if the state in the argument is the same as the 
                state in the item'''
            if i["state"] == state:
                num_disaster_for_state += 1
        return num_disaster_for_state

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
        # Get the claim.json file
        claim_data = self.get_claim_data()
        # Set the total cost of a specific disaster to 0
        total_claim_cost = 0
        # Access through each item in json file
        for i in claim_data:
            ''' If the disaster in the argument is the same as the 
                disaster id in the item,
                add the estimate cost of the disaster id to the total cost
                '''
            if i["disaster_id"] == disaster_id:
                total_claim_cost += i["estimate_cost"]
        '''Return the total cost rounded to the nearest hundredths 
           if total cost is greater than 0
           Return None if the total cost is 0'''
        if total_claim_cost > 0:
            return round(total_claim_cost, 2)
        else:
            return None
        

    def get_average_claim_cost_for_claim_handler(self, claim_handler_id):
        """Gets the average estimated cost of all claims assigned to a claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            float | None : average cost of claims, rounded to the nearest hundredths place
                           or None if no claims are found
        """
        # Get the claim.json file
        claim_data = self.get_claim_data()
        # Create an array of cost for the specific claim_handler_id
        cost = []
        # Access through each item in json file
        for i in claim_data:
            '''Add the estimate cost of each claim to the cost array
               if the claim handler id in the argument is the same as
               the claim handler id in the item'''
            if i["claim_handler_assigned_id"] == claim_handler_id:
                cost.append(i["estimate_cost"])
        '''If any claim is found, find the mean of the cost array and return
           the mean rounded to the nearest hundredths place
           If no claims are found, return None'''
        if len(cost) > 0:
            average_cost = mean(cost)
            return round(average_cost, 2)
        else:
            return None
        

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
        disaster_data = self.get_disaster_data()
        states = []
        for i in disaster_data:
            states.append(i["state"])
        states_with_count = {}
        for state in states:
            if state in states_with_count:
                states_with_count[state] += 1
            else:
                states_with_count[state] = 1
        sorted_states = dict(sorted(states_with_count.items()))
        return max(sorted_states, key=sorted_states.get)

   
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
        disaster_data = self.get_disaster_data()
        states = []
        for i in disaster_data:
            states.append(i["state"])
        states_with_count = {}
        for state in states:
            if state in states_with_count:
                states_with_count[state] += 1
            else:
                states_with_count[state] = 1
        sorted_states = dict(sorted(states_with_count.items()))
        return min(sorted_states, key=sorted_states.get)

    
    def get_most_spoken_agent_language_by_state(self, state):
        """Returns the name of the most spoken language by agents (besides English) for a specific state

        Args:
            state (string): name of state

        Returns:
            string: name of language
                    or empty string if state doesn't exist
        """
        agent_data = self.get_agent_data()
        languages = []
        for i in agent_data:
            if i["state"] == state:
                languages.append(i["secondary_language"])
        languages_with_count = {}
        for language in languages:
            if language in languages_with_count:
                languages_with_count[language] += 1
            else:
                languages_with_count[language] = 1
        sorted_languages = dict(sorted(languages_with_count.items()))
        if len(languages) > 0:
            return max(sorted_languages, key=sorted_languages.get)
        else:
            return ""

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
        claim_data = self.get_claim_data()
        num_open_claims = 0
        if min_severity_rating >= 1 & min_severity_rating <= 10:
            for i in claim_data:
                if i["agent_assigned_id"] == agent_id & i["severity_rating"] >= min_severity_rating & i["status"] != "Closed":
                    num_open_claims += 1
        else:
            num_open_claims = -1
        if num_open_claims != 0:
            return num_open_claims
        else:
            return None

    # endregion

    # region TestSetThree

    def get_num_disasters_declared_after_end_date(self):
        """Gets the number of disasters where it was declared after it ended

        Returns:
            int: number of disasters where the declared date is after the end date
        """
        disaster_data = self.get_disaster_data()
        num_disasters = 0
        for i in disaster_data:
            end_date = datetime.strptime(i["end_date"], "%Y-%m-%d")
            declared_date = datetime.strptime(i["declared_date"], "%Y-%m-%d")
            if declared_date > end_date:
                num_disasters += 1
        return num_disasters
        

    def build_map_of_agents_to_total_claim_cost(self):
        """Builds a map of agent and their total claim cost

        Hints:
            An agent with no claims should return 0
            Invalid agent id should have a value of None
            You should round your total_claim_cost to the nearest hundredths

        Returns:
            dict: key is agent id, value is total cost of claims associated to the agent
        """

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

        pass

    # endregion

