package com.statefarm.codingcompetition.simpledatatool.controller;

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

    /**
     * Calculates the number of claims where that status is "Closed"
     * 
     * @return number of closed claims
     */
    public int getNumClosedClaims() {
        // load the list of claims
        List<Claim> claims = this.getClaims();
        // number of closed claims
        int count = 0;
        for (Claim c: claims) {
            if (c.getStatus().equals("Closed")) {
                count++;
            }
        }
        return count;
    }

    /**
     * Calculates the number of claims assigned to a specific claim handler
     * 
     * @param id id of claim handler
     * @return number of claims assigned to claim handler
     */
    public int getNumClaimsForClaimHandlerId(int id) {
        // load the list of claims
        List<Claim> claims = this.getClaims();
        // number of claims assigned to handler
        int count = 0;
        for (Claim c: claims) {
            if (c.getClaim_handler_assigned_id() == id) {
                count++;
            }
        }
        return count;
    }

    /**
     * Calculates the number of disasters for a specific state
     * 
     * @param stateName name of a state in the United States of America,
     *                  including the District of Columbia
     * @return number of disasters for state
     */
    public int getNumDisastersForState(String stateName) {
        // load the list of disasters
        List<Disaster> disasters = this.getDisasters();
        // number of claims assigned to handler
        int count = 0;
        for (Disaster d: disasters) {
            if (d.getState().equals(stateName)) {
                count++;
            }
        }
        return count;
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
        // total cost of disaster
        Float cost = 0.0f;
        int count = 0;
        List<Claim> claims = this.getClaims();
        for (Claim c: claims) {
            if (c.getDisaster_id() == id) {
                count++;
                cost += c.getEstimate_cost();
            }
        }
        cost = Math.round(cost * 100f) / 100f;
        return (count == 0) ? null : cost;
    }

    /**
     * Gets the average estimated cost of all claims assigned to a claim handler
     * 
     * @param id id of claim handler
     * @return average cost of claims, rounded to the nearest hundredths place,
     *         or null if no claims are found
     */
    public Float getAverageClaimCostforClaimHandler(int id) {
        // total cost of all claims assigned to a claim handler
        Float cost = 0.0f;
        // total number of claims
        int count = 0;
        List<Claim> claims = this.getClaims();
        for (Claim c: claims) {
            if (c.getClaim_handler_assigned_id() == id) {
                count++;
                cost += c.getEstimate_cost();
            }
        }
        return (count == 0) ? null : (cost / count);
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
        // A map mapping between state's name and number of disasters
        HashMap<String, Integer> stateDisasterCounts = new HashMap<>();
        // list of disasters
        List<Disaster> disasters = this.getDisasters();
        // name and number of the state with most disasters
        String mostDisasterState = null;
        int maxDisasters = Integer.MIN_VALUE;
        for (Disaster d: disasters) {
            String stateName = d.getState();
            stateDisasterCounts.put(stateName, stateDisasterCounts.getOrDefault(stateName, 0) + 1);
            if (stateDisasterCounts.get(stateName) > maxDisasters || (stateDisasterCounts.get(stateName) == maxDisasters &&stateName.compareTo(mostDisasterState) < 0)) {
                maxDisasters = stateDisasterCounts.get(stateName);
                mostDisasterState = stateName;
            }
        }
        return mostDisasterState;
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
        // A map mapping between state's name and number of disasters
        HashMap<String, Integer> stateDisasterCounts = new HashMap<>();
        // list of disasters
        List<Disaster> disasters = this.getDisasters();
        // name and number of the state with most disasters
        String leastDisasterState = null;
        int minDisasters = Integer.MAX_VALUE;
        for (Disaster d: disasters) {
            String stateName = d.getState();
            stateDisasterCounts.put(stateName, stateDisasterCounts.getOrDefault(stateName, 0) + 1);
        }

        for (Map.Entry<String, Integer> entry: stateDisasterCounts.entrySet()) {
            String stateName = entry.getKey();
            int disasterNum = entry.getValue();
            if (disasterNum < minDisasters || (disasterNum == minDisasters && stateName.compareTo(leastDisasterState) < 0)) {
                leastDisasterState = stateName;
                minDisasters = disasterNum;
            }
        }
        return leastDisasterState;
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
        // list of agents
        List<Agent> agents = this.getAgents();
        Map<String, Integer> languageCount = new HashMap<>();
        for (Agent a : agents) {
            if (a.getState().equals(string)) {
                String primaryLan = a.getPrimary_language();
                String secondaryLan = a.getSecondary_language();
                if (primaryLan.equals("English")) {
                    languageCount.put(secondaryLan, languageCount.getOrDefault(secondaryLan, 0) + 1);
                } else {
                    languageCount.put(primaryLan, languageCount.getOrDefault(primaryLan, 0) + 1);
                }
            }
        }
        int mostSpokenNum = Integer.MIN_VALUE;
        String mostSpokenName = "";
        for (Map.Entry<String, Integer> entry: languageCount.entrySet()) {
            String lanName = entry.getKey();
            int lanNum = entry.getValue();
            if (lanNum > mostSpokenNum || (mostSpokenNum == lanNum && lanName.compareTo(mostSpokenName) < 0)) {
                mostSpokenName = lanName;
                mostSpokenNum = lanNum;
            }
        }
        return mostSpokenName;
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
        List<Claim> claims = this.getClaims();
        if (minSeverityRating > 10 || minSeverityRating < 1) {
            return -1;
        }
        Integer count = 0;
        for (Claim c : claims) {
            String status = c.getStatus();
            int severityLvl = c.getSeverity_rating();
            int agent = c.getAgent_assigned_id();
            if (agent == agentId && severityLvl >= minSeverityRating && status.equals("Open")) {
                count++;
            }
        }
        return count == 0 ? null : count;
    }

    // endregion

    // region TestSet3

    /**
     * Gets the number of disasters where it was declared after it ended
     * 
     * @return number of disasters where the declared date is after the end date
     */
    public int getNumDisastersDeclaredAfterEndDate() {
         // Stream through the list of disasters
        return (int) this.getDisasters().stream()
            // Filter for disasters where the declared date is after the end date
                    .filter(disaster -> disaster.getDeclared_date().after(disaster.getEnd_date()))
                    .count();
            // Count disasters
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
        // Stream through the list of claims and group by agent ID and the cost for each agent's claims
        Map<Integer, Float> agentToClaimCost = this.getClaims().stream()
        .collect(Collectors.groupingBy(Claim::getAgentId,
                Collectors.summingFloat(Claim::getEstimatedCost)));
            // For each agent cost of 0 if no claims
        this.getAgents().forEach(agent -> agentToClaimCost.putIfAbsent(agent.getId(), 0f));

        return agentToClaimCost;

        // return null;
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
        return new String[1];
    }

    // endregion
}