import json
import math

from statistics import mean


class SimpleDataTool:
    AGENTS_FILEPATH = "../round 1/sfcc_2023_agents.json"
    CLAIM_HANDLERS_FILEPATH = "../round 1/sfcc_2023_claim_handlers.json"
    CLAIMS_FILEPATH = "../round 1/sfcc_2023_claims.json"
    DISASTERS_FILEPATH = "../round 1/sfcc_2023_disasters.json"

    REGION_MAP = {
        "west": "Alaska,Hawaii,Washington,Oregon,California,Montana,Idaho,Wyoming,Nevada,Utah,Colorado,Arizona,New Mexico",
        "midwest": "North Dakota,South Dakota,Minnesota,Wisconsin,Michigan,Nebraska,Iowa,Illinois,Indiana,Ohio,Missouri,Kansas",
        "south": "Oklahoma,Texas,Arkansas,Louisiana,Kentucky,Tennessee,Mississippi,Alabama,West Virginia,Virginia,North Carolina,South Carolina,Georgia,Florida",
        "northeast": "Maryland,Delaware,District of Columbia,Pennsylvania,New York,New Jersey,Connecticut,Massachusetts,Vermont,New Hampshire,Rhode Island,Maine",
    }

    def __init__(self):
        self.__agent_data = self.load_json_from_file(self.AGENTS_FILEPATH)
        self.__claim_handler_data = self.load_json_from_file(
            self.CLAIM_HANDLERS_FILEPATH
        )
        self.__claim_data = self.load_json_from_file(self.CLAIMS_FILEPATH)
        self.__disaster_data = self.load_json_from_file(self.DISASTERS_FILEPATH)

    # Helper Methods

    def load_json_from_file(self, filename):
        data = None

        with open(filename, "r", encoding="utf-8") as file:
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
        return sum([claim["status"] == "Closed" for claim in self.__claim_data])

    def get_num_claims_for_claim_handler_id(self, claim_handler_id):
        """Calculates the number of claims assigned to a specific claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            int: number of claims assigned to claim handler
        """
        return sum(
            [
                claim["claim_handler_assigned_id"] == claim_handler_id
                for claim in self.__claim_data
            ]
        )

    def get_num_disasters_for_state(self, state):
        """Calculates the number of disasters for a specific state

        Args:
            state (string): name of a state in the United States of America,
                            including the District of Columbia

        Returns:
            int: number of disasters for state
        """
        return sum([disaster["state"] == state for disaster in self.__disaster_data])

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
        if not any(claim["disaster_id"] == disaster_id for claim in self.__claim_data):
            return None

        return sum(
            [
                claim["estimate_cost"]
                for claim in self.__claim_data
                if claim["disaster_id"] == disaster_id
            ]
        )

    def get_average_claim_cost_for_claim_handler(self, claim_handler_id):
        """Gets the average estimated cost of all claims assigned to a claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            float | None : average cost of claims, rounded to the nearest hundredths place
                           or None if no claims are found
        """
        if not any(
            claim["claim_handler_assigned_id"] == claim_handler_id
            for claim in self.__claim_data
        ):
            return None

        average_cost = mean(
            claim["estimate_cost"]
            for claim in self.__claim_data
            if claim["claim_handler_assigned_id"] == claim_handler_id
        )
        return round(average_cost, 2)

    def _dict_argmax(self, d):
        max_key = None
        max_value = -1e99

        for key, val in d.items():
            if val > max_value:
                max_value = val
                max_key = key
            elif val == max_value:
                max_key = min(max_key, key)
        return max_key
    
    def _dict_argmin(self, d):
        min_key = None
        min_value = 1e99

        for key, val in d.items():
            if val < min_value:
                min_value = val
                min_key = key
            elif val == min_value:
                min_key = min(min_key, key)
        return min_key

    def val_in_range(val, start, stop):
        return val > start and val < stop

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
        num_disasters = {}
        for disaster in self.__disaster_data:
            state = disaster["state"]
            num_disasters[state] = num_disasters.get(state, 0) + 1
        
        return self._dict_argmax(num_disasters)

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
        num_disasters = {}
        for disaster in self.__disaster_data:
            state = disaster["state"]
            num_disasters[state] = num_disasters.get(state, 0) + 1
        
        return self._dict_argmin(num_disasters)

    def get_most_spoken_agent_language_by_state(self, state):
        """Returns the name of the most spoken language by agents (besides English) for a specific state

        Args:
            state (string): name of state

        Returns:
            string: name of language
                    or empty string if state doesn't exist
        """
        if not any(agent["state"] == state for agent in self.__agent_data):
            return ""

        language_counts = {}
        for agent in self.__agent_data:
            if agent["state"] != state:
                continue

            primary_language = agent["primary_language"]
            secondary_language = agent["secondary_language"]

            language_counts[primary_language]   = language_counts.get(primary_language, 0)   + 1
            language_counts[secondary_language] = language_counts.get(secondary_language, 0) + 1

        if "English" in language_counts:
            del language_counts["English"]
             
        return self._dict_argmax(language_counts)

    def get_num_of_open_claims_for_agent_and_severity(
        self, agent_id, min_severity_rating
    ):
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
        if not any(claim["agent_assigned_id"] == agent_id for claim in self.__claim_data):
            return None
        
        num_valid = 0
        for claim in self.__claim_data:
            if claim["agent_assigned_id"] != agent_id:
                continue
            num_valid += claim["severity_rating"] >= min_severity_rating and claim["status"] != "Closed"

        return num_valid

    # endregion

    # region TestSetThree
    def compare_dates(self, date1, date2):
        '''
        Returns 1 if date1 occurs later than date2, 0 if they're the same, and -1 otherwise
        '''
        y1, m1, d1 = date1.split("-")
        y2, m2, d2 = date2.split("-")

        if y1 == y2 and m1 == m2 and d1 == d2:
            return 0
        
        date_int1 = int(y1 + m1 + d1)
        date_int2 = int(y2 + m2 + d2)
        return [-1, 1][date_int1 < date_int2]

    def get_num_disasters_declared_after_end_date(self):
        """Gets the number of disasters where it was declared after it ended

        Returns:
            int: number of disasters where the declared date is after the end date
        """
        return sum([self.compare_dates(claim["end_date"], claim["declared_date"]) == 1 for claim in self.__disaster_data])


    def build_map_of_agents_to_total_claim_cost(self):
        """Builds a map of agent and their total claim cost

        Hints:
            An agent with no claims should return 0
            Invalid agent id should have a value of None
            You should round your total_claim_cost to the nearest hundredths

        Returns:
            dict: key is agent id, value is total cost of claims associated to the agent
        """
        agent_total_claims = {}
        for claim in self.__claim_data:
            agent = claim["agent_assigned_id"]
            cost = claim["estimate_cost"]
            agent_total_claims[agent] = round(agent_total_claims.get(agent, 0) + cost, 2)
        
        # Fill in valid agent's counts with 0
        for agent in self.__agent_data:
            agent_id = agent["id"]
            agent_total_claims[agent_id] = agent_total_claims.get(agent_id, 0)
        
        return agent_total_claims

    def _get_disaster(self, id):
        for disaster in self.__disaster_data:
            if disaster["id"] == id:
                return disaster

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
        if disaster_id < 1 or disaster_id >= len(self.__disaster_data):
            return None
        
        num_disasters = sum([claim["disaster_id"] == disaster_id for claim in self.__claim_data])
        

        disaster_info = self._get_disaster(disaster_id)
        disaster_area = math.pi * disaster_info["radius_miles"] ** 2
        
        return round(num_disasters / disaster_area, 5)

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
        month_dict = {
            1 : "January",
            2 : "February",
            3 : "March",
            4 : "April",
            5 : "May",
            6 : "June",
            7 : "July",
            8 : "August",
            9 : "September",
            10 : "October",
            11 : "November",
            12 : "December"
        }

        date_total_claim = {}
        for claim in self.__claim_data:
            disaster_id = claim["disaster_id"]
            disaster = self._get_disaster(disaster_id)
            year, month, _ = disaster["declared_date"].split("-")
            key = f"{month_dict.get(int(month))} {year}"
            date_total_claim[key] = date_total_claim.get(key, 0) + 1

        top_three = []
        for _ in range(3):
            largest_key = self._dict_argmax(date_total_claim)
            top_three.append(largest_key)
            del date_total_claim[largest_key]

        return top_three         


    # endregion
