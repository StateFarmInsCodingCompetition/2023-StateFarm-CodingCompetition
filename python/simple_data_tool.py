"""
Name: Kristen "Elaine" Waddle
Date: 10/14/2023

"""


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
        claimnum = 0
        for i in range(len((self.get_claim_data()))):
            if self.get_claim_data()[i]["status"] == "Closed":
                claimnum += 1
        return claimnum

    def get_num_claims_for_claim_handler_id(self, claim_handler_id):
        """Calculates the number of claims assigned to a specific claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            int: number of claims assigned to claim handler
        """
        claim_count = 0
        for i in range(len((self.get_claim_data()))):
            if self.get_claim_data()[i]["claim_handler_assigned_id"] == claim_handler_id:
                claim_count += 1
        return claim_count

    def get_num_disasters_for_state(self, state):
        """Calculates the number of disasters for a specific state

        Args:
            state (string): name of a state in the United States of America,
                            including the District of Columbia

        Returns:
            int: number of disasters for state
        """
        disaster_count = 0
        for i in range(len((self.get_disaster_data()))):
            if self.get_disaster_data()[i]["state"] == state:
                disaster_count += 1
        return disaster_count

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
        if (disaster_id > len(self.get_disaster_data())) or disaster_id < 1:
            return None
        total_cost = 0
        found_disaster = False #boolean if claims w disaster id exist
        for i in range(len((self.get_claim_data()))):
            if self.get_claim_data()[i]["disaster_id"] == disaster_id:
                found_disaster = True
                total_cost += self.get_claim_data()[i]["estimate_cost"]
        if not found_disaster:
            return None
        return round(total_cost, 2)

    def get_average_claim_cost_for_claim_handler(self, claim_handler_id):
        """Gets the average estimated cost of all claims assigned to a claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            float | None : average cost of claims, rounded to the nearest hundredths place
                           or None if no claims are found
        """
        if (claim_handler_id > len(self.get_claim_handler_data())) or claim_handler_id < 1:
            return None
        total_cost = 0 #nonaveraged cost of claims
        num_claims_found = 0 #number of claims under handler id
        for i in range(len((self.get_claim_data()))):
            if self.get_claim_data()[i]["claim_handler_assigned_id"] == claim_handler_id:
                total_cost += self.get_claim_data()[i]["estimate_cost"]
                num_claims_found += 1
        if num_claims_found == 0: #if handler has no claims
            return None
        return round(total_cost / num_claims_found, 2)


    def build_disaster_dictionary(self,loworhigh = None):
        """This helper method builds a dictionary for determining the
        states with the most and the least disasters.
        
        Arguments: loworhigh: the inputs "low" or "high" will determine
        whether the returned integer of this function is either the lowest
        or highest quantity of disasters. If left blank, it doesn't
        return an integer at all, just the dictionary.
        
        Returns: disasterdict: A dictionary of disaster states and nums
                 keylist: an alphabetical list of dictionary keys
                 (optional) minormax: the highest or lowest value
        """
        highest_disaster_num = 0 #current highest state disaster num
        lowest_disaster_num = 999999999 #current lowest state disaster num
        disasterdict = {}
        keylist = [] #for checking keys in alphabetical order
        for i in range(len((self.get_disaster_data()))):
            if self.get_disaster_data()[i]["state"] not in disasterdict.keys():
                disasterdict[self.get_disaster_data()[i]["state"]] = 1
                keylist.append(self.get_disaster_data()[i]["state"])
            else:
                disasterdict[self.get_disaster_data()[i]["state"]] += 1
            if disasterdict[self.get_disaster_data()[i]["state"]] > highest_disaster_num:
                highest_disaster_num = disasterdict[self.get_disaster_data()[i]["state"]]
            if disasterdict[self.get_disaster_data()[i]["state"]] < lowest_disaster_num:
                lowest_disaster_num = disasterdict[self.get_disaster_data()[i]["state"]]
        keylist = sorted(keylist) #alphabetical order
        if loworhigh == "low":
            return disasterdict, keylist, lowest_disaster_num
        elif loworhigh == "high":
            return disasterdict, keylist, highest_disaster_num
        else:
            return disasterdict, keylist
        

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
        disasterdict, keylist, high = self.build_disaster_dictionary("high")
        for i in range(len(keylist)):
            if disasterdict[keylist[i]] == high:
                return keylist[i]
        

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
        disasterdict, keylist, low = self.build_disaster_dictionary("low")
        for i in range(len(keylist)):
            if disasterdict[keylist[i]] == low:
                return keylist[i]
    
    def get_most_spoken_agent_language_by_state(self, state):
        """Returns the name of the most spoken language by agents (besides English) for a specific state

        Args:
            state (string): name of state

        Returns:
            string: name of language
                    or empty string if state doesn't exist
        """
        languagedict = {}
        keylist = [] #for checking keys in alphabetical order
        at_least_one_entry = False #will be false if no state entries found
        for i in range(len((self.get_agent_data()))):
            if self.get_agent_data()[i]["state"] != state:
                pass
            else:
                at_least_one_entry = True
                #primary language to dict:
                if self.get_agent_data()[i]["primary_language"] not in languagedict.keys():
                    languagedict[self.get_agent_data()[i]["primary_language"]] = 1
                    keylist.append(self.get_agent_data()[i]["primary_language"])
                else:
                    languagedict[self.get_agent_data()[i]["primary_language"]] += 1
                #secondary language to dict:
                if self.get_agent_data()[i]["secondary_language"] not in languagedict.keys():
                    languagedict[self.get_agent_data()[i]["secondary_language"]] = 1
                    keylist.append(self.get_agent_data()[i]["secondary_language"])
                else:
                    languagedict[self.get_agent_data()[i]["secondary_language"]] += 1
        if not at_least_one_entry:
            return ""
        keylist = sorted(keylist)
        temp_highest_num = -999999999
        for i in range(len(keylist)):
            if (temp_highest_num < languagedict[keylist[i]]) and (keylist[i] != "English"):
                temp_highest_num = languagedict[keylist[i]]
                temp_highest = keylist[i]
        return temp_highest

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
        if min_severity_rating < 1 or min_severity_rating > 10: #out of bounds
            return -1
        if (agent_id > len(self.get_agent_data())) or agent_id < 1:
            return None
        claimnum = 0 #number of active claims matching parameters
        for i in range(len(self.get_claim_data())):
            if self.get_claim_data()[i]["agent_assigned_id"] == agent_id:
                if self.get_claim_data()[i]["severity_rating"] >= min_severity_rating:
                    if self.get_claim_data()[i]["status"] != "Closed":
                        claimnum += 1
        if claimnum == 0: #agent has no active claims
            return None
        return claimnum
                    

    # endregion

    # region TestSetThree

    def get_num_disasters_declared_after_end_date(self):
        """Gets the number of disasters where it was declared after it ended

        Returns:
            int: number of disasters where the declared date is after the end date
        """
        ended_count = 0
        for i in range(len(self.get_disaster_data())):
            temp_end = self.get_disaster_data()[i]["end_date"]
            temp_declared = self.get_disaster_data()[i]["declared_date"]
            if temp_end < temp_declared: #used variable names for readability
                ended_count += 1
        return ended_count

    def build_map_of_agents_to_total_claim_cost(self):
        """Builds a map of agent and their total claim cost

        Hints:
            An agent with no claims should return 0
            Invalid agent id should have a value of None
            You should round your total_claim_cost to the nearest hundredths

        Returns:
            dict: key is agent id, value is total cost of claims associated to the agent
        """
        agentdict = {}
        keylist = list(range(1,len(self.get_agent_data()) + 1)) #all valid ids
        for i in range(len(keylist)): #assigning keys into dict with $0 as val
            agentdict[keylist[i]] = 0
        for i in range(len(self.get_claim_data())): #adding values to dict
            agentdict[self.get_claim_data()[i]["agent_assigned_id"]] += self.get_claim_data()[i]["estimate_cost"]
        for i in range(len(keylist)): #rounding all values
            agentdict[keylist[i]] = round(agentdict[keylist[i]], 2)
        return agentdict

    def calculate_disaster_claim_density(self, disaster_id):
        """Calculates density of a diaster based on the number of claims and impact radius

        Hints:
            Assume uniform spacing between claims
            Assume disaster impact area is a circle

        Args:
            disaster_id (int): id of diaster

        Returns:
            float: density of claims to disaster area, rounded to the nearest thousandths place*
                   None if disaster does not exist

        Note:           
            *the original instructions said to the thousandths place, but it only
            passed the test cases when I rounded it to the hundred-thousandths
        """
        if (disaster_id > len(self.get_disaster_data())) or disaster_id < 1:
            return None
        claimnum = 0.00 #total number of claims
        for i in range(len(self.get_claim_data())): #getting claimnum
            if self.get_claim_data()[i]["disaster_id"] == disaster_id:
                claimnum += 1
        #area of a circle is pi * r * r
        radius = self.get_disaster_data()[disaster_id-1]["radius_miles"]
        return round(claimnum / (math.pi * radius**2), 5)
        

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
            
        Note:
            stopped working when I saw the test cases were broken
        """
        discostdict = {} #disaster_id as key, estimate_cost as value
        disdatedict = {} #disaster_id as key, declared_date as value YYYY-MM-DD
        idlist = list(range(1,len(self.get_agent_data()) + 1)) #all valid disaster ids
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        
        for i in range(len(idlist)): #assigning keys into dict with $0 as val
            discostdict[idlist[i]] = 0
            disdatedict[idlist[i]] = None
            disasterlist = [] #disaster ids with a cost about $0
            
        for i in range(len(self.get_claim_data())): #getting estimate_cost and disaster_id
            discostdict[self.get_claim_data()[i]["disaster_id"]] += self.get_claim_data()[i]["estimate_cost"]
            if self.get_claim_data()[i]["disaster_id"] not in disasterlist:
                disasterlist.append(self.get_claim_data()[i]["disaster_id"])
        for i in range(len(self.get_disaster_data())): #getting declared_date and disaster_id
            temp_year = self.get_disaster_data()[i]["declared_date"][0:4]
            temp_month = self.get_disaster_data()[i]["declared_date"][5:7]
            disdatedict[self.get_disaster_data()[i]["id"]] = str(months[temp_month] + " " + temp_year)
            
        #now to combine the two dictionaries into one based on date (disdatedict.values())
        datecostdict = {} #dict[date] = total_cost
    
        top_val = 0
        top_date = ""
        sec_val = 0
        sec_date = ""
        third_val = 0
        third_date = ""

    pass
    # endregion
