package com.statefarm.codingcompetition.simpledatatool.controller;

import java.sql.Date;
import java.time.LocalDate;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.statefarm.codingcompetition.simpledatatool.io.JsonHelper;
import com.statefarm.codingcompetition.simpledatatool.model.Agent;
import com.statefarm.codingcompetition.simpledatatool.model.Claim;
import com.statefarm.codingcompetition.simpledatatool.model.ClaimHandler;
import com.statefarm.codingcompetition.simpledatatool.model.Disaster;

public class SimpleDataTool {

    private static final String JSON_FILENAME_AGENTS = "sfcc_2023_agents.json";
    private static final String JSON_FILENAME_CLAIM_HANDLERS = "sfcc_2023_claim_handlers.json";
    private static final String JSON_FILENAME_CLAIMS = "sfcc_2023_claims.json";
    private static final String JSON_FILENAME_DISASTERS = "sfcc_2023_disasters.json";

    private List<Agent> agents;
    private List<ClaimHandler> claimHandlers;
    private List<Claim> claims;
    private List<Disaster> disasters;

    public SimpleDataTool() {
        agents = new JsonHelper<Agent>().loadJson(JSON_FILENAME_AGENTS, Agent.class);
        claimHandlers = new JsonHelper<ClaimHandler>().loadJson(JSON_FILENAME_CLAIM_HANDLERS, ClaimHandler.class);
        claims = new JsonHelper<Claim>().loadJson(JSON_FILENAME_CLAIMS, Claim.class);
        disasters = new JsonHelper<Disaster>().loadJson(JSON_FILENAME_DISASTERS, Disaster.class);
    }

    // region Helper Methods

    public List<Agent> getAgents() {
        return agents;
    }

    public List<ClaimHandler> getClaimHandlers() {
        return claimHandlers;
    }

    public List<Claim> getClaims() {
        return claims;
    }

    public List<Disaster> getDisasters() {
        return disasters;
    }

    // endregion

    // Unit Test Methods

    // region TestSet1

    /**
     * Calculates the number of claims where that status is "Closed"
     * 
     * @return number of closed claims
     */
    public int getNumClosedClaims() {
        int closedClaims = 0;
        
        for(int i = 0; i < claims.size(); i++) {
            if(claims.get(i).getStatus().equals("Closed")) closedClaims++;
        } //this loops through the claims list and increments the closedClaims int if the status of the claim is equal to "Closed".
        
        return closedClaims;
    }

    /**
     * Calculates the number of claims assigned to a specific claim handler
     * 
     * @param id id of claim handler
     * @return number of claims assigned to claim handler
     */
    public int getNumClaimsForClaimHandlerId(int id) {
        int handlerClaims = 0;
        for(int i = 0; i < claims.size(); i++) {
            if(claims.get(i).getClaim_handler_assigned_id() == id) handlerClaims++;
        } //this loops through the claims list, and if the handler id is the same as the id parameter, it increments handlerClaims.
        return handlerClaims;
    }

    /**
     * Calculates the number of disasters for a specific state
     * 
     * @param stateName name of a state in the United States of America,
     *                  including the District of Columbia
     * @return number of disasters for state
     */
    public int getNumDisastersForState(String stateName) {
        int stateDisasters = 0;
        for(int i = 0; i < disasters.size(); i++) {
            if(disasters.get(i).getState().equals(stateName)) stateDisasters++;
        } //this iterates through the disasters list, and if the disaster state is equal to the stateName parameter, it increments stateDisasters.
        return stateDisasters;
    }

    // endregion

    // region TestSet2

    /**
     * Sums the estimated cost of a specific disaster by its claims
     * 
     * @param id id of disaster
     * @return estimate cost of disaster, rounded to the nearest hundredths place
     *         returns null if no claims are found
     */
    public Double getTotalClaimCostForDisaster(int id) { //changed return value from float to double
        double totalCost = 0.00;
        int totalClaims = 0;
        for(int i = 0; i < claims.size(); i++) {
            if(claims.get(i).getDisaster_id() == id) {
                totalCost += claims.get(i).getEstimate_cost();
                totalClaims++;
            }
        }
        /*
        This for loop iterates through the claims list. If the disaster id of the claim is equal to the id parameter, it adds the estimate cost the claim to the total cost.
         */
        if(totalClaims == 0) return null; //if there were no claims, return null.
        return totalCost;
    }

