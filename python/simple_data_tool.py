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
        count = 0
        for claim in self.__claim_data:
            if (claim["status"] == "Closed"):
                count += 1
        return count


    def get_num_claims_for_claim_handler_id(self, claim_handler_id):
        """Calculates the number of claims assigned to a specific claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            int: number of claims assigned to claim handler
        """
        count = 0
        for claim in self.__claim_data:
            if (claim["claim_handler_assigned_id"] == claim_handler_id):
                count += 1
        return count

    def get_num_disasters_for_state(self, state):
        """Calculates the number of disasters for a specific state

        Args:
            state (string): name of a state in the United States of America,
                            including the District of Columbia

        Returns:
            int: number of disasters for state
        """
        count = 0
        for disaster in self.__disaster_data:
            if (disaster["state"] == state):
                count += 1
        return count

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

        sum = 0
        for claim in self.__claim_data:
            if (claim["disaster_id"] == disaster_id):
                sum += (claim["estimate_cost"])
        return sum or None

    def get_average_claim_cost_for_claim_handler(self, claim_handler_id):
        """Gets the average estimated cost of all claims assigned to a claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            float | None : average cost of claims, rounded to the nearest hundredths place
                           or None if no claims are found
        """

        sum = 0
        count = 0
        for claim in self.__claim_data:
            if (claim["claim_handler_assigned_id"] == claim_handler_id):
                sum += (claim["estimate_cost"])
                count += 1
        return round(sum / count, 2) if count else None

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
        states = [disaster["state"] for disaster in self.__disaster_data]
        return min(set(states), key=lambda x:(0 - states.count(x), x))


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
        states = [disaster["state"] for disaster in self.__disaster_data]
        return min(set(states), key=lambda x: (states.count(x), x))
    
    def get_most_spoken_agent_language_by_state(self, state):
        """Returns the name of the most spoken language by agents (besides English) for a specific state

        Args:
            state (string): name of state

        Returns:
            string: name of language
                    or empty string if state doesn't exist
        """
        languages = [agent["secondary_language"] for agent in self.__agent_data\
                     if (agent["secondary_language"] and agent["state"] == state)]
        return min(set(languages), key=lambda x: (0 - languages.count(x), x)) if languages else ""

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
        count = 0
        if min_severity_rating > 10 or min_severity_rating < 1:
            return -1
        for claim in self.__claim_data:
            if (claim["agent_assigned_id"] == agent_id)\
                    and (claim["severity_rating"] >= min_severity_rating)\
                    and claim["status"] != "Closed":
                count += 1
        return count or None

    # endregion

    # region TestSetThree

    def get_num_disasters_declared_after_end_date(self):
        """Gets the number of disasters where it was declared after it ended

        Returns:
            int: number of disasters where the declared date is after the end date
        """
        count = 0
        for disaster in self.__disaster_data:
            if (disaster["end_date"] < disaster["declared_date"]):
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
        map = dict((agent["id"], 0) for agent in self.__agent_data if agent["id"])
        for claim in self.__claim_data:
            map[claim["agent_assigned_id"]] \
                = round(map[claim["agent_assigned_id"]] + claim["estimate_cost"], 2)
        return map

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
        for disaster in self.__disaster_data:
            if disaster["id"] == disaster_id:
                return round(len([claim for claim in self.__claim_data
                            if claim["disaster_id"] == disaster_id])\
                                 / (math.pi * disaster["radius_miles"] ** 2), 5) or None
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
        def get_num_claims_for_disaster(disaster_id):
            count = 0
            for claim in self.__claim_data:
                if (claim["disaster_id"] == disaster_id):
                    count += 1
            return count
        months = {}
        for disaster in self.__disaster_data:
            count = get_num_claims_for_disaster(disaster["id"])
            months[disaster["declared_date"][0:7]] = months.get(disaster["declared_date"][0:7], 0) + count
        values = list(set(months.values()))
        values.sort(reverse=True)
        for v in values:
            v = 
        top = next(k for k, v in months.items() if v == values[0])
        second = next(k for k, v in months.items() if v == values[1])
        third = next(k for k, v in months.items() if v == values[2])
        return [top, second, third]
    # endregion
