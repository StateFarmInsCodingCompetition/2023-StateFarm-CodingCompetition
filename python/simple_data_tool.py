import json
import math
import helpers

from statistics import mean

class SimpleDataTool:

    AGENTS_FILEPATH = 'python/data/sfcc_2023_agents.json'
    CLAIM_HANDLERS_FILEPATH = 'python/data/sfcc_2023_claim_handlers.json'
    CLAIMS_FILEPATH = 'python/data/sfcc_2023_claims.json'
    DISASTERS_FILEPATH = 'python/data/sfcc_2023_disasters.json'

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
        return helpers.counter(self.get_claim_data(), "status", "Closed")

    def get_num_claims_for_claim_handler_id(self, claim_handler_id):
        """Calculates the number of claims assigned to a specific claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            int: number of claims assigned to claim handler
        """
        return helpers.counter(self.get_claim_data(), "claim_handler_assigned_id", claim_handler_id)

    def get_num_disasters_for_state(self, state):
        """Calculates the number of disasters for a specific state

        Args:
            state (string): name of a state in the United States of America,
                            including the District of Columbia

        Returns:
            int: number of disasters for state
        """
        return helpers.counter(self.get_disaster_data(), "state", state)

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
        return helpers.totaler(self.get_claim_data(), "disaster_id", disaster_id, "estimate_cost") or None

    def get_average_claim_cost_for_claim_handler(self, claim_handler_id):
        """Gets the average estimated cost of all claims assigned to a claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            float | None : average cost of claims, rounded to the nearest hundredths place
                           or None if no claims are found
        """
        total_cost = helpers.totaler(self.get_claim_data(), "claim_handler_assigned_id", claim_handler_id, "estimate_cost")
        count = helpers.counter(self.get_claim_data(), "claim_handler_assigned_id", claim_handler_id)
        if total_cost == 0 or count == 0:
            return None
        return round(total_cost/count, 2)

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
        state_to_disaster = helpers.map_counter(self.get_disaster_data(), "state")
        return helpers.max_map_alphabetically(state_to_disaster)

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
        state_to_disaster = helpers.map_counter(self.get_disaster_data(), "state")
        return helpers.min_map_alphabetically(state_to_disaster)
    
    def get_most_spoken_agent_language_by_state(self, state):
        """Returns the name of the most spoken language by agents (besides English) for a specific state

        Args:
            state (string): name of state

        Returns:
            string: name of language
                    or empty string if state doesn't exist
        """
        language_map = {}
        def increment_langauge(language):
            if language != "English":
                language_map[language] = language_map.get(language, 0) + 1
        for agent in self.get_agent_data():
            if agent["state"] == state:
                increment_langauge(agent["primary_language"])
                increment_langauge(agent["secondary_language"])
        if len(language_map) == 0:
            return ""
        return helpers.max_map_alphabetically(language_map)
        

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
        if min_severity_rating < 1 or min_severity_rating > 10:
            return -1
        count = 0
        for claim in self.get_claim_data():
            if claim["agent_assigned_id"] == agent_id and claim["status"] != "Closed":
                if claim["severity_rating"] >= min_severity_rating:
                    count += 1
        return count or None

    # endregion

    # region TestSetThree

    def get_num_disasters_declared_after_end_date(self):
        """Gets the number of disasters where it was declared after it ended

        Returns:
            int: number of disasters where the declared date is after the end date
        """
        def declared_exceeds_end(disaster):
            return helpers.date_to_datetime(disaster["declared_date"]) > helpers.date_to_datetime(disaster["end_date"])
        count = 0
        for disaster in self.get_disaster_data():
            if declared_exceeds_end(disaster):
                count += 1
        return count

    def build_map_of_agents_to_total_claim_cost(self):
        """Builds a map of agent and their total claim cost

        Hints:
            An agent with no claims should return 0
            Invalid agent id should have a value of None
            You should round your total_claim_cost to the nearest hundredths

        Returns:
            dict: key is agent id, value is total cost of claims associated to the agent
        """
        agent_to_cost = {}
        for agent in self.get_agent_data():
            agent_to_cost[agent["id"]] = 0
        for claim in self.get_claim_data():
            agent_to_cost[claim["agent_assigned_id"]] += claim["estimate_cost"]
        for id in list(agent_to_cost.keys()):
            agent_to_cost[id] = round(agent_to_cost[id],2)
        return agent_to_cost

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
        disaster_area = None
        for disaster in self.get_disaster_data():
            if disaster["id"] == disaster_id:
                disaster_area = math.pi*(disaster["radius_miles"]**2)
        if disaster_area == None:
            return None
        return round(helpers.counter(self.get_claim_data(), "disaster_id", disaster_id)/disaster_area, 5)

    # endregion

    # region TestSetFour

    def get_top_three_months_with_highest_num_of_claims_desc(self):
        """Gets the top three months with the highest number of claims

        OPTIONAL! OPTIONAL! OPTIONAL!
        AS OF 9:21CDT, TEST IS OPTIONAL. SEE GITHUB ISSUE #8 FOR MORE DETAILS

        Hint:
            Month should be full name like 01 is January and 12 is December
            Year should be full four-digit year
            List should be in descending order

        Returns:
            list: three strings of month and year, descending order of highest claims
        """
        def format_date(date):
            return helpers.date_to_datetime(date).strftime("%B %Y")
        disaster_to_month = {}
        for disaster in self.get_disaster_data():
            disaster_to_month[disaster["id"]] = format_date(disaster["declared_date"])
        month_to_claims = {}
        for claim in self.get_claim_data():
            month = disaster_to_month[claim["disaster_id"]]
            month_to_claims[month] = month_to_claims.get(month, 0) + 1
        months = list(month_to_claims.keys())
        months.sort(key=(lambda month : month_to_claims[month]), reverse=True)
        return months[:3]

    # endregion
