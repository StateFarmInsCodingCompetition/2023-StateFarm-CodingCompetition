import json
import math
import pandas as pd

from statistics import mean
from datetime import datetime as dt       



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
        claims = self.get_claim_data()
        count = 0
        for claim in claims:
            if claim['status'] == 'Closed':
                count += 1
        return count

    def get_num_claims_for_claim_handler_id(self, claim_handler_id):
        """Calculates the number of claims assigned to a specific claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            int: number of claims assigned to claim handler
        """
        claims = self.get_claim_data()
        count = 0
        for claim in claims:
            if claim['claim_handler_assigned_id'] == claim_handler_id:
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
        
        disasters = self.get_disaster_data()
        count = 0
        for disaster in disasters:
            if disaster['state'] == state:
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

        claims = self.get_claim_data()
        total = 0     
        for row in claims:
            if row['disaster_id'] == disaster_id:
                total += row['estimate_cost']     
     
        if total == 0:
            return None  
        else:
            return round(total, 2)  

    def get_average_claim_cost_for_claim_handler(self, claim_handler_id):
        """Gets the average estimated cost of all claims assigned to a claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            float | None : average cost of claims, rounded to the nearest hundredths place
                           or None if no claims are found
        """

        claims = self.get_claim_data()
        count = 0
        total_cost = 0
        for claim in claims:
            if claim["claim_handler_assigned_id"] == claim_handler_id:
                count += 1
                total_cost += claim["estimate_cost"]
        if count == 0:
            return None
        else:
            average = total_cost/count

        return round(average, 2)

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

        disatsers = self.get_disaster_data()

        # Keeps track of the state and the number of disasters
        state_disaster_count = {}

        for disaster in disatsers:
            state = disaster['state']
            state_disaster_count[state] = state_disaster_count.get(state, 0) + 1

        # Get maximum disaster count
        max_value = max(state_disaster_count.values())

        # Get list of states with max value
        states_with_max_disasters = [key for key, value in state_disaster_count.items() if value == max_value]

        # Sort list of states
        states_with_max_disasters.sort()

        # Return first state
        return states_with_max_disasters[0]

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
            
        disatsers = self.get_disaster_data()

        # Keeps track of the state and the number of disasters
        state_disaster_count = {}

        for disaster in disatsers:
            state = disaster['state']
            state_disaster_count[state] = state_disaster_count.get(state, 0) + 1

        # Get minimum disaster count
        min_value = min(state_disaster_count.values())

        # Get list of states with min value
        states_with_min_disasters = [key for key, value in state_disaster_count.items() if value == min_value]

        # Sort list of states
        states_with_min_disasters.sort()

        # Return first state
        return states_with_min_disasters[0]
    
    def get_most_spoken_agent_language_by_state(self, state):
        """Returns the name of the most spoken language by agents (besides English) for a specific state

        Args:
            state (string): name of state

        Returns:
            string: name of language
                    or empty string if state doesn't exist
        """

        agents = self.get_agent_data()

        # Keeps track of the language and the number of agents
        language_agent_count = {}

        for agent in agents:
            if agent['state'] == state:
                language = agent['secondary_language']
                print(language)
                language_agent_count[language] = language_agent_count.get(language, 0) + 1

        if language_agent_count:
            # Get maximum agent count
            max_value = max(language_agent_count.values())

            # Get list of languages with max value
            languages_with_max_agents = [key for key, value in language_agent_count.items() if value == max_value]

            # Sort list of languages
            languages_with_max_agents.sort()

        return languages_with_max_agents[0] if language_agent_count else ''

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

        def check_agent_exists(agent_id, agents):
            """Checks if agent exists

            Args:
                agent_id (int): ID of the agent
                agents (list): list of agents

            Returns:
                bool: True if agent exists, False otherwise
            """
            for agent in agents:
                if agent['id'] == agent_id:
                    return True
            return False
        
        def claim_has_min_severity_rating(claim, min_severity_rating):
            """Checks if claim has minimum severity rating

            Args:
                claim (dict): claim data
                min_severity_rating (int): minimum claim severity rating

            Returns:
                bool: True if claim has minimum severity rating, False otherwise
            """
            return claim['severity_rating'] >= min_severity_rating
        
        def claim_is_open(claim):
            """Checks if claim is open

            Args:
                claim (dict): claim data

            Returns:
                bool: True if claim is open, False otherwise
            """
            return claim['status'] != 'Closed'

        agents = self.get_agent_data()
        claims = self.get_claim_data()

        # Check if agent exists
        if not check_agent_exists(agent_id, agents) or (min_severity_rating < 1 or min_severity_rating > 10):
            return -1
        
        # Keeps track of the number of open claims with at least the minimum severity rating
        count = 0

        for claim in claims:
            if claim['agent_assigned_id'] == agent_id and claim_has_min_severity_rating(claim, min_severity_rating) and claim_is_open(claim):
                count += 1

        return count if count > 0 else None

    # endregion

    # region TestSetThree

    def get_num_disasters_declared_after_end_date(self):
        """Gets the number of disasters where it was declared after it ended

        Returns:
            int: number of disasters where the declared date is after the end date
        """

        disasters = self.get_disaster_data()
        count = 0
        for disaster in disasters:
            end_date = dt.strptime(disaster["end_date"],"%Y-%m-%d").date()
            declared_date = dt.strptime(disaster["declared_date"], "%Y-%m-%d").date()
            if declared_date > end_date:
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

        # Create dataframes for agents and claims data to make it easier to work with the data
        agents_df = pd.DataFrame(self.get_agent_data())
        claims_df = pd.DataFrame(self.get_claim_data())

        # Create a dataframe with the agent id and the total claim cost
        agents_total_claim_cost = pd.DataFrame(agents_df['id'])
        agents_total_claim_cost['total_claim_cost'] = 0

        # Calculate the total claim cost for each agent
        for agent_id in agents_total_claim_cost['id']:
            # Get the total claim cost for the agent 
            # by summing the estimate cost of all claims associated to the agent
            total_claim_cost = claims_df[claims_df['agent_assigned_id'] == agent_id]['estimate_cost'].sum()
            # Set the total claim cost for the agent in the dataframe
            agents_total_claim_cost.loc[agents_total_claim_cost['id'] == agent_id, 'total_claim_cost'] = total_claim_cost

        # Round the total claim cost to the nearest hundredths
        agents_total_claim_cost['total_claim_cost'] = agents_total_claim_cost['total_claim_cost'].round(2)

        return agents_total_claim_cost.set_index('id').to_dict()['total_claim_cost']

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
        claims = self.get_claim_data()
        disasters = self.get_disaster_data()

        num_of_claims = 0    
        for claim in claims:
            if claim["disaster_id"] == disaster_id:
                num_of_claims += 1 
        
        for disaster in disasters:
            if disaster["id"] == disaster_id:
                miles_radius = disaster["radius_miles"]

        if num_of_claims == 0:
            return None  
        else:
            impact_area = math.pi * math.pow(miles_radius, 2)
            claim_density = num_of_claims/impact_area
            return round(claim_density, 5)      





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

        claims_df = pd.DataFrame(self.get_claim_data())
        open_claims_df = claims_df[claims_df['status'] != 'Closed']

        disasters_df = pd.DataFrame(self.get_disaster_data())

        merged_df = pd.merge(open_claims_df, disasters_df, left_on='disaster_id', right_on='id', how='inner')

        merged_df['declared_date'] = pd.to_datetime(merged_df['declared_date'])
        merged_df['month_year'] = merged_df['declared_date'].dt.strftime('%B %Y')

        grouped_df = merged_df.groupby('month_year')['estimate_cost'].sum()

        top_three_months = grouped_df.nlargest(3)

        print(top_three_months)

        return top_three_months.index.tolist()






    # endregion