    /**
     * Gets the average estimated cost of all claims assigned to a claim handler
     * 
     * @param id id of claim handler
     * @return average cost of claims, rounded to the nearest hundredths place,
     *         or null if no claims are found
     */
    public Double getAverageClaimCostforClaimHandler(int id) { 
       double averageClaim = 0.00;
        int totalClaims = 0;
        for(int i = 0; i < claims.size(); i++) {
            if(claims.get(i).getClaim_handler_assigned_id() == id) {
                averageClaim += claims.get(i).getEstimate_cost();
                totalClaims++;
            }
        }
        /*
        this iterates through the claims list, and if the handler id of the claim is equal to id parameter, it adds the estimate cost of claim to the total cost.
        also increments totalClaims.
         */
        if(totalClaims == 0) return null;
        return averageClaim / totalClaims; //return the total cost divided by the number of claims
    }

    /**
     * Returns the name of the state with the most disasters based on disaster data
     * 
     * If two states have the same number of disasters, then sort by alphabetical
     * (a-z) and take the first.
     * 
     * Example: Say New Jersey and Delaware both have the highest number of
     * disasters at 12 disasters each. Then, this method would return "Delaware"
     * since "D"comes before "N" in the alphabet.
     * 
     * @return single name of state
     */
    public String getStateWithTheMostDisasters() {
        HashMap<String, Integer> map = new HashMap<>(); //create a hash map with the state being the key and the number of disasters being the value
        int maxDisasters = Integer.MIN_VALUE;
        String state = null;
        for(int i = 0; i < disasters.size(); i++) {
            if(!map.containsKey(disasters.get(i).getState())) map.put(disasters.get(i).getState(), 0); //if state not in map, yet, set state disaster to 0.
            else map.put(disasters.get(i).getState(), map.get(disasters.get(i).getState()) + 1); //increment state disaster
        }
        for(Map.Entry<String, Integer> entry : map.entrySet()) {
            if(entry.getValue() > maxDisasters) { //goes through the map, and if the value of the entry is greater than the max value, change the state and max value.
                state = entry.getKey();
                maxDisasters = entry.getValue();
            }
            else if(entry.getValue() == maxDisasters && entry.getKey().compareTo(state) < 0) { //if value of entry is the same as max value, check which state comes first lexicographically
                state = entry.getKey();
                maxDisasters = entry.getValue();
            }
        }
        return state;
    }

    /**
     * Returns the name of the state with the least disasters based on disaster data
     * 
     * If two states have the same number of disasters, then sort by alphabetical
     * (a-z) and take the first.
     * 
     * Example: Say New Mexico and West Virginia both have the least number of
     * disasters at 1 disaster each. Then, this method would return "New Mexico"
     * since "N" comes before "W" in the alphabet.
     * 
     * @return single name of state
     */
    public String getStateWithTheLeastDisasters() { //implementation of this is similar to getStateWithTheLeastDisasters, except find the minimum instead of the maximum
        HashMap<String, Integer> map = new HashMap<>();
        int minDisasters = Integer.MAX_VALUE;
        String state = null;
        for(int i = 0; i < disasters.size(); i++) {
            if(!map.containsKey(disasters.get(i).getState())) map.put(disasters.get(i).getState(), 0);
            else map.put(disasters.get(i).getState(), map.get(disasters.get(i).getState()) + 1);
        }
        for(Map.Entry<String, Integer> entry : map.entrySet()) {
            if(entry.getValue() < minDisasters) {
                state = entry.getKey();
                minDisasters = entry.getValue();
            }
            else if(entry.getValue() == minDisasters && entry.getKey().compareTo(state) < 0) {
                state = entry.getKey();
                minDisasters = entry.getValue();
            }
        }
        return state;
    }

