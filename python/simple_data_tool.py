import json
import math
import pandas as pd

from statistics import mean
from datetime import datetime, date, timedelta


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

    def __init__(
            self):
        self.__agent_data = self.load_json_from_file(self.AGENTS_FILEPATH)
        self.__claim_handler_data = self.load_json_from_file(
            self.CLAIM_HANDLERS_FILEPATH)
        self.__claim_data = self.load_json_from_file(self.CLAIMS_FILEPATH)
        self.__disaster_data = self.load_json_from_file(
            self.DISASTERS_FILEPATH)
        
        # convert data to dataframes for processing
        self.__agent_data_df = self.convert_data_to_df(self.__agent_data)
        self.__claim_handler_data_df = self.convert_data_to_df(self.__claim_handler_data)
        self.__claim_data_df = self.convert_data_to_df(self.__claim_data)
        self.__disaster_data_df = self.convert_data_to_df(self.__disaster_data)

    # Helper Methods

    def load_json_from_file(
            self, filename):
        data = None

        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return data
    
    def convert_data_to_df(
            self, data):
        df = pd.json_normalize(data)
        return df

    
    def get_agent_data(
            self):
        return self.__agent_data

    def get_claim_handler_data(
            self):
        return self.__claim_handler_data

    def get_disaster_data(
            self):
        return self.__disaster_data

    def get_claim_data(
            self):
        return self.__claim_data
    
    # functions for getting dataframes
    def get_agent_data_df(
            self):
        return self.__agent_data_df

    def get_claim_handler_data_df(
            self):
        return self.__claim_handler_data_df

    def get_disaster_data_df(
            self):
        return self.__disaster_data_df

    def get_claim_data_df(
            self):
        return self.__claim_data_df
    
    # Unit Test Methods

    # region Test Set One

    def get_num_closed_claims(
            self):
        """Calculates the number of claims where that status is "Closed"

        Returns:
            int: number of closed claims
        """
        # get number of entries with Closed status in the claims dataframe
        claim_data_df = self.get_claim_data_df()
        number_of_closed_claims = len(claim_data_df[
            (claim_data_df["status"] == "Closed")
            ])
        return number_of_closed_claims

    def get_num_claims_for_claim_handler_id(
            self, claim_handler_id):
        """Calculates the number of claims assigned to a specific claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            int: number of claims assigned to claim handler
        """
        # get number of entries assigned to given handler in the claims dataframe
        claim_data_df = self.get_claim_data_df()
        number_of_claims_assigned_to_handler = len(claim_data_df[
            (claim_data_df["claim_handler_assigned_id"] == claim_handler_id)
            ])
        return number_of_claims_assigned_to_handler

    def get_num_disasters_for_state(
            self, state):
        """Calculates the number of disasters for a specific state

        Args:
            state (string): name of a state in the United States of America,
                            including the District of Columbia

        Returns:
            int: number of disasters for state
        """
        # get number of entries of given state in the disaster dataframe
        disaster_data_df = self.get_disaster_data_df()
        number_of_disasters_of_state = len(disaster_data_df[
            (disaster_data_df["state"] == state)
            ])
        return number_of_disasters_of_state

    # endregion

    # region Test Set Two

    def get_total_claim_cost_for_disaster(
            self, disaster_id):
        """Sums the estimated cost of a specific disaster by its claims

        Args:
            disaster_id (int): id of disaster

        Returns:
            float | None: estimate cost of disaster, rounded to the nearest hundredths place
                          returns None if no claims are found
        """
        # get entries of given disaster id in the disaster dataframe
        claim_data_df = self.get_claim_data_df()
        df_for_given_disaster = claim_data_df[
            (claim_data_df["disaster_id"] == disaster_id)
            ]
        # return None if no claims are found
        if len(df_for_given_disaster) == 0:
            return None
        # sum the total estimated cost and round to 2 decimals
        total_cost = round(df_for_given_disaster["estimate_cost"].sum(), 2)
        return total_cost

    def get_average_claim_cost_for_claim_handler(
            self, claim_handler_id):
        """Gets the average estimated cost of all claims assigned to a claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            float | None : average cost of claims, rounded to the nearest hundredths place
                           or None if no claims are found
        """
        # get entries of given claim handler id in the claim dataframe
        claim_data_df = self.get_claim_data_df()
        df_for_given_claim_handler = claim_data_df[
            (claim_data_df["claim_handler_assigned_id"] == claim_handler_id)
            ]
        # return None if no claims are found
        if len(df_for_given_claim_handler) == 0:
            return None
        # sum the total estimated cost
        total_cost = df_for_given_claim_handler["estimate_cost"].sum()
        # divide by number of claims and round by 2 decimals to get average cost
        average_cost = round(total_cost / len(df_for_given_claim_handler), 2)
        return average_cost

    def get_state_with_most_disasters(
            self):
        """Returns the name of the state with the most disasters based on disaster data

        If two states have the same number of disasters, then sort by alphabetical (a-z)
        and take the first.

        Example: Say New Jersey and Delaware both have the highest number of disasters at
                 12 disasters each. Then, this method would return "Delaware" since "D"
                 comes before "N" in the alphabet. 

        Returns:
            string: single name of state
        """
        # get count of entries grouped by state in the disaster dataframe and sort by names
        disaster_data_df = self.get_disaster_data_df()
        df_for_count_of_disasters_by_state = disaster_data_df.groupby(["state"]).count().sort_values("state")
        # select the state with most disaster count
        state_with_most_disasters = df_for_count_of_disasters_by_state["id"].idxmax()
        return state_with_most_disasters

    def get_state_with_least_disasters(
            self):
        """Returns the name of the state with the least disasters based on disaster data

        If two states have the same number of disasters, then sort by alphabetical (a-z)
        and take the first.

        Example: Say New Mexico and West Virginia both have the least number of disasters at
                 1 disaster each. Then, this method would return "New Mexico" since "N"
                 comes before "W" in the alphabet. 

        Returns:
            string: single name of state
        """
        # get count of entries grouped by state in the disaster dataframe and sort by names
        disaster_data_df = self.get_disaster_data_df()
        df_for_count_of_disasters_by_state = disaster_data_df.groupby(["state"]).count().sort_values("state")
        # select the state with least disaster count
        state_with_least_disasters = df_for_count_of_disasters_by_state["id"].idxmin()
        return state_with_least_disasters
    
    def get_most_spoken_agent_language_by_state(
            self, state):
        """Returns the name of the most spoken language by agents (besides English) for a specific state

        Args:
            state (string): name of state

        Returns:
            string: name of language
                    or empty string if state doesn't exist
        """
        # get entries of agents from given state in the agent dataframe
        agent_data_df = self.get_agent_data_df()
        df_for_agents_of_given_state = agent_data_df[
            agent_data_df["state"] == state
            ]
        # record the occurrences of non-English languages
        dict_for_counting_languages = {}
        # go through each agent entry
        for index, row in df_for_agents_of_given_state.iterrows():
            # first language
            current_primary_language = row["primary_language"]
            # second language
            current_secondary_language = row["secondary_language"]
            # record first language if it's not English or null
            if current_primary_language != "English" and current_primary_language != "null":
                if current_primary_language not in dict_for_counting_languages:
                    dict_for_counting_languages[current_primary_language] = 1
                else:
                    dict_for_counting_languages[current_primary_language] += 1
            # record second language if it's not English or null
            if current_secondary_language != "English" and current_secondary_language != "null":
                if current_secondary_language not in dict_for_counting_languages:
                    dict_for_counting_languages[current_secondary_language] = 1
                else:
                    dict_for_counting_languages[current_secondary_language] += 1
        
        # return empty string for nonexistent results
        if len(dict_for_counting_languages) == 0:
            return ""
        
        # find the most spoken language with max occurrences
        most_spoken_language = max(dict_for_counting_languages, key=dict_for_counting_languages.get)
        return most_spoken_language


    def get_num_of_open_claims_for_agent_and_severity(
            self, agent_id, min_severity_rating):
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
        # check if severity bound is valid and return -1 if not
        if min_severity_rating < 1 or min_severity_rating > 10:
            return -1
        # get entries of given agent's open claims within bound in the claim dataframe
        claim_data_df = self.get_claim_data_df()
        df_for_open_claims_of_given_agent_within_severity_bound = claim_data_df[
            (claim_data_df["agent_assigned_id"] == agent_id)
            & (claim_data_df["status"] != "Closed")
            & (claim_data_df["severity_rating"] >= min_severity_rating)
            ]
        # get number of entries of given agent's open claims within bound
        num_of_open_claims_for_agent_within_bound = len(df_for_open_claims_of_given_agent_within_severity_bound)
        # return None if there's no entry for this agent
        if num_of_open_claims_for_agent_within_bound == 0:
            return None
        return num_of_open_claims_for_agent_within_bound

    # endregion

    # region TestSetThree

    def get_num_disasters_declared_after_end_date(
            self):
        """Gets the number of disasters where it was declared after it ended

        Returns:
            int: number of disasters where the declared date is after the end date
        """
        # get entries of disasters declared after end date in the disaster dataframe
        disaster_data_df = self.get_disaster_data_df()
        df_for_disasters_declared_after_end_date = disaster_data_df[
            pd.to_datetime(disaster_data_df["declared_date"]) > pd.to_datetime(disaster_data_df["end_date"])
            ]
        # get number of disasters declared after end date
        num_of_disasters_declared_after_end_date = len(df_for_disasters_declared_after_end_date)
        return num_of_disasters_declared_after_end_date

    def build_map_of_agents_to_total_claim_cost(
            self):
        """Builds a map of agent and their total claim cost

        Hints:
            An agent with no claims should return 0
            Invalid agent id should have a value of None
            You should round your total_claim_cost to the nearest hundredths

        Returns:
            dict: key is agent id, value is total cost of claims associated to the agent
        """
        # get all agents and their ids
        agent_data_df = self.get_agent_data_df()
        list_of_agent_ids = agent_data_df["id"].to_list()
        # create map for all agents
        map_of_agents_to_total_claim_cost = {key: 0 for key in list_of_agent_ids}
        # go through all claims to calculate total cost
        claim_data_df = self.get_claim_data_df()
        for index, row in claim_data_df.iterrows():
            # get current agent id
            current_agent_id = row["agent_assigned_id"]
            # get estimated cost of current claim
            current_estimate_cost = row["estimate_cost"]
            # check if agent id is valid
            # add current cost to map if agent is valid and use None as value if not
            if current_agent_id not in map_of_agents_to_total_claim_cost:
                map_of_agents_to_total_claim_cost[current_agent_id] = None
            else:
                map_of_agents_to_total_claim_cost[current_agent_id] += current_estimate_cost
        
        # round values of the map to 2 decimals
        map_of_agents_to_total_claim_cost = {
            key : round(map_of_agents_to_total_claim_cost[key], 2) for key in map_of_agents_to_total_claim_cost
                                             }
        return map_of_agents_to_total_claim_cost

    def calculate_disaster_claim_density(
            self, disaster_id):
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
        # get entries of given disaster's claims in the claim dataframe
        claim_data_df = self.get_claim_data_df()
        df_for_claims_of_given_disaster = claim_data_df[
            claim_data_df["disaster_id"] == disaster_id
            ]
        # get the total number of given disaster's claims
        num_of_claims_for_given_disaster = len(df_for_claims_of_given_disaster)
        # return None if disaster does not exist
        if num_of_claims_for_given_disaster == 0:
            return None
        # get entry of given disaster in the disaster dataframe
        disaster_data_df = self.get_disaster_data_df()
        df_for_given_disaster = disaster_data_df[
            disaster_data_df["id"] == disaster_id
            ]
        # get radius of given disaster from entry
        radius_of_given_disaster = df_for_given_disaster.iloc[0]["radius_miles"]
        # calculate area of disaster using A = PI * r^2
        area_of_given_disaster = math.pi * math.pow(radius_of_given_disaster, 2)
        # calculate density using D = N / A and round to 5 decimals
        density_of_claims_to_disaster = round(num_of_claims_for_given_disaster / area_of_given_disaster, 5)
        return density_of_claims_to_disaster

    # endregion

    # region TestSetFour

    def get_top_three_months_with_highest_num_of_claims_desc(
            self):
        """Gets the top three months with the highest total claim cost

        Hint:
            Month should be full name like 01 is January and 12 is December
            Year should be full four-digit year
            List should be in descending order

        Returns:
            list: three strings of month and year, descending order of highest claims
        """
        
        # create function for getting the last day of current date's month
        def get_last_day_of_current_month(
                date):
            return (date.replace(day = 1) + timedelta(days = 32)).replace(day = 1) \
                - timedelta(days = 1)
        
        # create function for getting the first day of current date's next month
        def get_first_day_of_next_month(
                date):
            return (date.replace(day = 1) + timedelta(days = 32)).replace(day = 1)
        
        # create function for finding total costs of each disaster
        def get_total_costs_of_each_disaster(
                list_of_disaster_ids, claim_data_df):
            dict_for_total_claim_cost_of_given_disaster = {}
            for current_disaster_id in list_of_disaster_ids:
                # find all claims of current disaster
                df_for_claims_of_current_disaster = claim_data_df[
                    claim_data_df["disaster_id"] == current_disaster_id
                ]
                # calculate total claim cost by summing claim costs
                dict_for_total_claim_cost_of_given_disaster[current_disaster_id] = \
                    df_for_claims_of_current_disaster["estimate_cost"].sum()
            return dict_for_total_claim_cost_of_given_disaster
        
        # create function for assigning costs to each month involved
        def assign_costs_to_each_month_involved(
                list_of_disaster_ids, 
                dict_for_total_claim_cost_of_given_disaster,
                claim_data_df,
                disaster_data_df):
            dict_for_total_costs_by_month = {}
            for current_disaster_id in list_of_disaster_ids:
                dict_for_given_disaster = disaster_data_df[
                    disaster_data_df["id"] == current_disaster_id
                ].iloc[0]
                start_date = datetime.strptime(dict_for_given_disaster["start_date"], "%Y-%m-%d")
                end_date = datetime.strptime(dict_for_given_disaster["end_date"], "%Y-%m-%d")
                # assign cost for each month
                total_cost_for_given_disaster = \
                    dict_for_total_claim_cost_of_given_disaster[current_disaster_id]
                # find unit cost for each day of disaster
                total_days_of_disaster = (end_date - start_date).days
                unit_cost_for_each_day_of_disaster = total_cost_for_given_disaster / total_days_of_disaster
                # assign cost to each month
                current_date = start_date
                while current_date <= end_date:
                    current_month_str = current_date.strftime("%B %Y")
                
                    last_day_of_current_month = get_last_day_of_current_month(current_date)
                    first_day_of_next_month = get_first_day_of_next_month(current_date)
                    # find number of days of disaster in given month
                    num_of_days_of_disaster_of_current_month = 0
                    if end_date > last_day_of_current_month:
                        num_of_days_of_disaster_of_current_month = \
                            (last_day_of_current_month - current_date).days
                    else:
                        num_of_days_of_disaster_of_current_month = \
                            (end_date - current_date).days
                    cost_for_current_month = unit_cost_for_each_day_of_disaster \
                        * num_of_days_of_disaster_of_current_month
                    
                    if current_month_str not in dict_for_total_costs_by_month:
                        dict_for_total_costs_by_month[current_month_str] = cost_for_current_month
                    else:
                        dict_for_total_costs_by_month[current_month_str] += cost_for_current_month
                    
                    # go to next month if end date is bigger than end of current month or stop here if not
                    if end_date >= first_day_of_next_month:
                        current_date = first_day_of_next_month
                    else:
                        break
            return dict_for_total_costs_by_month
        
        
        # get all disaster ids in the disaster dataframe
        claim_data_df = self.get_claim_data_df()
        disaster_data_df = self.get_disaster_data_df()
        list_of_disaster_ids = disaster_data_df["id"].to_list()
        # find total cost for each disaster
        dict_for_total_claim_cost_of_given_disaster = get_total_costs_of_each_disaster(
                                                        list_of_disaster_ids, claim_data_df)
        # assign costs to each month involved
        dict_for_total_costs_by_month = assign_costs_to_each_month_involved(
            list_of_disaster_ids, dict_for_total_claim_cost_of_given_disaster, 
            claim_data_df, disaster_data_df)
        # get the top 3 months with highest total claim cost
        top_three_months_with_highest_total_claim_cost = sorted(
            dict_for_total_costs_by_month, key=dict_for_total_costs_by_month.get, reverse=True)[:3]
        return top_three_months_with_highest_total_claim_cost

    # endregion
