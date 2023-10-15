import json
import math
from data import *
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
        return sum(1 for data in self.get_claim_data() if data['status'] == "closed")

    def get_num_claims_for_claim_handler_id(self, claim_handler_id):
        return sum(1 for data in self.get_claim_data() if data["claim_handler_assigned_id"] == claim_handler_id)

    def get_num_disasters_for_state(self, state):
        return sum(1 for data in self.get_disaster_data() if data["state"] == state)

        # endregion

    # region Test Set Two

    def get_total_claim_cost_for_disaster(self, disaster_id):
        disasterData = self.get_claim_data()

        costs = sum(data["estimate_cost"] for data in disasterData if data['disaster_id'] == disaster_id)

        if costs == 0:
            return None
        else:
            return costs

    def get_average_claim_cost_for_claim_handler(self, claim_handler_id):
        claimData = self.get_claim_data()

        totals = []
        for data in claimData:
            if data["claim_handler_assigned_id"] == claim_handler_id:
                totals += [data["estimate_cost"]]

        if len(totals) == 0:
            return None
        else:
            return sum(totals) / len(totals)


    def get_state_with_most_disasters(self):

        disasterData = self.get_disaster_data()

        counts = {}
        for data in disasterData:
            state = data["state"]
            counts[state] = counts[state] + 1

        maxVal = max(counts.values())

        topStates = [key for key, value in counts.items() if maxVal == value]

        topStates.sort()

        return topStates[0]










    def get_state_with_least_disasters(self):
        disasterData = self.get_disaster_data()

        counts = {}
        for data in disasterData:
            state = data["state"]
            counts[state] = counts[state] + 1

        minVal = min(counts.values())

        topStates = [key for key, value in counts.items() if minVal == value]

        for key, value in counts.items():
            if minVal == value:
                topStates.append(key)

        topStates.sort()

        return topStates[0]
    
    def get_most_spoken_agent_language_by_state(self, state):


        agentData = self.get_agent_data()

        agentsForState = [data["id"] for data in agentData if data["state"] == state]

        if len(agentsForState) == 0:
            return ''

        counts = {}
        for agent in agentsForState:
            primLang = agentData[agent]["primary_language"]
            secLang = agentData[agent]["secondary_language"]
            counts[primLang] = counts[primLang] + 1
            counts[secLang] = counts[secLang] + 1

        maxVal = max(counts.values())

        topLangs = [key for key, value in counts if value == maxVal]

        topLangs.remove('English')
        topLangs.sort()
        return topLangs[0]



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
        disasterData = self.get_disaster_data()

        declared = [data["declared_date"].split('-') for data in disasterData]
        end = [data["end_date"].split('-') for data in disasterData]

        count = 0
        for d, e in zip(declared, end):
            if d[0] > e[0]:
                count += 1
            elif d[1] > e[1]:
                count += 1
            elif d[2] > e[2]:
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
