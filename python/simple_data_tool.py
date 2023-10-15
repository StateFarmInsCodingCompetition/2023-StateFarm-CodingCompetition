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
        # Initialize close count
        closed_claims = 0

        # Get Data
        data = self.get_claim_data()

        # Loop through claim data
        for item in data:

            # Check if claim is
            if item["status"] == 'Closed':

                # Increase amount of closed claims
                closed_claims += 1

        # Return Closed claim amount
        return closed_claims

    def get_num_claims_for_claim_handler_id(self, claim_handler_id):
        """Calculates the number of claims assigned to a specific claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            int: number of claims assigned to claim handler
        """
        # Initialize claim count
        claim_count = 0

        # Get Data of claims
        data = self.get_claim_data()

        # Loop through casses
        for item in data:

            # Check if item has claim id in it
            if item['claim_handler_assigned_id'] == claim_handler_id:

                # Increase claim count
                claim_count += 1

        # Return count of claim
        return claim_count

    def get_num_disasters_for_state(self, state):
        """Calculates the number of disasters for a specific state

        Args:
            state (string): name of a state in the United States of America,
                            including the District of Columbia

        Returns:
            int: number of disasters for state
        """
        # Initialize number of disasters
        num_disasters = 0

        # Get data
        data = self.get_disaster_data()

        # Loop through data
        for item in data:

            # check if item is for state specified
            if item['state'] == state:

                # increase number of disasters
                num_disasters += 1

        # Return number of disasters
        return num_disasters

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
        # Initialize total cost of damages
        total_cost = 0.0

        # Get disaster data
        data = self.get_claim_data()

        # Loop
        for item in data:

            # check if disaster id matches
            if item['disaster_id'] == disaster_id:

                # Add to total costs
                total_cost += item['estimate_cost']

        # Check if claims were found
        if total_cost:

            # return total cost of disasters
            return total_cost

        # Return None if nothing found
        return None

    def get_average_claim_cost_for_claim_handler(self, claim_handler_id):
        """Gets the average estimated cost of all claims assigned to a claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            float | None : average cost of claims, rounded to the nearest hundredths place
                           or None if no claims are found
        """
        # Initialize list of costs
        cost_list = []

        # Initialize average cost
        avg_cost = 0.0

        # Get claims data
        data = self.get_claim_data()

        # Loop trhough data
        for item in data:

            # Check if handler id matches item
            if item['claim_handler_assigned_id'] == claim_handler_id:

                # Add Cost for claim to list of costs
                cost_list.append(item['estimate_cost'])

        # Check if claims were found
        if len(cost_list) > 0:

            # Get average cost
            avg_cost = mean(cost_list)

            # Return average cost
            return round(avg_cost, 2)

        # Return None if no claims found
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
        # Get disaster data
        data = self.get_disaster_data()

        # Create empty dictionary
        state_totals = {}

        max_state = ''

        # loop through data
        for item in data:

            # Get state for current item
            state_name = item['state']

            # Check if state is in the dictionary
            if state_name in state_totals:

                # Increase total disasters for state
                state_totals[state_name] += 1

            # Otherwise initialize state
            else:

                # Set state name number of disasters to 1
                state_totals[state_name] = 1

        # Get Max disasters from all the states
        max_states = [key for key, value in state_totals.items() if value ==
                      max(state_totals.values())]

        max_state = max_states[0]

        if len(max_states) > 1:

            if max_states[0] > max_states[1]:

                return max_states[0]

            else:

                return max_states[1]

        # Return first max value
        return max_state

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
        data = self.get_disaster_data()

        # Create empty dictionary
        state_totals = {}

        max_state = ''

        # loop through data
        for item in data:

            # Get state for current item
            state_name = item['state']

            # Check if state is in the dictionary
            if state_name in state_totals:

                # Increase total disasters for state
                state_totals[state_name] += 1

            # Otherwise initialize state
            else:

                # Set state name number of disasters to 1
                state_totals[state_name] = 1

        # Get Max disasters from all the states
        min_states = [key for key, value in state_totals.items() if value ==
                      min(state_totals.values())]

        print(min_states)

        # Return first max value
        return min_states[0]

    def get_most_spoken_agent_language_by_state(self, state):
        """Returns the name of the most spoken language by agents (besides English) for a specific state

        Args:
            state (string): name of state

        Returns:
            string: name of language
                    or empty string if state doesn't exist
        """

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

        pass

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
