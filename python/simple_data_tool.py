import json
import math

from statistics import mean



class SimpleDataTool:

    AGENTS_FILEPATH = 'python/data/sfcc_2023_agents.json'
    CLAIM_HANDLERS_FILEPATH = 'python/data/sfcc_2023_claim_handlers.json'
    CLAIMS_FILEPATH = 'python/data/sfcc_2023_claims.json'
    DISASTERS_FILEPATH = 'python/data/sfcc_2023_disasters.json'

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
        
        count = 0
        
        # find number of closed claims
        for claim in self.__claim_data:
            if claim['status'] == 'Closed':
                count += 1
                
        #  return count
        return count
        pass

    def get_num_claims_for_claim_handler_id(self, claim_handler_id):
        """Calculates the number of claims assigned to a specific claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            int: number of claims assigned to claim handler
        """
        
        count = 0
        
        # find number of claims for given claim handler
        for claim in self.__claim_data:
            if claim['claim_handler_assigned_id'] == claim_handler_id:
                count += 1
          
        # return count      
        return count
    
        pass

    def get_num_disasters_for_state(self, state):
        """Calculates the number of disasters for a specific state

        Args:
            state (string): name of a state in the United States of America,
                            including the District of Columbia

        Returns:
            int: number of disasters for state
        """

        count = 0
        
        # find number of disasters for given state
        for disaster in self.__disaster_data:
            if disaster['state'] == state:
                count += 1
                
        # return count
        return count
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
    
        total = 0.00
        
        # find total cost of claims for disaster with given id
        for claim in self.__claim_data:
            if claim['disaster_id'] == disaster_id:
                total += claim['estimate_cost']
                
        # make sure total is not 0
        if total > 0:
            return round(total, 2)
        else:
            return None
        
        pass

    def get_average_claim_cost_for_claim_handler(self, claim_handler_id):
        """Gets the average estimated cost of all claims assigned to a claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            float | None : average cost of claims, rounded to the nearest hundredths place
                           or None if no claims are found
        """

        total = 0
        count = 0
        for claim in self.__claim_data:
            if claim['claim_handler_assigned_id'] == claim_handler_id:
                total += claim['estimate_cost']
                count += 1
                
        # make sure count is not 0
        if count > 0:
            return round(total/count, 2)
        
        # if count is 0, return None
        return None
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
        
        state_dict = {}
        
        # find number of disasters for each state
        for disaster in self.__disaster_data:
            if disaster['state'] in state_dict:
                state_dict[disaster['state']] += 1
            else:
                state_dict[disaster['state']] = 1
                
        max_state = ''
        max_count = 0
        
        # find max state
        for state in state_dict:
            if state_dict[state] > max_count:
                max_state = state
                max_count = state_dict[state]
            elif state_dict[state] == max_count:
                if state < max_state:
                    max_state = state
                    max_count = state_dict[state]
            
        # return max state      
        return max_state
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
    
        state_dict = {}
        
        # find number of disasters for each state
        for disaster in self.__disaster_data:
            if disaster['state'] in state_dict:
                state_dict[disaster['state']] += 1
            else:
                state_dict[disaster['state']] = 1
                
        min_state = ''
        min_count = 100
        
        # find min state
        for state in state_dict:
            if state_dict[state] < min_count:
                min_state = state
                min_count = state_dict[state]
            elif state_dict[state] == min_count:
                if state < min_state:
                    min_state = state
                    min_count = state_dict[state]
    
        # return min state
        return min_state
        pass
    
    def get_most_spoken_agent_primary_language_by_state(self, state):
        """Returns the name of the most spoken primary_language by agents (besides English) for a specific state

        Args:
            state (string): name of state

        Returns:
            string: name of primary_language
                    or empty string if state doesn't exist
        """
        agent_dict = {}
        
        # find agents with given state
        for agent in self.__agent_data:
            # add language to dict if it doesn't exist as long as it is not English
            if agent['state'] == state and agent['primary_language'] != 'English':
                if agent['primary_language'] not in agent_dict:
                    agent_dict[agent['primary_language']] = 1
                else:
                    agent_dict[agent['primary_language']] += 1
                    
        # find max language
        max_language = ''
        max_count = 0
        
        # find max language
        for language in agent_dict:
            if agent_dict[language] > max_count:
                max_language = language
                max_count = agent_dict[language]
            if agent_dict[language] == max_count:
                if language < max_language:
                    max_language = language
                    max_count = agent_dict[language]
         
         # return max language
        return max_language
    
        # I am pretty sure this works. I am not sure why it is not passing the test.
        # AttributeError: 'SimpleDataTool' object has no attribute 'get_most_spoken_agent_language_by_state'
        # Its producting this when there is no code in this function
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

        count = 0
        
        # return None if agent does not exist
        if min_severity_rating < 1 or min_severity_rating > 10:
            return -1
        
        # find number of open claims for agent with given id and severity rating
        for claim in self.__claim_data:
            if claim['agent_assigned_id'] == agent_id:
                if claim['severity_rating'] >= min_severity_rating and claim['status'] != 'Closed':
                    count += 1
          
        # return None if count is 0      
        if count == 0:
            return None
        
        # return count
        return count
        pass

    # endregion

    # region TestSetThree

    def get_num_disasters_declared_after_end_date(self):
        """Gets the number of disasters where it was declared after it ended

        Returns:
            int: number of disasters where the declared date is after the end date
        """
        
        count = 0
        
        # find disasters that were declared after they ended
        for disaster in self.__disaster_data:
            if disaster['declared_date'] > disaster['end_date']:
                count += 1
        
        # retun count
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
        
        agent_dict = {}
        
        # add agents to dict
        for agent in self.__agent_data:
            agent_dict[agent['id']] = 0.00
            
        # add claims to dict
        for claim in self.__claim_data:
            if claim['agent_assigned_id'] in agent_dict:
                agent_dict[claim['agent_assigned_id']] += claim['estimate_cost']
           
        # round values to nearest hundredths     
        for agent in agent_dict:
            agent_dict[agent] = round(agent_dict[agent], 2)
           
        # return dict 
        return agent_dict
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
        # sets disaster to the disaster with the given id
        disaster = [disaster for disaster in self.__disaster_data if disaster['id'] == disaster_id]
        
        # if disaster does not exist, return None
        if len(disaster) == 0:
            return None
        
        # sets disaster to the first element in the list
        disaster = disaster[0]
        
        # calculate area of disaster
        radius = disaster['radius_miles']
        area = math.pi * radius**2
        
        count = 0
        
        # calculate number of claims in disaster
        for claim in self.__claim_data:
            if claim['disaster_id'] == disaster_id:
                count += 1
                
        # calculate density
        density = count / area
        
        # round density to nearest thousandths place
        return round(density, 5)
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
    
        month_dict = {}
        
        # create dict with month name is key and month number is value
        month_name_dict = {
            '01': 'January',
            '02': 'February',
            '03': 'March',
            '04': 'April',
            '05': 'May',
            '06': 'June',
            '07': 'July',
            '08': 'August',
            '09': 'September',
            '10': 'October',
            '11': 'November',
            '12': 'December'
        }
        
        
        # add months to dict
        for claim in self.__disaster_data:
            date = claim['declared_date']
            month = date[5:7]
            year = date[:4]
            
            # convert month to full name
            month = month_name_dict[month]
            
            # add in year
            month += ' ' + year
            
            # add month to dict
            if month in month_dict:
                month_dict[month] += 1
            else:
                month_dict[month] = 1
                
        # find top three months
        top_three = []
        
        # find top three months
        for i in range(3):
            max_month = ''
            max_count = 0
            for month in month_dict:
                if month_dict[month] > max_count:
                    max_month = month
                    max_count = month_dict[month]
                elif month_dict[month] == max_count:
                    if month < max_month:
                        max_month = month
                        max_count = month_dict[month]
            top_three.append(max_month)
            month_dict.pop(max_month)
            
            
        # return the top three months
        return top_three
        pass

    # endregion
