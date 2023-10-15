import json
import math
import pandas as pd
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

    def get_num_closed_claims(self):  #: z
        """Calculates the number of claims where that status is "Closed"

        Returns:
            int: number of closed claims
        """
        df = pd.DataFrame(self.get_claim_data())

        return len(df[df["status"] == "Closed"])

    def get_num_claims_for_claim_handler_id(self, claim_handler_id):
        """Calculates the number of claims assigned to a specific claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            int: number of claims assigned to claim handler
        """
        df = pd.DataFrame(self.get_claim_data())

        handler_df = df[df["claim_handler_assigned_id"] == claim_handler_id]

        return len(handler_df)

    def get_num_disasters_for_state(self, state):  #: z
        """Calculates the number of disasters for a specific state

        Args:
            state (string): name of a state in the United States of America,
                            including the District of Columbia

        Returns:
            int: number of disasters for state
        """
        df = pd.DataFrame(self.get_disaster_data())

        return len(df[df["state"] == state])

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
        df = pd.DataFrame(self.get_claim_data())

        filtered_df = df[df["disaster_id"] == disaster_id]

        if len(filtered_df) == 0:
            return None

        ketotal_cost = round(filtered_df["estimate_cost"].sum(), 2)

        return total_cost

    def get_average_claim_cost_for_claim_handler(self, claim_handler_id):  #: z
        """Gets the average estimated cost of all claims assigned to a claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            float | None : average cost of claims, rounded to the nearest hundredths place
                           or None if no claims are found
        """
        df = pd.DataFrame(self.get_claim_data())

        needed_data = df[df["claim_handler_assigned_id"] == claim_handler_id][
            "estimate_cost"
        ]
        if needed_data is None or len(needed_data) == 0:
            return None

        return round(mean(needed_data), 2)

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
        data = self.get_disaster_data()
        df = pd.DataFrame(data)

        state_counts = df.groupby("state").agg({"id": "nunique"}).reset_index()

        state_counts = state_counts.sort_values(
            by=["id", "state"], ascending=[False, True]
        )

        return state_counts.iloc[0]["state"]

    def get_state_with_least_disasters(self):  #: z
        """Returns the name of the state with the least disasters based on disaster data

        If two states have the same number of disasters, then sort by alphabetical (a-z)
        and take the first.

        Example: Say New Mexico and West Virginia both have the least number of disasters at
                 1 disaster each. Then, this method would return "New Mexico" since "N"
                 comes before "W" in the alphabet.

        Returns:
            string: single name of state
        """
        df = pd.DataFrame(self.get_disaster_data())

        states_and_counts = df["state"].value_counts()

        #: remove all states that don't have the amount of the last state (lowest amount)
        least_states = states_and_counts[states_and_counts == states_and_counts[-1]]

        #: sort alphabetically
        least_states.sort_index(inplace=True)

        #: return first state in list
        return least_states.index[0]

    def get_most_spoken_agent_language_by_state(self, state):
        """Returns the name of the most spoken language by agents (besides English) for a specific state

        Args:
            state (string): name of state

        Returns:
            string: name of language
                    or empty string if state doesn't exist
        """
        df = pd.DataFrame(self.get_agent_data())

        state_agents = df[
            (df["state"] == state)
            & (df["secondary_language"].notnull())
            & (df["secondary_language"] != "English")
        ]

        if state_agents.empty:
            return ""

        most_common_language = (
            state_agents["secondary_language"].value_counts().idxmax()
        )

        return most_common_language

    def get_num_of_open_claims_for_agent_and_severity(
        self, agent_id, min_severity_rating
    ):  #: z
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
        df = pd.DataFrame(self.get_claim_data())

        #: Severity rating scale for claims is 1 to 10, inclusive.
        if not (1 <= min_severity_rating <= 10):
            return -1

        claims = df[
            (df["agent_assigned_id"] == agent_id)  #: get all claims for agent
            & (df["status"] != "Closed")  #: remove all closed claims
            & (
                df["severity_rating"] >= min_severity_rating
            )  #: remove all claims with lower severity rating
        ]

        if claims_length := len(claims) == 0:
            return None

        return claims_length

    # endregion

    # region TestSetThree

    def get_num_disasters_declared_after_end_date(self):
        """Gets the number of disasters where it was declared after it ended

        Returns:
            int: number of disasters where the declared date is after the end date
        """
        df = pd.DataFrame(self.get_disaster_data())

        late_declaration = df[df["declared_date"] > df["end_date"]]

        return len(late_declaration)

    def build_map_of_agents_to_total_claim_cost(self):  #: z
        """Builds a map of agent and their total claim cost

        Hints:
            An agent with no claims should return 0
            Invalid agent id should have a value of None
            You should round your total_claim_cost to the nearest hundredths

        Returns:
            dict: key is agent id, value is total cost of claims associated to the agent
        """

        claims_df = pd.DataFrame(self.get_claim_data())
        agent_df = pd.DataFrame(self.get_agent_data())

        agent_ids = agent_df["id"].unique()
        costs = {}

        for agent_id in agent_ids:
            #: Get agent's claims
            agent_df = claims_df[claims_df["agent_assigned_id"] == agent_id]

            if len(agent_df) != 0:
                costs[agent_id] = round(agent_df["estimate_cost"].sum(), 2)
            else:
                costs[agent_id] = 0  #: No claims case

        #: This covers None (Invalid agent id) cases as well, since .get will return None if key doesn't exist

        return costs

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
        df_disaster = pd.DataFrame(self.get_disaster_data())
        df_claim = pd.DataFrame(self.get_claim_data())

        disaster_row = df_disaster[df_disaster["id"] == disaster_id]

        if disaster_row.empty:
            return None

        num_claims = df_claim[df_claim["disaster_id"] == disaster_id].shape[0]

        radius = disaster_row.iloc[0]["radius_miles"]

        area = math.pi * (radius**2)
        density = num_claims / area

        return round(density, 5)

    # endregion

    # region TestSetFour

    def get_top_three_months_with_highest_num_of_claims_desc(self):  #: z
        """Gets the top three months with the highest total claim cost

        Hint:
            Month should be full name like 01 is January and 12 is December
            Year should be full four-digit year
            List should be in descending order

        Returns:
            list: three strings of month and year, descending order of highest claims
        """

        #: Load data
        claims_df = pd.DataFrame(self.get_claim_data())
        disaster_df = pd.DataFrame(self.get_disaster_data())

        #: Shorten lists
        claims_df = claims_df[["disaster_id"]]
        disaster_df = disaster_df[["id", "declared_date"]]

        #: Merge data & calculate month_year
        merged_df = pd.merge(
            claims_df, disaster_df, left_on="disaster_id", right_on="id"
        )
        merged_df["month_year"] = pd.to_datetime(
            merged_df["declared_date"]
        ).dt.strftime("%B %Y")

        #: Group by month_year and count month_years
        grouped_df = merged_df.groupby("month_year").size().reset_index(name="count")
        grouped_df = grouped_df.sort_values(by="count", ascending=False)

        #: Return top 3 month_years
        return grouped_df["month_year"].head(3).tolist()

    # endregion
