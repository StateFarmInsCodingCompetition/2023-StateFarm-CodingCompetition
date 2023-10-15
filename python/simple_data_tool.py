import json
import math
from statistics import mean
import matplotlib.pyplot as plt
import numpy as np

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
        claim_data = self.get_claim_data()
        closed = 0
        for claim in claim_data:
            if(claim['status'] == "Closed"): # Checks to see if each claim is closed
                closed += 1
        """Calculates the number of claims where that status is "Closed"
        
        Returns:
            int: number of closed claims
        """
        return closed

    def get_num_claims_for_claim_handler_id(self, claim_handler_id):
        claim_data = self.get_claim_data()
        num = 0
        for claim in claim_data:
            if(claim['claim_handler_assigned_id'] == claim_handler_id): # Checks to see if the claim has the correct claim handler id
                num += 1
        """Calculates the number of claims assigned to a specific claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            int: number of claims assigned to claim handler
        """
        return num

    def get_num_disasters_for_state(self, state):
        disaster_data = self.get_disaster_data()
        num = 0
        for disaster in disaster_data:
            if(disaster['state'] == state): # Checks to see if disaster has correct state
                num += 1
        """Calculates the number of disasters for a specific state

        Args:
            state (string): name of a state in the United States of America,
                            including the District of Columbia

        Returns:
            int: number of disasters for state
        """
        return num

    # endregion

    # region Test Set Two

    def get_total_claim_cost_for_disaster(self, disaster_id):
        claim_data = self.get_claim_data()
        total = 0.0
        for claim in claim_data:
            if(claim['disaster_id'] == disaster_id): # checks to see if claim has correct disaster id and adds the cost if so
                total += claim['estimate_cost']
        """Sums the estimated cost of a specific disaster by its claims

        Args:
            disaster_id (int): id of disaster

        Returns:
            float | None: estimate cost of disaster, rounded to the nearest hundredths place
                          returns None if no claims are found
        """
        if(total == 0.0): # checks if any disasters with the id were found
            return
        return total

    def get_average_claim_cost_for_claim_handler(self, claim_handler_id):
        claim_data = self.get_claim_data()
        sum = 0
        num = 0
        for claim in claim_data:
            if(claim['claim_handler_assigned_id'] == claim_handler_id): # checks if claim has correct claim handler id and adds cost if so
                sum += claim['estimate_cost']
                num += 1
        """Gets the average estimated cost of all claims assigned to a claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            float | None : average cost of claims, rounded to the nearest hundredths place
                           or None if no claims are found
        """
        if(num == 0): # checks if any disasters with the claim handler id were found
            return
        return round(sum/num,2) # computes average and rounds to the nearest cent

    def get_state_with_most_disasters(self):
        disaster_data = self.get_disaster_data()
        state_counts = {} # creates map
        for disaster in disaster_data: # updates map according to state
            if(state_counts.__contains__(disaster['state'])): # checks if the state is in the map
                state_counts[disaster['state']] += 1
            else:
                state_counts[disaster['state']] = 1 # adds state to map
        state_counts = dict(sorted(state_counts.items())) # sorts map alphabetically

        """Returns the name of the state with the most disasters based on disaster data

        If two states have the same number of disasters, then sort by alphabetical (a-z)
        and take the first.

        Example: Say New Jersey and Delaware both have the highest number of disasters at
                 12 disasters each. Then, this method would return "Delaware" since "D"
                 comes before "N" in the alphabet. 

        Returns:
            string: single name of state
        """
        return max(state_counts, key=state_counts.get) # gets state with most disasters

    def get_state_with_least_disasters(self):
        disaster_data = self.get_disaster_data()
        state_counts = {} # creates map
        for disaster in disaster_data: # updates map according to state
            if(state_counts.__contains__(disaster['state'])): # checks if the state is in the map
                state_counts[disaster['state']] += 1
            else:
                state_counts[disaster['state']] = 1 # adds state to map
        state_counts = dict(sorted(state_counts.items())) # sorts map alphabetically
        """Returns the name of the state with the least disasters based on disaster data

        If two states have the same number of disasters, then sort by alphabetical (a-z)
        and take the first.

        Example: Say New Mexico and West Virginia both have the least number of disasters at
                 1 disaster each. Then, this method would return "New Mexico" since "N"
                 comes before "W" in the alphabet. 

        Returns:
            string: single name of state
        """
        return min(state_counts,key=state_counts.get) # gets state with least disasters
    
    def get_most_spoken_agent_language_by_state(self, state):
        agent_data = self.get_agent_data()
        language_counts = {} # creates map
        for agent in agent_data:
            if(agent['state'] == state): # checks if agent is in correct state
                if(language_counts.__contains__(agent['secondary_language'])): # checks if the language exists in the map
                    language_counts[agent['secondary_language']] += 1
                else: 
                    language_counts[agent['secondary_language']] = 1 # adds language to map
                #repeated for primary language
                if(language_counts.__contains__(agent['primary_language'])): # checks if the language exists in the map
                    language_counts[agent['primary_language']] += 1
                else: 
                    language_counts[agent['primary_language']] = 1 # adds language to map               
        language_counts = dict(sorted(language_counts.items())) # sorts map alphabetically
        if(language_counts.__contains__("English")): # deletes English from the language map
            language_counts.__delitem__("English")
        """Returns the name of the most spoken language by agents (besides English) for a specific state

        Args:
            state (string): name of state

        Returns:
            string: name of language
                    or empty string if state doesn't exist
        """
        if(len(language_counts) == 0): # checks if map is empty
            return ""
        return max(language_counts,key=language_counts.get) # gets language with most speakers

    def get_num_of_open_claims_for_agent_and_severity(self, agent_id, min_severity_rating):
        if(min_severity_rating < 1 or min_severity_rating > 10): # check for invalid severity rating
            return -1
        claim_data = self.get_claim_data()
        num = 0
        hasClaim = False
        for claim in claim_data:
            if(not(hasClaim) and claim['agent_assigned_id'] == agent_id): # checks if agent has any claims
                hasClaim = True
            # checks if all fields are correct
            if(claim['agent_assigned_id'] == agent_id and claim['severity_rating'] >= min_severity_rating and claim['status'] != "Closed"):
                num += 1
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
        if(not(hasClaim)): # checks if there are no claims for the agent
            return 
        return num

    # endregion

    # region TestSetThree

    def get_num_disasters_declared_after_end_date(self):
        disaster_data = self.get_disaster_data()
        num = 0
        for disaster in disaster_data:
            if(disaster['end_date'] < disaster['declared_date']): # checks if the disaster ended before it was declared
                num += 1
        """Gets the number of disasters where it was declared after it ended

        Returns:
            int: number of disasters where the declared date is after the end date
        """
        return num

    def build_map_of_agents_to_total_claim_cost(self):
        agent_map = {} # create map
        agent_data = self.get_agent_data()
        for i in range(1,len(agent_data)+1): # assign every valid agent id to 0
            agent_map[i] = 0.0
        claim_data = self.get_claim_data()
        for claim in claim_data: 
            agent_map[claim['agent_assigned_id']] += claim['estimate_cost'] # add claim costs to correct agent id
        for i in range(1,len(agent_data)+1): # get rid of rounding errors in the adding
            agent_map[i] = round(agent_map[i],2)

        """Builds a map of agent and their total claim cost

        Hints:
            An agent with no claims should return 0
            Invalid agent id should have a value of None
            You should round your total_claim_cost to the nearest hundredths

        Returns:
            dict: key is agent id, value is total cost of claims associated to the agent
        """
        return agent_map

    def calculate_disaster_claim_density(self, disaster_id):
        disaster_data = self.get_disaster_data()
        if(disaster_id > len(disaster_data)): # checks for invalid disaster_id
            return 
        claim_data = self.get_claim_data()
        radius = disaster_data[disaster_id-1]['radius_miles'] # get disaster radius
        area = radius*radius*math.pi # gets disaster area
        num = 0
        for claim in claim_data:
            if(claim['disaster_id'] == disaster_id): # checks if the disaster id matches
                num += 1
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
        return round(num/area,5) # calculates and rounds disaster density

    # endregion

    # region TestSetFour

    def get_top_three_months_with_highest_num_of_claims_desc(self):
        claim_data = self.get_claim_data()
        disaster_data = self.get_disaster_data()
        month_count = {} # initlaize dict
        for claim in claim_data:
            disaster_id = claim['disaster_id'] # get disaster_id of claim
            month = disaster_data[disaster_id-1]['declared_date'][0:7] # get declared_date of disaster
            if(month_count.__contains__(month)): # add the cost to the correct month in the dict
                month_count[month] += claim['estimate_cost']
            else:
                month_count[month] = claim['estimate_cost']
        for month in month_count.keys():
            month_count[month] = round(month_count[month],2)
        month_count = dict(sorted(month_count.items()))
        top_three = []
        # map for traslation from 2 digit month number to name of month
        month_num_to_name = {"01":"January","02":"February","03":"March","04":"April","05":"May","06":"June","07":"July","08":"August","09":"September","10":"October","11":"November","12":"December"}
        for i in range(3): # gets top three total cost
            top = max(month_count,key=month_count.get)
            top_three.append(month_num_to_name[top[5:7]] + " " + top[0:4]) # formats string correctly
            month_count.__delitem__(top) # removes the prevous maximum
        
        """Gets the top three months with the highest total claim cost

        Hint:
            Month should be full name like 01 is January and 12 is December
            Year should be full four-digit year
            List should be in descending order

        Returns:
            list: three strings of month and year, descending order of highest claims
        """
        return top_three

    # endregion

    # extras
    def get_top_three_disaster_types(self): # seeing what disaster types are most common
        disaster_data = self.get_disaster_data()
        disaster_types = {} # creates map
        for disaster in disaster_data:
            if(disaster_types.__contains__(disaster['type'])): # updates map for each disaster
                disaster_types[disaster['type']] += 1
            else:
                disaster_types[disaster['type']] = 1
        top_three = []
        for i in range(3): # gets top three disaster types
            top = max(disaster_types,key=disaster_types.get)
            top_three.append(top)
            disaster_types.__delitem__(top) # removes the previous maximum
        return top_three
    def plot_severity_rating_to_cost(self): # plotting cost vs severity rating
        claim_data = self.get_claim_data()
        severity_ratings = []
        costs = []
        for claim in claim_data: # creating lists
            severity_ratings.append(claim['severity_rating'])
            costs.append(claim['estimate_cost'])
        severity_ratings = np.array(severity_ratings) # convert lists to numpy arrays
        costs = np.array(costs)
        plt.title("Cost vs Severity Rating")
        plt.xlabel("Severity Rating")
        plt.ylabel("Cost")
        a,b = np.polyfit(severity_ratings,costs,1) # compute best fit line
        plt.scatter(severity_ratings,costs)
        plt.plot(severity_ratings,a*severity_ratings+b)
        plt.show()

if (__name__ == "__main__"):
    a = SimpleDataTool()
    a.__init__()
    print(a.get_top_three_disaster_types())
    a.plot_severity_rating_to_cost()