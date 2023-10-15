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
        
        closedClaims = 0
        for claim in self.get_claim_data():
            if claim.get("status") == 'Closed':
                closedClaims += 1
        
        return closedClaims
    
        pass

    def get_num_claims_for_claim_handler_id(self, claim_handler_id):
        """Calculates the number of claims assigned to a specific claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            int: number of claims assigned to claim handler
        """
        
        theirClaims = 0
        for claim in self.get_claim_data():
            if claim.get("claim_handler_assigned_id")==claim_handler_id:
                theirClaims += 1
        
        return theirClaims
    
        pass

    def get_num_disasters_for_state(self, state):
        """Calculates the number of disasters for a specific state

        Args:
            state (string): name of a state in the United States of America,
                            including the District of Columbia

        Returns:
            int: number of disasters for state
        """
        
        statesDisasters = 0
        for disaster in self.get_disaster_data():
            if disaster.get("state") == state:
                statesDisasters += 1
        
        return statesDisasters
        
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
        totalCost = 0
        
        for claim in self.get_claim_data():
            if claim.get("disaster_id") == disaster_id:
                totalCost += claim.get("estimate_cost")
                
        if totalCost==0:
            return None
            
        return totalCost
        

        pass

    def get_average_claim_cost_for_claim_handler(self, claim_handler_id):
        """Gets the average estimated cost of all claims assigned to a claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            float | None : average cost of claims, rounded to the nearest hundredths place
                           or None if no claims are found
        """
        
        averageCost = 0
        totalClaims = 0
        
        for claim in self.get_claim_data():
            if claim.get("claim_handler_assigned_id") == claim_handler_id:
                averageCost += claim.get("estimate_cost")
                totalClaims += 1
        
        if totalClaims == 0:
            return None
        
        return round(averageCost/totalClaims, 2)

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
        states = []
        for region in self.REGION_MAP:
            states+= self.REGION_MAP.get(region).split(",")
        
        statesDisasters = {}
        for disaster in self.get_disaster_data():
            if disaster.get("state") in statesDisasters:
                statesDisasters[disaster.get("state")] +=1
            else:
                statesDisasters[disaster.get("state")] = 1
        
        max = 0
        maxStates=[]
        for state in statesDisasters:
            if statesDisasters.get(state) > max:
                maxStates = []
                maxStates.append(state)
                max = statesDisasters.get(state)
            elif statesDisasters.get(state) == max:
                maxStates.append(state)
        
        return sorted(maxStates)[0]

        
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
        
        states = []
        for region in self.REGION_MAP:
            states+= self.REGION_MAP.get(region).split(",")
        
        statesDisasters = {}
        for disaster in self.get_disaster_data():
            if disaster.get("state") in statesDisasters:
                statesDisasters[disaster.get("state")] +=1
            else:
                statesDisasters[disaster.get("state")] = 1
        
        min = statesDisasters.get(list(statesDisasters.keys())[0])
        minStates=[list(statesDisasters.keys())[0]]
        for state in statesDisasters:
            if statesDisasters.get(state) < min:
                minStates = []
                minStates.append(state)
                min = statesDisasters.get(state)
            elif statesDisasters.get(state) == min:
                minStates.append(state)
        
        return sorted(minStates)[0]
        pass
    
    def get_most_spoken_agent_language_by_state(self, state):
        """Returns the name of the most spoken language by agents (besides English) for a specific state

        Args:
            state (string): name of state

        Returns:
            string: name of language
                    or empty string if state doesn't exist
        """
        
        language = ""
        max = 0
        languageMaxes = {}

        for agent in self.get_agent_data():
            if agent.get("state") == state:
                if agent.get("secondary_language") in languageMaxes:
                    languageMaxes[agent.get("secondary_language")] += 1
                else:
                    languageMaxes[agent.get("secondary_language")] = 1
        
        if len(languageMaxes) == 0:
            return ''
        values = list(languageMaxes.keys())
        for single in values:
            return single
        
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
        if min_severity_rating > 0 or min_severity_rating < 10:
            return -1
        
        allClaims = 0
        openClaims = 0
        for claim in self.get_claim_data():
            if claim.get("agent_assigned_id") == agent_id:
                allClaims += 1
                if claim.get("severity_rating") >= min_severity_rating and claim.get("status") != "Closed":
                    openClaims += 1
        
        if allClaims == 0:
            return None
        return openClaims

        pass

    # endregion

    # region TestSetThree

    def get_num_disasters_declared_after_end_date(self):
        """Gets the number of disasters where it was declared after it ended

        Returns:
            int: number of disasters where the declared date is after the end date
        """
        num = 0
        for disaster in self.get_disaster_data():
            endDate = disaster.get("end_date").split("-")
            endDate = (int(endDate[0])*365) + (int(endDate[1])*30) + (int(endDate[2]))
            declared = disaster.get("declared_date").split("-")
            declared = (int(declared[0])*365) + (int(declared[1])*30) + (int(declared[2]))
            if declared > endDate:
                num += 1
        
        return num
        

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
        
        agentClaims = {}
        
        for claim in self.get_claim_data():
            if claim.get("claim_handler_assigned_id") in agentClaims:
                agentClaims[claim.get("claim_handler_assigned_id")] += claim.get("estimate_cost")
            else:
                agentClaims[claim.get("claim_handler_assigned_id")] = claim.get("estimate_cost")
                
        for agent in self.get_agent_data():
            if agent.get("id") not in agentClaims:
                agentClaims[agent.get("id")] = 0
                
        return agentClaims

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
        
        count = 0
        area = 0
        
        for disaster in self.get_disaster_data():
            if disaster.get("id") == disaster_id:
                count+= 1
                area += (disaster.get("radius_miles"))*3.14
        
        if count == 0:
            return None
        return count/area
                
        
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
    #get_num_closed_claims(self=self)
