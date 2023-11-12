import json
import math
import pandas as pd
from pandas import DataFrame
import datetime as dt

dates = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
         'December']


class SimpleDataTool:
    AGENTS_FILEPATH = '../data/sfcc_2023_agents.json'
    CLAIM_HANDLERS_FILEPATH = '../data/sfcc_2023_claim_handlers.json'
    CLAIMS_FILEPATH = '../data/sfcc_2023_claims.json'
    DISASTERS_FILEPATH = '../data/sfcc_2023_disasters.json'

    REGION_MAP = {
        'west': 'Alaska,Hawaii,Washington,Oregon,California,Montana,Idaho,Wyoming,Nevada,Utah,Colorado,Arizona,New Mexico',
        'midwest': 'North Dakota,South Dakota,Minnesota,Wisconsin,Michigan,Nebraska,Iowa,Illinois,Indiana,Ohio,Missouri,Kansas',
        'south': 'Oklahoma,Texas,Arkansas,Louisiana,Kentucky,Tennessee,Mississippi,Alabama,West Virginia,Virginia,North Carolina,South Carolina,Georgia,Florida',
        'northeast': 'Maryland,Delaware,District of Columbia,Pennsylvania,New York,New Jersey,Connecticut,Massachusetts,Vermont,New Hampshire,Rhode Island,Maine'
    }

    def __reload_data(self):
        self.__agent_data = self.__client['agents']
        self.__claim_handler_data = self.__client['claim_handlers']
        self.__claim_data = self.__client['claims']
        self.__disaster_data = self.__client['disasters']
        # self.__agent_data = self.load_json_from_file(self.AGENTS_FILEPATH)
        # self.__claim_handler_data = self.load_json_from_file(
        #     self.CLAIM_HANDLERS_FILEPATH)
        # self.__claim_data = self.load_json_from_file(self.CLAIMS_FILEPATH)
        # self.__disaster_data = self.load_json_from_file(
        #     self.DISASTERS_FILEPATH)

    def __init__(self, client):
        self.__client = client['statefarm_data']
        self.__reload_data()

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

        # converting JSON to pd dataframe
        df = pd.json_normalize(self.get_claim_data())

        # filtering the data
        res = df.loc[df['status'] == 'Closed']

        return len(res.index)

    def get_num_claims_for_claim_handler_id(self, claim_handler_id: int):
        """Calculates the number of claims assigned to a specific claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            int: number of claims assigned to claim handler
        """
        df = pd.json_normalize(self.get_claim_data())
        res = df.loc[df['claim_handler_assigned_id'] == claim_handler_id]
        return len(res.index)

    def get_num_disasters_for_state(self, state: str):
        """Calculates the number of disasters for a specific state

        Args:
            state (string): name of a state in the United States of America,
                            including the District of Columbia

        Returns:
            int: number of disasters for state
        """
        df = pd.json_normalize(self.get_disaster_data())
        res = df.loc[df['state'] == state]
        return len(res.index)

    # endregion

    # region Test Set Two

    def get_total_claim_cost_for_disaster(self, disaster_id: int):
        """Sums the estimated cost of a specific disaster by its claims

        Args:
            disaster_id (int): id of disaster

        Returns:
            float | None: estimate cost of disaster, rounded to the nearest hundredths place
                          returns None if no claims are found
        """
        df = pd.json_normalize(self.get_claim_data())
        related = df.loc[df['disaster_id'] == disaster_id]

        # summing the estimate cost for specified disaster
        res = related['estimate_cost'].sum()
        if res == 0:
            res = None
        return res

    def get_average_claim_cost_for_claim_handler(self, claim_handler_id: int):
        """Gets the average estimated cost of all claims assigned to a claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            float | None : average cost of claims, rounded to the nearest hundredths place
                           or None if no claims are found
        """
        df = pd.json_normalize(self.get_claim_data())
        related = df.loc[df['claim_handler_assigned_id'] == claim_handler_id]
        if related.empty:
            return None


        # average of estiamte cost for specified disaster
        res = related['estimate_cost'].mean()
        if res == 0:
            res = None
        else:
            res = round(res, 2)
        return res

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
        df = pd.json_normalize(self.get_disaster_data())

        # creating frequency table, then sorting the values
        related: DataFrame = df['state'].value_counts().reset_index(drop=False)
        related.sort_values(by=['count', 'state'], ascending=[False, True], inplace=True)
        res = related['state'].iloc[0]
        return res

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

        # same as above function
        df = pd.json_normalize(self.get_disaster_data())
        related: DataFrame = df['state'].value_counts().reset_index(drop=False)
        related.sort_values(by=['count', 'state'], ascending=[True, True], inplace=True)
        res = related['state'].iloc[0]
        return res

    def get_most_spoken_agent_language_by_state(self, state: str):
        """Returns the name of the most spoken language by agents (besides English) for a specific state

        Args:
            state (string): name of state

        Returns:
            string: name of language
                    or empty string if state doesn't exist
        """
        df = pd.DataFrame(list(self.get_agent_data().find()))
        df = df.loc[df['state'] == state]

        # creating frequency tables for the languages
        primary: DataFrame = df['primary_language'].value_counts().reset_index(drop=False)
        secondary = df['secondary_language'].value_counts().reset_index(drop=False)

        primary.columns = ['language', 'count']
        secondary.columns = ['language', 'count']

        # combining them to get dataframe with all languages
        merged = pd.concat([primary, secondary])
        if merged.empty:
            return ''

        res = merged['language'].iloc[0]
        if res == 'English':
            res = merged['language'].iloc[1]

        return res

    def get_num_of_open_claims_for_agent_and_severity(self, agent_id: int, min_severity_rating: int):
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

        df = pd.json_normalize(self.get_claim_data())
        res = df.loc[(df['agent_assigned_id'] == agent_id)
                          & (df['severity_rating'] >= min_severity_rating)
                          & (df['status'] != 'Closed')]
        if res.empty:
            return None
        return len(res.index)

    # endregion

    # region TestSetThree

    def get_num_disasters_declared_after_end_date(self):
        """Gets the number of disasters where it was declared after it ended

        Returns:
            int: number of disasters where the declared date is after the end date
        """

        df = pd.json_normalize(self.get_disaster_data())
        res = df.loc[df['end_date'] < df['declared_date']]
        return len(res.index)

    def build_map_of_agents_to_total_claim_cost(self):
        """Builds a map of agent and their total claim cost

        Hints:
            An agent with no claims should return 0
            Invalid agent id should have a value of None
            You should round your total_claim_cost to the nearest hundredths

        Returns:
            dict: key is agent id, value is total cost of claims associated to the agent
        """

        # getting total of estimate cost for each agent, and filling 0 for any empty costs
        df = pd.json_normalize(self.get_claim_data())
        res = df.groupby('agent_assigned_id')['estimate_cost'].sum().round(2).to_frame()
        res = res.reindex(range(1, 101), fill_value=0).reset_index()

        return pd.Series(res.estimate_cost.values, index=res.agent_assigned_id).to_dict()

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
        df = pd.json_normalize(self.get_claim_data())
        related = df.loc[df['disaster_id'] == disaster_id]
        if related.empty:
            return None

        num = len(related.index)

        df2 = pd.json_normalize(self.get_disaster_data())

        # matching disaster id to the radius
        radius = df2.loc[df2['id'] == disaster_id]['radius_miles'].iloc[0]

        return round(num / (math.pi * radius ** 2), 5)

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

        df = pd.json_normalize(self.get_claim_data())
        related = df['disaster_id'].value_counts().reset_index(drop=False)

        df2 = pd.json_normalize(self.get_disaster_data())
        related = related.map(str)

        # getting the month and year for each disaster id
        for i, row in related.iterrows():
            date = dt.datetime.strptime(df2.loc[df2['id'] == int(row.iloc[0])]['declared_date'].iloc[0],
                                        '%Y-%m-%d')
            row.iloc[0] = dates[date.month - 1] + ' ' + str(date.year)

        related['count'] = related['count'].astype(int)

        # getting the total count for each month/year
        related = related.groupby('disaster_id')['count'].sum().to_frame().reset_index()  # xd now its actually month:count
        related.columns = ['month', 'count']
        related.sort_values(by=['count'], ascending=[False], inplace=True)

        return [related['month'].iloc[0], related['month'].iloc[1], related['month'].iloc[2]]

    # endregion
