package com.statefarm.codingcompetition.simpledatatool.controller;

import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.HashMap;
import java.util.HashSet;
import java.text.SimpleDateFormat;

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
        // System.out.println(agents);
        int counter = 0;
        for (Claim c: this.getClaims()){
            if (c.getStatus().equals("Closed")){
                counter++;
            }
        }
        return counter;
    }

    /**
     * Calculates the number of claims assigned to a specific claim handler
     * 
     * @param id id of claim handler
     * @return number of claims assigned to claim handler
     */
    public int getNumClaimsForClaimHandlerId(int id) {
        int counter = 0;
        for (Claim claim : getClaims()) {
            if (claim.getClaim_handler_assigned_id() == id) {
                counter++;
            }
        }
        return counter;
    }
        

    /**
     * Calculates the number of disasters for a specific state
     * 
     * @param stateName name of a state in the United States of America,
     *                  including the District of Columbia
     * @return number of disasters for state
     */
    public int getNumDisastersForState(String stateName) {
        int counter = 0;
        for (Disaster d: this.getDisasters()){
            if (d.getState().equals(stateName)){
                counter++;
            }
        }
        return counter;
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
    public Double getTotalClaimCostForDisaster(int id) {
        double sum = 0f;

        for (Claim c: this.getClaims()){
            if (c.getDisaster_id() == id){
                sum += c.getEstimate_cost();
            }
        }
        if (sum == 0){
            return null;
        }
        return sum;
    }

    /**
     * Gets the average estimated cost of all claims assigned to a claim handler
     * 
     * @param id id of claim handler
     * @return average cost of claims, rounded to the nearest hundredths place,
     *         or null if no claims are found
     */
    public Float getAverageClaimCostforClaimHandler(int id) {
        Float sum = 0f;
        int count = 0;

        for (Claim c: claims){
            if (c.getClaim_handler_assigned_id() == id){
                sum += c.getEstimate_cost();
                count++;
            }
        }
        if (sum == 0f){
            return null;
        }
        return sum/count;
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
        HashMap<String, Integer> map = new HashMap<>();
        for (Disaster d: this.getDisasters()){
            if (map.containsKey(d.getState())){
                int currentCount = map.get(d.getState());
                currentCount++;
                map.put(d.getState(), currentCount);
            }
            else{
                map.put(d.getState(), 1);
            }
        }

        String maxKey = null;
        int maxValue = Integer.MIN_VALUE;

        for (Map.Entry<String, Integer> entry : map.entrySet()) {
            if (entry.getValue() > maxValue) {
                maxValue = entry.getValue();
                maxKey = entry.getKey();
            }
        }

        return maxKey;
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
        HashMap<String, Integer> map = new HashMap<>();
        for (Disaster d: this.getDisasters()){
            if (map.containsKey(d.getState())){
                int currentCount = map.get(d.getState());
                currentCount++;
                map.put(d.getState(), currentCount);
            }
            else{
                map.put(d.getState(), 1);
            }
        }

        String minKey = null;
        int minValue = Integer.MAX_VALUE;

        for (Map.Entry<String, Integer> entry : map.entrySet()) {
            int value = entry.getValue();
            String key = entry.getKey();

            if (value < minValue || (value == minValue && key.compareTo(minKey) < 0)) {
                minValue = value;
                minKey = key;
            }
        }

        return minKey;
    }

    /**
     * Returns the name of the most spoken language by agents (besides English) for
     * a specific state
     * 
     * @param string name of state
     * @return name of language
     *         or empty string if state doesn't exist
     */
    public String getMostSpokenAgentLanguageByState(String state) {
        String result = "";
        int maxFreq = 0;

        Map<String, Integer> freq = new HashMap<>();
        for (Agent a: getAgents()){
            String agentState = a.getState();
            String agentLang1 = a.getPrimary_language();
            String agentLang2 = a.getSecondary_language();

            if (agentState.equals(state)){
                if (freq.containsKey(agentLang1) && !agentLang1.equals("English")){
                    freq.put(agentLang1, freq.get(agentLang1) + 1);

                    if (freq.get(agentLang1) > maxFreq) {
                        maxFreq = freq.get(agentLang1);
                        result = agentLang1;
                    }
                } else if(agentLang1 != null && !agentLang1.equals("English")) {
                    freq.put(agentLang1, 1);

                    if (freq.get(agentLang1) > maxFreq) {
                        maxFreq = freq.get(agentLang1);
                        result = agentLang1;
                    }
                }

                if (freq.containsKey(agentLang2) && !agentLang2.equals("English")){
                    freq.put(agentLang2, freq.get(agentLang2) + 1);

                    if (freq.get(agentLang2) > maxFreq) {
                        maxFreq = freq.get(agentLang2);
                        result = agentLang2;
                    }
                } else if(agentLang2 != null && !agentLang2.equals("English")) {
                    freq.put(agentLang2, 1);

                    if (freq.get(agentLang2) > maxFreq) {
                        maxFreq = freq.get(agentLang2);
                        result = agentLang2;
                    }
                }
            }
        }

        // get the max
        return result;
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
    public Integer getNumOfOpenClaimsForAgentAndSeverity(int agentId, int minSeverityRating) {
        int counter = 0;
        for (Claim c: getClaims()){
            if (c.getAgent_assigned_id() == agentId){
                if (c.getSeverity_rating() >= minSeverityRating && !c.getStatus().equals("Closed")){
                    counter++;
                }
            }
        }
        if (minSeverityRating < 1 || minSeverityRating > 10){
            return -1;
        }
        if (counter == 0){
            return null;
        }
        return counter;
    }

    // endregion

    // region TestSet3

    /**
     * Gets the number of disasters where it was declared after it ended
     * 
     * @return number of disasters where the declared date is after the end date
     */
    public int getNumDisastersDeclaredAfterEndDate() {
        int counter = 0;
        for (Disaster d: getDisasters()){
            if (d.getDeclared_date().compareTo(d.getEnd_date()) > 0) {
                counter += 1;
            }
           
        }
        return counter;
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
        HashMap<Integer, Double> mapping = new HashMap<>();
        HashSet<Integer> agentIdSet = new HashSet<>();

        for(Agent agent : getAgents()){
            Integer agentId = agent.getId();
            if (!mapping.containsKey(agentId)) {
                mapping.put(agentId, 0.0);
            }
        }

        for (Claim claim : getClaims()) {
            Integer agentId = claim.getAgent_assigned_id();
            double cost = (double) claim.getEstimate_cost();

            if (mapping.containsKey(agentId)) {
                mapping.put(agentId, mapping.get(agentId) + cost);
            } else if (agentIdSet.contains(agentId)) {
                mapping.put(agentId, cost);
            } else {
                mapping.put(agentId, null);
            }
        }

        for (Integer agentId : mapping.keySet()) {
            mapping.put(agentId, Math.round(mapping.get(agentId) * 100.0) / 100.0);
        }

        return mapping;
        // HashMap<String, Double> map = new HashMap<>();
        // return map;

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
    public float calculateDisasterClaimDensity(int id) {
        return -0.01f;
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
        // Map<String, Float> monthToTotalClaimCost = new HashMap<>();
        // SimpleDateFormat sdf = new SimpleDateFormat("MMMM yyyy");
    
        // for (Claim claim : claims) {
        //     String monthYear = sdf.format(claim.getDisaster_id());
        //     monthToTotalClaimCost.put(monthYear,
        //         monthToTotalClaimCost.getOrDefault(monthYear, 0f) + claim.getEstimatedLoss());
        // }
    
        // return monthToTotalClaimCost.entrySet().stream()
        //     .sorted((e1, e2) -> Float.compare(e2.getValue(), e1.getValue()))
        //     .limit(3)
        //     .map(Map.Entry::getKey)
        //     .toArray(String[]::new);
        return new String[2];
    }
    

    // endregion
}