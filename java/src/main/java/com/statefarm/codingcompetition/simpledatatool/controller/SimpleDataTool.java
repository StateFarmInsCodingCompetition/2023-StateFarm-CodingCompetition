package com.statefarm.codingcompetition.simpledatatool.controller;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.ArrayList;
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
        int num = 0;
        for(var claim : claims) {
            if(claim.getStatus().contains("Closed")) {
                num++;
            }
        }
        return num;
    }

    /**
     * Calculates the number of claims assigned to a specific claim handler
     * 
     * @param id id of claim handler
     * @return number of claims assigned to claim handler
     */
    public int getNumClaimsForClaimHandlerId(int id) {
        int num = 0;
        for(var claim : claims) {
            if(claim.getClaim_handler_assigned_id() == id) {
                num++;
            }
        }
        return num;
    }

    /**
     * Calculates the number of disasters for a specific state
     * 
     * @param stateName name of a state in the United States of America,
     *                  including the District of Columbia
     * @return number of disasters for state
     */
    public int getNumDisastersForState(String stateName) {
        int num = 0;
        for(var disaster : disasters) {
            if(disaster.getState().contains(stateName)) {
                num++;
            }
        }
        return num++;
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
    public Float getTotalClaimCostForDisaster(int id) {
        float totalCost = 0f;
        // get all claims from disaster
        for(var claim : claims) {
            if(claim.getDisaster_id() == id) {
                totalCost += claim.getEstimate_cost();
            }
        }

        if(totalCost > 0f) {
            System.out.println(totalCost);
            totalCost = roundFloat(totalCost);
            return totalCost;
        }
        else {
            return null;
        }
    }

    /**
     * Gets the average estimated cost of all claims assigned to a claim handler
     * 
     * @param id id of claim handler
     * @return average cost of claims, rounded to the nearest hundredths place,
     *         or null if no claims are found
     */
    public Float getAverageClaimCostforClaimHandler(int id) {
        float totalCost = 0f;
        int numOfClaims = 0;
        for(var claim : claims) {
            if(claim.getClaim_handler_assigned_id() == id) {
                totalCost += claim.getEstimate_cost();
                numOfClaims++;
            }
        }
        if(numOfClaims == 0) {
            return null;
        }
        float average = totalCost/numOfClaims;
        average = roundFloat(average);
        return average;
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
        List<String> allDisasters = new ArrayList<String>();
        for(var disaster : disasters) {
            allDisasters.add(disaster.getState());
        }

        Map<String, Integer> frequencyMap = new HashMap<>();
        String mostFrequentString = null;
        int maxFrequency = 0;

        for (String str : allDisasters) {
            frequencyMap.put(str, frequencyMap.getOrDefault(str, 0) + 1);
            int currentFrequency = frequencyMap.get(str);
            
            // Update mostFrequentString if we find a higher frequency
            if (currentFrequency > maxFrequency || (currentFrequency == maxFrequency && (mostFrequentString == null || str.compareTo(mostFrequentString) < 0))) {
                mostFrequentString = str;
                maxFrequency = currentFrequency;
            }
        }

        return mostFrequentString;
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
    public String getStateWithTheLeastDisasters() {
        List<String> allDisasters = new ArrayList<String>();
        for(var disaster : disasters) {
            allDisasters.add(disaster.getState());
        }

        Map<String, Integer> frequencyMap = new HashMap<>();
        String leastFrequentString = null;
        int minFrequency = Integer.MAX_VALUE;

        for (String str : allDisasters) {
            frequencyMap.put(str, frequencyMap.getOrDefault(str, 0) + 1);
        }

        for (String str : frequencyMap.keySet()) {
            int frequency = frequencyMap.get(str);

            if (frequency < minFrequency || (frequency == minFrequency && str.compareTo(leastFrequentString) < 0)) {
                leastFrequentString = str;
                minFrequency = frequency;
            }
        }

        return leastFrequentString;
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
        List<String> languages = new ArrayList<String>();

        for(var agent: agents) {
            if(agent.getState().contains(string)){
                languages.add(agent.getSecondary_language());
            }
        }

        if(languages.size() == 0) {
            return "";
        }
        
        Map<String, Integer> frequencyMap = new HashMap<>();
        String mostFrequentString = null;
        int maxFrequency = 0;

        for (String str : languages) {
            frequencyMap.put(str, frequencyMap.getOrDefault(str, 0) + 1);
            int currentFrequency = frequencyMap.get(str);
            
            // Update mostFrequentString if we find a higher frequency
            if (currentFrequency > maxFrequency || (currentFrequency == maxFrequency && (mostFrequentString == null || str.compareTo(mostFrequentString) < 0))) {
                mostFrequentString = str;
                maxFrequency = currentFrequency;
            }
        }

        return mostFrequentString;
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
     *         null if agent does not exist, or agent has no claims (open or not)
     */
    public Integer getNumOfOpenClaimsForAgentAndSeverity(int agentId, int minSeverityRating) {
        // check severity rating:
        if(minSeverityRating > 10 || minSeverityRating < 1){
            return -1;
        }

        int num = 0;
        // check for agent/agent has claims
        List<Claim> totalClaimsFromAgent = new ArrayList<Claim>();
        for(var claim : claims) {
            if(claim.getAgent_assigned_id() == agentId && !claim.getStatus().contains("Closed")) {
                totalClaimsFromAgent.add(claim);
            }
        }

        if(totalClaimsFromAgent.size() == 0){
            return null;
        }

        for(var claim : totalClaimsFromAgent) {
            if(claim.getSeverity_rating() >= minSeverityRating) {
                num++;
            }
        }
        
        return num;
    }

    // endregion

    // region TestSet3

    /**
     * Gets the number of disasters where it was declared after it ended
     * 
     * @return number of disasters where the declared date is after the end date
     */
    public int getNumDisastersDeclaredAfterEndDate() {
        int num = 0;
        for(var disaster : disasters) {
            if(disaster.getDeclared_date().isAfter(disaster.getEnd_date())){
                num++;
            }
        }
        return num;
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
    public Map<Integer, Float> buildMapOfAgentsToTotalClaimCost() {
        Map<Integer, Float> agentMap = new HashMap<>();

        for(var agent : agents) {
            // check for claims:
            List<Claim> agentClaims = new ArrayList<Claim>();
            Float totalCost = 0f;
            for(var claim : claims) {
                if(claim.getAgent_assigned_id() == agent.getId()) {
                    agentClaims.add(claim);
                    totalCost += claim.getEstimate_cost();
                }
            }
            if(agentClaims.size() == 0) {
                agentMap.put(agent.getId(), 0.00f);
            }
            totalCost = roundFloat(totalCost);
            agentMap.put(agent.getId(), totalCost);

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
    public Float calculateDisasterClaimDensity(int id) {
        Disaster disaster = new Disaster();
        boolean isInit = false;
        for(var dis : disasters) {
            if(dis.getId() == id) {
                disaster = dis;
                isInit = true;
                break;
            }
        }
        if(isInit == false) {
            return null;
        }
        

        int numOfClaims = 0;
        List<Claim> disasterClaims = new ArrayList<Claim>();
        for(var claim : claims) {
            if(claim.getDisaster_id() == id) {
                disasterClaims.add(claim);
                numOfClaims++;
            }
        }

        

        float area = (float) Math.PI * (disaster.getRadius_miles()*disaster.getRadius_miles());
        float density = numOfClaims/area;
        return density;
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
    public String[] getTopThreeMonthsWithHighestNumOfClaimsDesc() {
        return new String[1];
    }

    // endregion



    // caleb's methods:
    public static float roundFloat(float input) {
        float num = BigDecimal.valueOf(input).setScale(2, RoundingMode.HALF_EVEN).floatValue();
        return num;
    }
}
