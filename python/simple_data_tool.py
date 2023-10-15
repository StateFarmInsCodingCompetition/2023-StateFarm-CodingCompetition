import json
import math

from statistics import mean
import datetime # For Test Set Four



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
        claims = self.get_claim_data()
        closed_claims_count = sum(1 for claim in claims if claim['status'] == 'Closed')
        return closed_claims_count
        """Calculates the number of claims where that status is "Closed"

        Returns:
            int: number of closed claims
        """
        pass

    def get_num_claims_for_claim_handler_id(self, claim_handler_id):
        claims = self.get_claim_data()
        claim_handler_claims = sum(1 for claim in claims if claim['claim_handler_assigned_id'] == claim_handler_id)
        return claim_handler_claims
        """Calculates the number of claims assigned to a specific claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            int: number of claims assigned to claim handler
        """
        pass

    def get_num_disasters_for_state(self, state):
        disasters = self.get_disaster_data()
        state_disasters = sum(1 for disaster in disasters if disaster['state'] == state)
        return state_disasters
        """Calculates the number of disasters for a specific state

        Args:
            state (string): name of a state in the United States of America,
                            including the District of Columbia

        Returns:
            int: number of disasters for state
        """
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
        # Assign dataset to variable
        claims = self.get_claim_data()
        
        # Total_cost to calculate all sums of estimate_cost
        total_cost = 0  

        # Looping through claims to find those related to the disaster_id
        for claim in claims:
            if claim['disaster_id'] == disaster_id:
                # add to total cost if disaster_id matches
                total_cost += claim['estimate_cost']

        # If there is no cost, return None
        return round(total_cost, -2) if total_cost > 0 else None


    def get_average_claim_cost_for_claim_handler(self, claim_handler_id):
        """Gets the average estimated cost of all claims assigned to a claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            float | None : average cost of claims, rounded to the nearest hundredths place
                           or None if no claims are found
        """
        # Initialize variables for total_cost and count
        total_cost = 0
        count = 0

        # Assign dataset to variable
        claims = self.get_claim_data()
        
        # Iterate through claims, add estimate_cost if claim_handler_assigned_id matches
        for claim in claims:
            if claim['claim_handler_assigned_id'] == claim_handler_id:
                # If the dataset matches, add to total_cost and increment count
                total_cost += claim['estimate_cost']
                count += 1
        
        # If count is 0, return None, else return average cost rounded to nearest hundredths place
        return None if count == 0 else round(total_cost / count, -2)

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
        # Create a dictionary to hold counts of disasters per state
        disaster_counts = {}
        
        # Assign dataset to variable
        disasters = self.get_disaster_data()
        
        # Iterate through disasters, add to dictionary for each state
        for disaster in disasters:
            state = disaster['state']
            disaster_counts[state] = disaster_counts.get(state, 0) + 1
            
        # Initialize variables to store the state with most disasters
        most_disasters_state = None
        max_disasters_count = 0
        
        # Sorted list of states alphabetically by using keys() method
        states = sorted(disaster_counts.keys())
        
        # Iterate through states and find the state with the most disasters
        for state in states:
            if disaster_counts[state] > max_disasters_count:
                most_disasters_state = state
                max_disasters_count = disaster_counts[state]
        
        return most_disasters_state

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
        # Create a dictionary to hold counts of disasters per state
        disaster_counts = {}
        
        # Assign dataset to variable
        disasters = self.get_disaster_data()
        
        # Iterate through disasters, add to dictionary for each state
        for disaster in disasters:
            state = disaster['state']
            disaster_counts[state] = disaster_counts.get(state, 0) + 1
        
        # Initialize variables to store the state with the least disasters
        least_disasters_state = None
        min_disasters_count = float('inf')  # Set initial value to positive infinity
        
        # Sorted list of states alphabetically
        states = sorted(disaster_counts.keys())
        
        # Iterate through states and find the state with the least disasters
        for state in states:
            if disaster_counts[state] < min_disasters_count:
                least_disasters_state = state
                min_disasters_count = disaster_counts[state]
        
        return least_disasters_state
    
    def get_most_spoken_agent_language_by_state(self, state):
        """Returns the name of the most spoken language by agents (besides English) for a specific state

        Args:
            state (string): name of state

        Returns:
            string: name of language
                    or empty string if state doesn't exist
        """
        # Create a dictionary to hold counts of languages per state
        language_counts = {}  
        
        # Assign dataset to variable
        agents = self.get_agent_data()
        
        # Traverse through agents data
        for agent in agents:
            # Check if the agent is from the specified state
            if agent['state'] == state:
                # Get the languages spoken by the agent excluding English
                languages = [lang for lang in agent['languages'] if lang != 'English']
                # Increment count for each language in the dictionary
                for lang in languages:
                    language_counts[lang] = language_counts.get(lang, 0) + 1
        
        # Check if no languages were found return empty string
        if not language_counts:
            return ''
    
        # Find and return the most spoken language / get function returns 0 if key not found
        most_spoken_language = max(language_counts, key=language_counts.get)
        return most_spoken_language

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
        # Assign dataset to variable
        agents = self.get_agent_data()
        claims = self.get_claim_data()
        
        # Check if the severity rating is out of bounds
        if min_severity_rating < 1 or min_severity_rating > 10:
            return -1
        
        # Check if the agent exists / any() returns True if any element of the iterable is true
        agent_exists = any(agent['id'] == agent_id for agent in agents)
        if not agent_exists:
            return None
        
        
        # Initialize a counter for open claims
        open_claims_count = 0
        # Check every claim
        for claim in claims:
            # Check if the claim is assigned to the agent, is not closed, and has sufficient severity
            if (
                claim['agent_assigned_id'] == agent_id and
                claim['status'] != "Closed" and
                claim['severity_rating'] >= min_severity_rating
            ):
                # If all conditions are met, increment the counter
                open_claims_count += 1
        
        # Return None if there are no qualifying claims
        return open_claims_count if open_claims_count > 0 else None

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
        # Dictionary to store the total cost of claims per month
        monthly_costs = {}

        # Assign dataset to variable
        claims = self.get_claim_data()
        
        # Loop through each claim
        for claim in claims:
            # Extract the month and year (assuming a date field is available and in 'YYYY-MM-DD' format)
            claim_date = datetime.datetime.strptime(claim['date'], '%Y-%m-%d')
            month_year = claim_date.strftime('%B %Y')

            # Add the cost of this claim to the monthly total
            monthly_costs[month_year] = monthly_costs.get(month_year, 0) + claim['estimate_cost']
        
        # Get the top three months by total claim cost
        top_three_months = sorted(monthly_costs.keys(), key=lambda month: monthly_costs[month], reverse=True)[:3]
        
        return top_three_months

    # endregion
