package com.statefarm.codingcompetition.simpledatatool.controller;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.SortedMap;
import java.util.TreeMap;

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

        List<Claim> claims = getClaims();

        for (Claim claim : claims) {

            String status = claim.getStatus();
            if (status.equals("Closed"))
                closedClaims++;

        }

        int result = closedClaims == 0 ? -1 : closedClaims;
        return result;
    }

    /**
     * Calculates the number of claims assigned to a specific claim handler
     * 
     * @param id id of claim handler
     * @return number of claims assigned to claim handler
     */
    public int getNumClaimsForClaimHandlerId(int id) {
        int claimsForClaimHandler = 0;

        List<Claim> claims = getClaims();

        for (Claim claim : claims) {

            int claimHandlerID = claim.getClaim_handler_assigned_id();
            if (claimHandlerID == id)
                claimsForClaimHandler++;

        }

        int result = claimsForClaimHandler == 0 ? -1 : claimsForClaimHandler;
        return result;
    }

    /**
     * Calculates the number of disasters for a specific state
     * 
     * @param stateName name of a state in the United States of America,
     *                  including the District of Columbia
     * @return number of disasters for state
     */
    public int getNumDisastersForState(String stateName) {
        int numDisasters = 0;

        List<Disaster> disasters = getDisasters();

        for (Disaster disaster : disasters) {

            if (disaster.getState().equals(stateName))
                numDisasters++;
        }

        int result = numDisasters == 0 ? -1 : numDisasters;
        return result;
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
        float totalClaimCost = 0;

        List<Claim> claims = getClaims();

        for (Claim claim : claims) {

            if (claim.getDisaster_id() != id)
                continue;
            totalClaimCost += claim.getEstimate_cost();

        }

        if (totalClaimCost == 0)
            return null;

        String result = String.format("%.2f", totalClaimCost);
        return Float.parseFloat(result);
    }

    /**
     * Gets the average estimated cost of all claims assigned to a claim handler
     * 
     * @param id id of claim handler
     * @return average cost of claims, rounded to the nearest hundredths place,
     *         or null if no claims are found
     */
    public Float getAverageClaimCostforClaimHandler(int id) {

        float avgClaimCost = 0;
        float totalClaimCost = 0;

        List<Claim> claims = getClaims();

        int noOfClaims = 0;
        for (Claim claim : claims) {

            if (claim.getClaim_handler_assigned_id() != id)
                continue;
            noOfClaims++;

            totalClaimCost += claim.getEstimate_cost();
        }

        if (noOfClaims == 0)
            return null;

        avgClaimCost = totalClaimCost / noOfClaims;

        String result = String.format("%.2f", avgClaimCost);

        return Float.parseFloat(result);
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

        SortedMap<String, Integer> stateMap = new TreeMap<String, Integer>();

        List<Disaster> disasters = getDisasters();

        for (Disaster disaster : disasters) {

            String stateName = disaster.getState();

            if (!stateMap.containsKey(stateName)) { // initialize if new element
                stateMap.put(stateName, 1);
                continue;
            }

            stateMap.put(stateName, stateMap.get(stateName) + 1); // Add one if existing element
        }

        String result = "";
        int topDisasters = 0;
        // loop through map and take greatest # of disasters in alphabetical order
        for (Map.Entry<String, Integer> element : stateMap.entrySet()) {

            if (element.getValue() < topDisasters || element.getValue() == topDisasters)
                continue;
            topDisasters = element.getValue();
            result = element.getKey();
        }

        return result;
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

        SortedMap<String, Integer> stateMap = new TreeMap<String, Integer>();

        List<Disaster> disasters = getDisasters();

        for (Disaster disaster : disasters) {

            String stateName = disaster.getState();

            if (!stateMap.containsKey(stateName)) { // initialize if new element
                stateMap.put(stateName, 1);
                continue;
            }

            stateMap.put(stateName, stateMap.get(stateName) + 1); // Add one if existing element
        }

        String result = "";
        int leastDisasters = 0;
        // loop through map and take the least # of disasters in alphabetical order
        for (Map.Entry<String, Integer> element : stateMap.entrySet()) {

            if (leastDisasters == 0) { // initialize least disasters
                leastDisasters = element.getValue();
                continue;
            }

            if (element.getValue() > leastDisasters || element.getValue() == leastDisasters)
                continue;

            leastDisasters = element.getValue();
            result = element.getKey();
        }

        return result;
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

        HashMap<String, Integer> languageMap = new HashMap<String, Integer>();

        List<Agent> agents = getAgents();

        //loop through and fill HashMap
        for (Agent agent : agents) {

            if(!string.equals(agent.getState())) continue;
            String secondaryLan = agent.getSecondary_language();

            if (!languageMap.containsKey(secondaryLan)) { // initialize if new element
                languageMap.put(secondaryLan, 1);
                continue;
            }

            languageMap.put(secondaryLan, languageMap.get(secondaryLan) + 1); // Add one if existing element
        }

        String result = "";
        int mostSpoken = 0;
        // loop through map and take the most spoken secondary language
        for (Map.Entry<String, Integer> element : languageMap.entrySet()) {



            if (element.getValue() < mostSpoken)
                continue;

            mostSpoken = element.getValue();
            result = element.getKey();
        }


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
     *         null if agent does not exist, or agent has no claims (open or not)
     */
    public Integer getNumOfOpenClaimsForAgentAndSeverity(int agentId, int minSeverityRating) {
        return -2;
    }

    // endregion

    // region TestSet3

    /**
     * Gets the number of disasters where it was declared after it ended
     * 
     * @return number of disasters where the declared date is after the end date
     */
    public int getNumDisastersDeclaredAfterEndDate() {
        return -1;
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
        return null;
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
     * Gets the top three months with the highest number of claims
     * 
     * OPTIONAL! OPTIONAL! OPTIONAL!
     * AS OF 9:21CDT, TEST IS OPTIONAL. SEE GITHUB ISSUE #8 FOR MORE DETAILS
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
}
