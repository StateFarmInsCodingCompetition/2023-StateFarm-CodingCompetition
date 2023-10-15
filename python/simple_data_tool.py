import json
import math

from statistics import mean



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
        closed_claim_counter = 0
        claim_data = self.get_claim_data(self)
        for claim in claim_data:  
            if claim.status == "Closed":
                closed_claim_counter+= 1 
        
        return closed_claim_counter

    def get_num_claims_for_claim_handler_id(self, claim_handler_id):
        """Calculates the number of claims assigned to a specific claim handler
        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            int: number of claims assigned to claim handler
        """
        claim_data = self.get_claim_data(self)
        num_claim_to_handler = 0
        for claim in claim_data:
            if claim.claim_handler_assigned_id == claim_handler_id:
                num_claim_to_handler += 1
        return num_claim_to_handler

    def get_num_disasters_for_state(self, state):
        """Calculates the number of disasters for a specific state

        Args:
            state (string): name of a state in the United States of America,
                            including the District of Columbia

        Returns:
            int: number of disasters for state
        """

        disasters = self.get_disaster_data(self)
        num_disaster_of_state = 0
        for disaster in disasters:
            if disaster.state == state:
                num_disaster_of_state += 1
        return num_disaster_of_state

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
        claims = self.get_claim_data()
        claims_by_disaster_id = filter(lambda claim: claim["disaster_id"] == disaster_id, claims)
        if len(list(claims_by_disaster_id)) == 0: return None
        total_claim = 0
        for item in claims_by_disaster_id:
            total_claim += item["estimate_cost"]
        return round(total_claim, 2)
        
    def get_average_claim_cost_for_claim_handler(self, claim_handler_id):
        """Gets the average estimated cost of all claims assigned to a claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            float | None : average cost of claims, rounded to the nearest hundredths place
                           or None if no claims are found
        """
        claims = self.get_claim_data()
        claims_by_handler_id = filter(lambda claim: claim["claim_handler_assigned_id"] == claim_handler_id, claims)
        if len(list(claims_by_handler_id)) == 0: return None
        all_costs = [item["estimate_cost"] for item in claims_by_handler_id]
        return round(mean(all_costs), 2)

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
        disasters = self.get_disaster_data()
        hash_state_disaster_count = {}
        for d in disasters:
            if d["state"] not in hash_state_disaster_count:
                hash_state_disaster_count[d["state"]] = 1
            hash_state_disaster_count[d["state"]] += 1
        hash_state_disaster_count = dict(sorted(hash_state_disaster_count.items(), key=lambda item: item[0]))
        key_with_max_value = max(hash_state_disaster_count, key=hash_state_disaster_count.get)
        return key_with_max_value

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
        disasters = self.get_disaster_data()
        hash_state_disaster_count = {}
        for d in disasters:
            if d["state"] not in hash_state_disaster_count:
                hash_state_disaster_count[d["state"]] = 1
            hash_state_disaster_count[d["state"]] += 1
        hash_state_disaster_count = dict(sorted(hash_state_disaster_count.items(), key=lambda item: item[0]))
        key_with_min_value = min(hash_state_disaster_count, key=hash_state_disaster_count.get)
        return key_with_min_value
    
    def get_most_spoken_agent_language_by_state(self, state):
        """Returns the name of the most spoken language by agents (besides English) for a specific state

        Args:
            state (string): name of state

        Returns:
            string: name of language
                    or empty string if state doesn't exist
        """
        agents = self.get_agent_data()
        agents_by_state = filter(lambda agent: agent["state"] == state, agents)
        hash_agents_count_by_lang = {}
        for agent in agents_by_state:
            if agent["secondary_language"] not in hash_agents_count_by_lang:
                hash_agents_count_by_lang[agent["secondary_language"]] = 1
            hash_agents_count_by_lang[agent["secondary_language"]] += 1

        hash_agents_count_by_lang = dict(sorted(hash_agents_count_by_lang.items(), key=lambda item: item[0]))
        if hash_agents_count_by_lang == {}: return ''
        key_with_max_value = max(hash_agents_count_by_lang, key=hash_agents_count_by_lang.get)
        return key_with_max_value

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
        if min_severity_rating < 1 and min_severity_rating > 10: return -1
        claims = self.get_claim_data()
        claims_by_agent_id = filter(lambda claim: claim["claim_handler_assigned_id"] == agent_id, claims)
        if len(list(claims_by_agent_id)) == 0: return None
        open_claim_count = 0
        for claim in claims_by_agent_id:
            if claim["status"] != "Closed" and claim["severity_rating"] >= min_severity_rating:
                open_claim_count += 1
        return open_claim_count

    # endregion

    # region TestSetThree

    def get_num_disasters_declared_after_end_date(self):
        """Gets the number of disasters where it was declared after it ended

        Returns:
            int: number of disasters where the declared date is after the end date
        """

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
        
        agent_claim_cost = {}

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

test_class = SimpleDataTool()
# print(test_class.get_total_claim_cost_for_disaster(0))
# print(test_class.get_average_claim_cost_for_claim_handler(2))
# print(test_class.get_state_with_most_disasters())
# print(test_class.get_state_with_least_disasters())
# print(test_class.get_most_spoken_agent_language_by_state("Wisconsin"))
print(test_class.get_num_of_open_claims_for_agent_and_severity(24, 1))


