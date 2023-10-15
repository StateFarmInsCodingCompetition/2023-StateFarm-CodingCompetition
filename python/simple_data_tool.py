import json
import math
import os
# import matplotlib.pyplot as plt
# import seaborn as sns
# import pandas as pd
# import plotly.express as px
from datetime import datetime
from statistics import mean

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Get the directory of your script
DATA_DIR = os.path.join(BASE_DIR, 'data')  

class SimpleDataTool:

    AGENTS_FILEPATH = os.path.join(DATA_DIR, 'sfcc_2023_agents.json')
    CLAIM_HANDLERS_FILEPATH = os.path.join(DATA_DIR, 'sfcc_2023_claim_handlers.json')
    CLAIMS_FILEPATH = os.path.join(DATA_DIR, 'sfcc_2023_claims.json')
    DISASTERS_FILEPATH = os.path.join(DATA_DIR, 'sfcc_2023_disasters.json')


    # AGENTS_FILEPATH = '/Users/yashsarkar/2023-StateFarm-CodingCompetition/round 1/sfcc_2023_agents.json'
    # CLAIM_HANDLERS_FILEPATH = '/Users/yashsarkar/2023-StateFarm-CodingCompetition/round 1/sfcc_2023_claim_handlers.json'
    # CLAIMS_FILEPATH = '/Users/yashsarkar/2023-StateFarm-CodingCompetition/round 1/sfcc_2023_claims.json'
    # DISASTERS_FILEPATH = '/Users/yashsarkar/2023-StateFarm-CodingCompetition/round 1/sfcc_2023_disasters.json'

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

    def get_disaster_by_id(self, disaster_id):
        for disaster in self.get_disaster_data():
            if disaster['id'] == disaster_id:
                return disaster
        return None
    # Unit Test Methods

    # region Test Set One

    def get_num_closed_claims(self):
        """Calculates the number of claims where that status is "Closed"

        Returns:
            int: number of closed claims
        """
        closed_claims = [claim for claim in self.__claim_data if claim['status'] == 'Closed']
        return len(closed_claims)
        pass

    def get_num_claims_for_claim_handler_id(self, claim_handler_id):
        """Calculates the number of claims assigned to a specific claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            int: number of claims assigned to claim handler
        """
         # Initialize a counter to keep track of the number of claims
        num_claims = 0
        # Iterate through the list of claims
        for claim in self.__claim_data:
            # Check if the claim's 'claim_handler_id' matches the provided 'claim_handler_id'
            if claim['claim_handler_assigned_id'] == claim_handler_id:
                num_claims += 1  # Increment the counter for each matching claim

        return num_claims
        pass

    def get_num_disasters_for_state(self, state):
        """Calculates the number of disasters for a specific state 

        Args:
            state (string): name of a state in the United States of America,
                            including the District of Columbia

        Returns:
            int: number of disasters for state
        """
        num_disasters = 0

        for disaster in self.__disaster_data:
        # Check if the disaster's 'location' field contains the specified state
            if state in disaster['state']:
                num_disasters += 1  # Increment the counter for each matching disaster

        return num_disasters
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
        total_cost = 0.0

        # Iterate through the list of claims
        for claim in self.__claim_data:
            # Check if the claim is associated with the specified disaster_id
            if claim['disaster_id'] == disaster_id:
                # Add the estimated cost of the claim to the total cost
                total_cost += claim['estimate_cost']

        # Check if there were no claims found for the specified disaster
        if total_cost == 0.0:
            return None  # Return None if no claims were found
        else:
            # Round the total cost to the nearest hundredths place
            return round(total_cost, 2)
        
        pass

    def get_average_claim_cost_for_claim_handler(self, claim_handler_id):
        """Gets the average estimated cost of all claims assigned to a claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            float | None : average cost of claims, rounded to the nearest hundredths place
                           or None if no claims are found
        """
        total_cost = 0.0
        num_claims = 0

        # Iterate through the list of claims
        for claim in self.__claim_data:
            # Check if the claim is assigned to the specified claim_handler_id
            if claim['claim_handler_assigned_id'] == claim_handler_id:
                # Add the estimated cost of the claim to the total cost
                total_cost += claim['estimate_cost']
                # Increment the number of claims
                num_claims += 1

        # Check if there were no claims found for the specified claim handler
        if num_claims == 0:
            return None  # Return None if no claims were found

        # Calculate the average cost by dividing the total cost by the number of claims
        average_cost = total_cost / num_claims

        # Round the average cost to the nearest hundredths place
        return round(average_cost, 2)
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
        state_disaster_count = {}

        # Iterate through the list of disasters
        for disaster in self.__disaster_data:
            state = disaster['state'] # Extract the state name
            if state in state_disaster_count:
                state_disaster_count[state] += 1
            else:
                state_disaster_count[state] = 1

        # Find the state with the most disasters
        max_disasters = max(state_disaster_count.values())

        # Create a list of states with the maximum number of disasters
        states_with_max_disasters = [state for state, count in state_disaster_count.items() if count == max_disasters]

        # Sort the list alphabetically and return the first state
        return sorted(states_with_max_disasters)[0]
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
        state_disaster_count = {}

        # Iterate through the list of disasters
        for disaster in self.__disaster_data:
            state = disaster['state'] # Extract the state name
            if state in state_disaster_count:
                state_disaster_count[state] += 1
            else:
                state_disaster_count[state] = 1

        # Find the state with the least disasters
        min_disasters = min(state_disaster_count.values())

        # Create a list of states with the minimum number of disasters
        states_with_min_disasters = [state for state, count in state_disaster_count.items() if count == min_disasters]

        # Sort the list alphabetically and return the first state
        return sorted(states_with_min_disasters)[0]
        pass
    
    def get_most_spoken_agent_language_by_state(self, state):
        """Returns the name of the most spoken language by agents (besides English) for a specific state

        Args:
            state (string): name of state

        Returns:
            string: name of language
                    or empty string if state doesn't exist
        """
        language_count = {}

        # Iterate through the agent data
        for agent in self.__agent_data:
            agent_state = agent['state']

            # Check if the agent belongs to the specified state
            if agent_state == state:
                # Extract primary and secondary languages spoken by the agent (excluding English)
                primary_language = agent.get('primary_language', '')
                secondary_language = agent.get('secondary_language', '')
                
                # Add primary language to the language count
                if primary_language != 'English':
                    language_count[primary_language] = language_count.get(primary_language, 0) + 1
                
                # Add secondary language to the language count
                if secondary_language != 'English':
                    language_count[secondary_language] = language_count.get(secondary_language, 0) + 1

        # Find the language with the highest count
        most_spoken_language = max(language_count, key=language_count.get, default="")

        return most_spoken_language

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
        if not (1 <= min_severity_rating <= 10):
            return -1  # Severity rating out of bounds

        # Initialize a variable to count the number of matching open claims
        num_matching_claims = 0

        # Iterate through the list of claims
        for claim in self.__claim_data:
            # Check if the claim is assigned to the specified agent and is not closed
            if claim['agent_assigned_id'] == agent_id and claim['status'] != 'Closed':
                # Check if the claim's severity rating is greater than or equal to min_severity_rating
                if claim['severity_rating'] >= min_severity_rating:
                    num_matching_claims += 1

        # Check if the agent exists and has at least one open claim
        if num_matching_claims > 0:
            return num_matching_claims  # Return the number of matching open claims
        else:
            return None  # Agent does not exist or has no open claims

        pass

    # endregion

    # region TestSetThree

    def get_num_disasters_declared_after_end_date(self):
        """Gets the number of disasters where it was declared after it ended

        Returns:
            int: number of disasters where the declared date is after the end date
        """
        count = 0

        # Iterate through the list of disasters
        for disaster in self.__disaster_data:
            # Extract the declared date and end date from the disaster data
            declared_date_str = disaster['declared_date']
            end_date_str = disaster['end_date']

            # Convert the date strings to datetime objects
            declared_date = datetime.strptime(declared_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

            # Check if the declared date is after the end date
            if declared_date > end_date:
                count += 1

        # Return the count of disasters declared after the end date
        return count

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
        agent_to_total_claim_cost = {}

        # Iterate through the list of claims
        for claim in self.__claim_data:
            # Extract the agent ID and claim cost from the claim data
            agent_id = claim['agent_assigned_id']
            claim_cost = claim['estimate_cost']

            # Check if the agent ID is valid (exists in the agent data)
            if agent_id in agent_to_total_claim_cost:
                # Increment the total claim cost associated with the agent
                agent_to_total_claim_cost[agent_id] += claim_cost
            else:
                # If the agent ID is not in the dictionary, add it with the claim cost
                agent_to_total_claim_cost[agent_id] = claim_cost

        # Round the total claim cost to the nearest hundredths for each agent
        for agent_id in agent_to_total_claim_cost:
            agent_to_total_claim_cost[agent_id] = round(agent_to_total_claim_cost[agent_id], 2)

        # Ensure agents with no claims have a total claim cost of 0
        for agent in self.__agent_data:
            agent_id = agent['id']
            if agent_id not in agent_to_total_claim_cost:
                agent_to_total_claim_cost[agent_id] = 0.0

        return agent_to_total_claim_cost

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
        # Find the disaster with the specified disaster_id in the disaster data
        disaster = None
        for d in self.__disaster_data:
            if d['id'] == disaster_id:
                disaster = d
                break

        # Check if the disaster exists
        if disaster is None:
            return None  # Disaster does not exist

        # Calculate the area of the disaster impact area (assuming it's a circle)
        impact_radius = disaster['radius_miles']
        disaster_area = math.pi * (impact_radius ** 2)

        # Count the number of claims associated with the disaster
        num_claims = 0
        for claim in self.__claim_data:
            if claim['disaster_id'] == disaster_id:
                num_claims += 1

        # Calculate the density of claims to the disaster area
        if disaster_area > 0:
            density = num_claims / disaster_area
            return round(density, 5)  # Round to three decimal places
        else:
            return None  # Avoid division by zero if the disaster_area is zero
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
        # Create a dictionary to store the count of claims for each month and year combination
        month_year_to_claim_count = {}

        # Iterate through the list of claims
        for claim in self.__claim_data:
            # Extract the disaster ID associated with the claim
            disaster_id = claim['disaster_id']

            # Find the corresponding disaster data using the disaster ID
            disaster = next((d for d in self.__disaster_data if d['id'] == disaster_id), None)

            # If a matching disaster is found, extract the claim date
            if disaster:
                claim_date = disaster['declared_date']

                # Extract the year and month from the claim date (assuming the date format is 'YYYY-MM-DD')
                year, month, _ = claim_date.split('-')

                # Create a key in the format 'YYYY-MM' and increment the claim count for that month and year
                month_year_key = f"{year}-{month}"
                if month_year_key in month_year_to_claim_count:
                    month_year_to_claim_count[month_year_key] += 1
                else:
                    month_year_to_claim_count[month_year_key] = 1

        # Sort the dictionary by claim count in descending order and get the top three entries
        top_three_months = sorted(month_year_to_claim_count.items(), key=lambda x: x[1], reverse=True)[:3]

        # Format the result as required (full month name and full four-digit year)
        formatted_result = []
        for month_year, _ in top_three_months:
            year, month = month_year.split('-')
            formatted_month = {
                '01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June',
                '07': 'July', '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'
            }[month]
            formatted_result.append(f"{formatted_month} {year}")

        return formatted_result

    # endregion
