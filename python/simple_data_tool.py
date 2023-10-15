import json
import math

from statistics import mean


class SimpleDataTool:
    AGENTS_FILEPATH = "data/sfcc_2023_agents.json"
    CLAIM_HANDLERS_FILEPATH = "data/sfcc_2023_claim_handlers.json"
    CLAIMS_FILEPATH = "data/sfcc_2023_claims.json"
    DISASTERS_FILEPATH = "data/sfcc_2023_disasters.json"

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
        count = 0
        claim_data = self.get_claim_data()
        for claim in claim_data:
            if claim["status"] == "Closed":
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
        claim_data = self.get_claim_data()
        for claim in claim_data:
            if claim["claim_handler_assigned_id"] == claim_handler_id:
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
        disaster_data = self.get_disaster_data()
        for disaster in disaster_data:
            if disaster["state"] == state:
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
        total = 0
        claim_data = self.get_claim_data()
        for claim in claim_data:
            if claim["disaster_id"] == disaster_id:
                total += claim["estimate_cost"]
        return round(total, 2) if total > 0 else None

    def get_average_claim_cost_for_claim_handler(self, claim_handler_id):
        """Gets the average estimated cost of all claims assigned to a claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            float | None : average cost of claims, rounded to the nearest hundredths place
                           or None if no claims are found
        """
        costs = []
        claim_data = self.get_claim_data()
        for claim in claim_data:
            if claim["claim_handler_assigned_id"] == claim_handler_id:
                costs.append(claim["estimate_cost"])
        return round(mean(costs), 2) if len(costs) > 0 else None

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
        state_disasters_count = {}
        disaster_data = self.get_disaster_data()
        for disaster in disaster_data:
            if disaster["state"] in state_disasters_count:
                state_disasters_count[disaster["state"]] += 1
            else:
                state_disasters_count[disaster["state"]] = 1
        max_disasters = max(state_disasters_count.values())
        states_most_disasters = [
            k for k, v in state_disasters_count.items() if v == max_disasters
        ]
        return min(states_most_disasters)

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
        state_disasters_count = {}
        disaster_data = self.get_disaster_data()
        for disaster in disaster_data:
            if disaster["state"] in state_disasters_count:
                state_disasters_count[disaster["state"]] += 1
            else:
                state_disasters_count[disaster["state"]] = 1
        min_disasters = min(state_disasters_count.values())
        states_least_disasters = [
            k for k, v in state_disasters_count.items() if v == min_disasters
        ]
        return min(states_least_disasters)

    def get_most_spoken_agent_language_by_state(self, state):
        """Returns the name of the most spoken language by agents (besides English) for a specific state

        Args:
            state (string): name of state

        Returns:
            string: name of language
                    or empty string if state doesn't exist
        """
        agent_data = self.get_agent_data()
        languages_count = {}
        for agent in agent_data:
            if agent["state"] == state:
                primary_language = agent["primary_language"]
                secondary_language = agent["secondary_language"]
                if primary_language in languages_count:
                    languages_count[primary_language] += 1
                else:
                    languages_count[primary_language] = 1
                if secondary_language in languages_count:
                    languages_count[secondary_language] += 1
                else:
                    languages_count[secondary_language] = 1
        if len(languages_count) == 0:
            return ""
        if "English" in languages_count:
            del languages_count["English"]
        return max(languages_count, key=languages_count.get)

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
        count = 0
        claim_data = self.get_claim_data()
        for claim in claim_data:
            if (
                claim["agent_assigned_id"] == agent_id
                and claim["status"] != "Closed"
                and claim["severity_rating"] >= min_severity_rating
            ):
                count += 1
        return count if count > 0 else None

    # endregion

    # region TestSetThree

    def get_num_disasters_declared_after_end_date(self):
        """Gets the number of disasters where it was declared after it ended

        Returns:
            int: number of disasters where the declared date is after the end date
        """
        count = 0
        disaster_data = self.get_disaster_data()
        for disaster in disaster_data:
            if disaster["declared_date"] > disaster["end_date"]:
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
        agent_data = self.get_agent_data()
        claim_data = self.get_claim_data()
        agent_total_claim_cost = {}
        for agent in agent_data:
            agent_total_claim_cost[agent["id"]] = 0
        for claim in claim_data:
            if claim["agent_assigned_id"] in agent_total_claim_cost:
                agent_total_claim_cost[claim["agent_assigned_id"]] += claim[
                    "estimate_cost"
                ]
        for agent in agent_total_claim_cost:
            agent_total_claim_cost[agent] = round(agent_total_claim_cost[agent], 2)
        return agent_total_claim_cost

    def calculate_disaster_claim_density(self, disaster_id):
        """Calculates density of a disaster based on the number of claims and impact radius

        Hints:
            Assume uniform spacing between claims
            Assume disaster impact area is a circle

        Args:
            disaster_id (int): id of diaster

        Returns:
            float: density of claims to disaster area, rounded to the nearest thousandths place
                   None if disaster does not exist
        """
        disaster_data = self.get_disaster_data()
        claim_data = self.get_claim_data()
        disaster = next(
            (item for item in disaster_data if item["id"] == disaster_id), None
        )
        if disaster == None:
            return None
        disaster_radius = disaster["radius_miles"]
        disaster_area = disaster_radius**2 * math.pi
        claims_count = 0
        for claim in claim_data:
            if claim["disaster_id"] == disaster_id:
                claims_count += 1
        return round(claims_count / (disaster_area), 5)

    # endregion

    # region TestSetFour

    def get_top_three_months_with_highest_num_of_claims_desc(self):
        """Gets the top three months with the highest number of claims

        Hint:
            Month should be full name like 01 is January and 12 is December
            Year should be full four-digit year
            List should be in descending order

        Returns:
            list: three strings of month and year, descending order of highest claims
        """
        NUMBER_TO_MONTH_MAP = {
            "01": "January",
            "02": "February",
            "03": "March",
            "04": "April",
            "05": "May",
            "06": "June",
            "07": "July",
            "08": "August",
            "09": "September",
            "10": "October",
            "11": "November",
            "12": "December",
        }
        disaster_data = self.get_disaster_data()
        claim_data = self.get_claim_data()
        disaster_claims_count = {}
        for disaster in disaster_data:
            disaster_date = disaster["declared_date"]
            disaster_claims_count[disaster["id"]] = {
                "date": f"{NUMBER_TO_MONTH_MAP[disaster_date.split('-')[1]]} {disaster_date[:4]}",
                "count": 0,
            }
        for claim in claim_data:
            disaster_claims_count[claim["disaster_id"]]["count"] += 1
        # consolidate disaster and counts keyed by month
        dates_count = {}
        for disaster in disaster_claims_count:
            date = disaster_claims_count[disaster]["date"]
            count = disaster_claims_count[disaster]["count"]
            if date in dates_count:
                dates_count[date] += count
            else:
                dates_count[date] = count
        # sort dates by count
        sorted_dates = sorted(dates_count, key=dates_count.get, reverse=True)
        return sorted_dates[:3]

    # endregion