    /**
     * Returns the name of the most spoken language by agents (besides English) for
     * a specific state
     * 
     * @param string name of state
     * @return name of language
     *         or empty string if state doesn't exist
     */
    public String getMostSpokenAgentLanguageByState(String string) {
        HashMap<String, Integer> languages = new HashMap<>(); //map of languages and how many agents speak each language in a state
        int languageCount = Integer.MIN_VALUE;
        String language = "";
        for(int i = 0; i < agents.size(); i++) {
            if(agents.get(i).getState().equals(string)) {  //if the state of agent is equal to string parameter, we can add primary language and secondary language.
                if(!languages.containsKey(agents.get(i).getPrimary_language())) languages.put(agents.get(i).getPrimary_language(), 1);
                else languages.put(agents.get(i).getPrimary_language(), languages.get(agents.get(i).getPrimary_language()) + 1); //adds for primary language

                if(agents.get(i).getSecondary_language() != null) {
                    if(!languages.containsKey(agents.get(i).getSecondary_language())) languages.put(agents.get(i).getSecondary_language(), 1);
                else languages.put(agents.get(i).getSecondary_language(), languages.get(agents.get(i).getSecondary_language()) + 1); //adds for secondary language
                }
            }
        }
        for(Map.Entry<String, Integer> entry : languages.entrySet()) {
            if(entry.getValue() > languageCount && !entry.getKey().equals("English")) { //checks for every language beside English and sees if number of speakers greater than the current max.
                language = entry.getKey();
                languageCount = entry.getValue();
            }
        }
        return language;
    }

    /**
     * Returns the number of open claims for a specific agent and for a minimum
     * severity level and higher
     * 
     * Note: Severity rating scale for claims is 1 to 10, inclusive.
     * 
     * @param agentId           id of agent
     * @param minSeverityRating minimum claim severity rating
     * @return number of claims that are not closed and have minimum severity rating
     *         or greater
     *         -1 if severity rating out of bounds
     *         None if agent does not exist, or agent has no claims (open or not)
     */
    public int getNumOfOpenClaimsForAgentAndSeverity(int agentId, int minSeverityRating) {
        int claimCount = 0;
        if(minSeverityRating < 1 || minSeverityRating > 10) return -1;
        for(int i = 0; i < claims.size(); i++) { //iterates through claims list, and checks if claim agent id is equal to agentId parameter, claim severity rating is greater than or equal to the minimum rating, and that the status of claim is NOT closed
            if(claims.get(i).getAgent_assigned_id() == agentId && claims.get(i).getSeverity_rating() >= minSeverityRating && !claims.get(i).getStatus().equals("Closed"))  claimCount++;
        }
        return claimCount;
    }

    // endregion

    // region TestSet3

    /**
     * Gets the number of disasters where it was declared after it ended
     * 
     * @return number of disasters where the declared date is after the end date
     */
    public int getNumDisastersDeclaredAfterEndDate() {
        int disasterCount = 0;
        for(int i = 0; i < disasters.size(); i++) {
            if(disasters.get(i).getDeclared_date().isAfter(disasters.get(i).getEnd_date())) disasterCount++; //uses isAfter method for LocalDate to check if declared date is after end date.
        }
        return disasterCount;
    }

    /**
     * Builds a map of agent and their total claim cost
     * 
     * Hints:
     * - An agent with no claims should return 0
     * - Invalid agent id should have a value of null
     * - You should round your total_claim_cost to the nearest hundredths
     * 
     * @return Map where key is agent id, value is total cost of claims associated
     *         to the agent
     */
    public Map<Integer, Double> buildMapOfAgentsToTotalClaimCost() { 
        Map <Integer, Double> agentMap = new HashMap<>();
        for(int i = 0; i < agents.size(); i++) {
            agentMap.put(agents.get(i).getId(), 0.00); //for each agent, set their initial value to zero.
        }
        for(int i = 0; i < claims.size(); i++) {
            agentMap.put(claims.get(i).getAgent_assigned_id(), agentMap.get(claims.get(i).getAgent_assigned_id()) + claims.get(i).getEstimate_cost()); //add cost of each claim to the agent the claim belongs to
        }
        return agentMap;
    }

