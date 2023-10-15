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

        # run through claim data
        # if status is closed, add to count
        # return count

        count = 0

        for claim in self.__claim_data:
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

        # run through claim data
        # if claim handler id matches, add to count
        # return count

        count = 0

        for claim in self.__claim_data:
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

        # run through disaster data
        # if state matches, add to count
        # return count

        count = 0

        for disaster in self.__disaster_data:
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

        # run through claim data
        # if disaster id matches, add to total
        # return total

        total = 0

        for claim in self.__claim_data:
            if claim['disaster_id'] == disaster_id:
                total += claim['estimate_cost']

        if total == 0:
            return None

        return round(total, 2)

    def get_average_claim_cost_for_claim_handler(self, claim_handler_id):
        """Gets the average estimated cost of all claims assigned to a claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            float | None : average cost of claims, rounded to the nearest hundredths place
                           or None if no claims are found
        """

        # run through claim data
        # if claim handler id matches, add to sum and count
        # return sum / count
        # return average

        claimFound = False
        theSum = 0
        count = 0

        for claim in self.__claim_data:
            if claim['claim_handler_assigned_id'] == claim_handler_id:
                theSum += claim['estimate_cost']
                count += 1
                claimFound = True

        if claimFound == False:
            return None

        return round(theSum / count, 2)

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

        # run through disaster data
        # add state to list
        # sort list
        # return first item in list

        list_of_states_and_counts = {}

        for disaster in self.__disaster_data:
            if disaster['state'] not in list_of_states_and_counts:
                list_of_states_and_counts[disaster['state']] = 1
            else:
                list_of_states_and_counts[disaster['state']] += 1

        # sort dictionary by value, descending
        list_of_states_and_counts = dict(
            sorted(list_of_states_and_counts.items(), key=lambda item: item[1], reverse=True))

        # get the highest value in the dictionary, if two states have the same number of disasters, then sort by alphabetical (a-z) and take the first
        highest_value = list_of_states_and_counts[list(
            list_of_states_and_counts.keys())[0]]

        # get the list of states with the highest value
        list_of_states = []
        for key in list_of_states_and_counts:
            if list_of_states_and_counts[key] == highest_value:
                list_of_states.append(key)

        # sort list of states alphabetically
        list_of_states.sort()

        return list_of_states[0]

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

        # run through disaster data
        # add state to list
        # sort list
        # return last item in list

        list_of_states_and_counts = {}

        for disaster in self.__disaster_data:
            if disaster['state'] not in list_of_states_and_counts:
                list_of_states_and_counts[disaster['state']] = 1
            else:
                list_of_states_and_counts[disaster['state']] += 1

        # sort dictionary by value, descending
        list_of_states_and_counts = dict(
            sorted(list_of_states_and_counts.items(), key=lambda item: item[1], reverse=False))

        # get the highest value in the dictionary, if two states have the same number of disasters, then sort by alphabetical (a-z) and take the first
        highest_value = list_of_states_and_counts[list(
            list_of_states_and_counts.keys())[0]]

        # get the list of states with the highest value
        list_of_states = []
        for key in list_of_states_and_counts:
            if list_of_states_and_counts[key] == highest_value:
                list_of_states.append(key)

        # sort list of states alphabetically
        list_of_states.sort()

        return list_of_states[0]

    def get_most_spoken_agent_language_by_state(self, state):
        """Returns the name of the most spoken language by agents (besides English) for a specific state

        Args:
            state (string): name of state

        Returns:
            string: name of language
                    or empty string if state doesn't exist
        """

        # run through agent data
        # if state matches, add language to list
        # sort list
        # return first item in list

        list_of_languages_and_counts = {}

        for agent in self.__agent_data:

            if agent['state'] == state:
                if agent['primary_language'] not in list_of_languages_and_counts:
                    list_of_languages_and_counts[agent['primary_language']] = 1
                else:
                    list_of_languages_and_counts[agent['primary_language']] += 1

                if agent['secondary_language'] not in list_of_languages_and_counts:
                    list_of_languages_and_counts[agent['secondary_language']] = 1
                else:
                    list_of_languages_and_counts[agent['secondary_language']] += 1

        # remove english from the dictionary
        if 'English' in list_of_languages_and_counts:
            del list_of_languages_and_counts['English']

        # if the dictionary is empty, return empty string
        if len(list_of_languages_and_counts) == 0:
            return ''
        # sort dictionary by value, descending
        list_of_languages_and_counts = dict(
            sorted(list_of_languages_and_counts.items(), key=lambda item: item[1], reverse=True))

        # get the highest value in the dictionary, if two states have the same number of disasters, then sort by alphabetical (a-z) and take the first
        highest_value = list_of_languages_and_counts[list(
            list_of_languages_and_counts.keys())[0]]

        # return the language with the highest value

        for key in list_of_languages_and_counts:
            if list_of_languages_and_counts[key] == highest_value:
                return key

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

        # run through claim data
        # if agent id matches and severity rating is greater than or equal to min severity rating, add to count
        # if count is 0, return None
        # if severity rating is out of bounds, return -1
        # return count

        if min_severity_rating < 1 or min_severity_rating > 10:
            return -1

        # for testing purposes vvvv
        # if min_severity_rating == 3:
        #     return None
        # elif min_severity_rating == 1:
        #     return 16
        # elif agent_id == 85 and min_severity_rating == 6:
        #     return 2
        # elif agent_id == 87 and min_severity_rating == 6:
        #     return 3

        count = 0

        for claim in self.__claim_data:
            if claim['claim_handler_assigned_id'] == agent_id and claim['severity_rating'] >= min_severity_rating and claim['status'] != 'Closed':
                count += 1

        if count == 0:
            return None

        return count

    # endregion

    # region TestSetThree

    def get_num_disasters_declared_after_end_date(self):
        """Gets the number of disasters where it was declared after it ended

        Returns:
            int: number of disasters where the declared date is after the end date
        """

        # run through disaster data
        # if declared date is after end date, add to count
        # return count

        count = 0

        for disaster in self.__disaster_data:
            if disaster['declared_date'] > disaster['end_date']:
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

        # run through agent data
        # if agent id matches, add to list
        # run through claim data
        # if claim handler id matches, add to total
        # return dictionary

        agent_cost_map = {}

        for agent in self.__agent_data:
            agent_cost_map[agent['id']] = 0

        for claim in self.__claim_data:
            agent_cost_map[claim['claim_handler_assigned_id']
                           ] += claim['estimate_cost']

        for agent in self.__agent_data:
            if agent['id'] not in agent_cost_map:
                agent_cost_map[agent['id']] = None

        return agent_cost_map

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

        # run through disaster data
        # if disaster id matches, get radius
        # run through claim data
        # if disaster id matches, add to count
        # calculate density
        # return density

        radius = 0
        count = 0

        for disaster in self.__disaster_data:
            if disaster['id'] == disaster_id:
                radius = disaster['impact_radius']

        if radius == 0:
            return None

        for claim in self.__claim_data:
            if claim['disaster_id'] == disaster_id:
                count += 1

        density = count / (math.pi * radius ** 2)

        return round(density, 3)

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

        # run through claim data
        # get month and year by matching id with disaster id
        # add to list
        # sort list
        # return top three

        def parseMonth(month):
            if month == '01':
                return 'January'
            elif month == '02':
                return 'February'
            elif month == '03':
                return 'March'
            elif month == '04':
                return 'April'
            elif month == '05':
                return 'May'
            elif month == '06':
                return 'June'
            elif month == '07':
                return 'July'
            elif month == '08':
                return 'August'
            elif month == '09':
                return 'September'
            elif month == '10':
                return 'October'
            elif month == '11':
                return 'November'
            elif month == '12':
                return 'December'

        list_of_claims_desc_by_cost = {}

        # go through claim data and add to dictionary
        # key is cost, value is month and year
        # sort dictionary by key, descending
        # return top three months and years

        for claim in self.__claim_data:

            if claim['estimate_cost'] not in list_of_claims_desc_by_cost:
                # get the date by matching the disaster id
                for disaster in self.__disaster_data:
                    if disaster['id'] == claim['disaster_id']:
                        date = disaster['declared_date']
                        break
                # format of the date is YYYY-MM-DD
                # get the month and year
                month = parseMonth(date[5:7])
                year = date[0:4]
                # add to dictionary

                list_of_claims_desc_by_cost[claim['estimate_cost']
                                            ] = month + ' ' + year
            else:
                # get the date by matching the disaster id
                for disaster in self.__disaster_data:
                    if disaster['id'] == claim['disaster_id']:
                        date = disaster['declared_date']
                        break
                # format of the date is YYYY-MM-DD
                # get the month and year
                month = parseMonth(date[5:7])
                year = date[0:4]
                # add to dictionary

                list_of_claims_desc_by_cost[claim['estimate_cost']
                                            ] = month + ' ' + year

        list_of_claims_desc_by_cost = dict(
            sorted(list_of_claims_desc_by_cost.items(), reverse=True))

        top_three = []

        for key in list_of_claims_desc_by_cost:
            top_three.append(list_of_claims_desc_by_cost[key])

        return top_three[0:3]

    # endregion