    /**
     * Calculates density of a diaster based on the number of claims and impact
     * radius
     * 
     * Hints:
     * - Assume uniform spacing between claims
     * - Assume disaster impact area is a circle
     * 
     * @param id id of disaster
     * @return density of claims to disaster area, rounded to the nearest
     *         thousandths place
     *         null if disaster does not exist
     */
    public Double calculateDisasterClaimDensity(int id) {
        int radius = 0;
        int disasterCount = 0;
        for(int i = 0; i < disasters.size(); i++) {
            if(id == disasters.get(i).getId()) radius = disasters.get(i).getRadius_miles(); //find the disaster radius
        }
        for(int i = 0; i < claims.size(); i++) {
            if(claims.get(i).getDisaster_id() == id) disasterCount++; //if claim has same disaster id as id parameter, increment disasterCount
        }
        if(radius == 0) return 0.0;
        return (double)(disasterCount / (Math.pow(radius, 2) * 3.14)); //divide number of claims in disaster by disaster area
    }

    // endregion

    // region TestSet4

    /**
     * Gets the top three months with the highest total claim cost
     * 
     * Hint:
     * - Month should be full name like 01 is January and 12 is December
     * - Year should be full four-digit year
     * - List should be in descending order
     * 
     * @return three strings of month and year, descending order of highest claims
     */
    public String getMonth(int i) { //helper function to get month as a string
        if(i == 1) return "January";
        if(i == 2) return "February";
        if(i == 3) return "March";
        if(i == 4) return "April";
        if(i == 5) return "May";
        if(i == 6) return "June";
        if(i == 7) return "July";
        if(i == 8) return "August";
        if(i == 9) return "September";
        if(i == 10) return "October";
        if(i == 11) return "November";
        if(i == 12) return "December";
        return null;
    }
    public String[] getTopThreeMonthsWithHighestNumOfClaimsDesc() {
        String[] months = new String[3];
        Map<Integer, LocalDate> disasterDates = new HashMap<>(); //map of disaster id and their dates
        for(int i = 0; i < disasters.size(); i++) {
            disasterDates.put(disasters.get(i).getId(), disasters.get(i).getDeclared_date());
        } //for each disaster, set date
        Map<Integer, Integer> claimCostByDates = new HashMap<>(); //map of date and the amount of claims they have
        for(int i = 0; i < claims.size(); i++) {
            int claimDate = disasterDates.get(claims.get(i).getDisaster_id()).getMonthValue()*10000 + disasterDates.get(claims.get(i).getDisaster_id()).getYear();
            if(!claimCostByDates.containsKey(claimDate)) claimCostByDates.put(claimDate, 1);
            else claimCostByDates.put(claimDate, claimCostByDates.get(claimDate) + 1);
        } //for each claim, increment corresponding disaster date
        for(int i = 0; i < 3; i++) { //loops three times to find the three dates with the highest number of claims
            int maxCost = Integer.MIN_VALUE;
            int maxDate = 0;
            for(Map.Entry<Integer, Integer> entry : claimCostByDates.entrySet()) {
                if(entry.getValue() > maxCost) { 
                    maxCost = entry.getValue();
                    maxDate = entry.getKey();
                }
                else if(entry.getValue() == maxCost) {
                    if(entry.getKey() % 10000 > maxDate % 10000) {
                        maxCost = entry.getValue();
                        maxDate = entry.getKey();
                    }
                }
            } //this loop finds the date with the largest number of claims. if two dates have the same number of claims, it returns the date that was most recent
            String year = Integer.toString(maxDate % 10000);
            String month = getMonth(maxDate/10000);
            months[i] = month + " " + year;
            claimCostByDates.remove(maxDate); //remove the entry for the following loop
        }
        return months;
    }

    // endregion
}