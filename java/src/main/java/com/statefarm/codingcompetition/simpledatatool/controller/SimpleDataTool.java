package com.statefarm.codingcompetition.simpledatatool.controller;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.text.DecimalFormat;
import java.time.LocalDate;
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
        List<Claim> claims = getClaims();
        int numClosedClaims = 0;
        for (Claim claim : claims) {
            if (claim.getStatus().equals("Closed")) {
                numClosedClaims++;
            }
        }
        return numClosedClaims;
    }

    /**
     * Calculates the number of claims assigned to a specific claim handler
     * 
     * @param id id of claim handler
     * @return number of claims assigned to claim handler
     */
    public int getNumClaimsForClaimHandlerId(int id) {
        List<Claim> claims = getClaims();
        int numClaimsForClaimHandlerId = 0;
        for (Claim claim : claims) {
            if (claim.getClaim_handler_assigned_id() == id) {
                numClaimsForClaimHandlerId++;
            }
        }
        return numClaimsForClaimHandlerId;
    }

    /**
     * Calculates the number of disasters for a specific state
     * 
     * @param stateName name of a state in the United States of America,
     *                  including the District of Columbia
     * @return number of disasters for state
     */
    public int getNumDisastersForState(String stateName) {
        List<Disaster> disasters = getDisasters();
        int numDisastersForState = 0;
        for (Disaster disaster : disasters) {
            if (disaster.getState().equals(stateName)) {
                numDisastersForState++;
            }
        }
        return numDisastersForState;
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
        List<Claim> claims = getClaims();

        // Map of disaster to cost
        Map<Integer, Float> disasterToCost = new HashMap<Integer, Float>();

        for (Claim claim : claims) {
            int disasterId = claim.getDisaster_id();
            float claimCost = claim.getEstimate_cost();

            if (disasterToCost.containsKey(disasterId)) {
                float newCost = disasterToCost.get(disasterId) + claimCost;
                disasterToCost.put(disasterId, newCost);
            } else {
                disasterToCost.put(disasterId, claimCost);
            }
        }

        if (disasterToCost.containsKey(id)) {
            BigDecimal bd = new BigDecimal(Float.toString(disasterToCost.get(id)));
            bd = bd.setScale(2, RoundingMode.HALF_UP);
            return bd.floatValue();
        } else {
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
        List<Claim> claims = getClaims();

        // Map of claim handler to cost
        Map<Integer, Float> claimHandlerToCost = new HashMap<Integer, Float>();

        for (Claim claim : claims) {
            int claimHandlerId = claim.getClaim_handler_assigned_id();
            float claimCost = claim.getEstimate_cost();

            if (claimHandlerToCost.containsKey(claimHandlerId)) {
                float newCost = claimHandlerToCost.get(claimHandlerId) + claimCost;
                claimHandlerToCost.put(claimHandlerId, newCost);
            } else {
                claimHandlerToCost.put(claimHandlerId, claimCost);
            }
        }

        if (claimHandlerToCost.containsKey(id)) {
            int numClaims = getNumClaimsForClaimHandlerId(id);
            float totalCost = claimHandlerToCost.get(id);
            float averageCost = totalCost / numClaims;

            BigDecimal bd = new BigDecimal(Float.toString(averageCost));
            bd = bd.setScale(2, RoundingMode.HALF_UP);
            return bd.floatValue();
        } else {
            return null;
        }
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
        List<String> statesWithMostDisasters = new ArrayList<String>();
        List<Disaster> disasters = getDisasters();

        // Map of state to number of disasters
        Map<String, Integer> stateToNumDisasters = new HashMap<String, Integer>();

        for (Disaster disaster : disasters) {
            String state = disaster.getState();

            if (stateToNumDisasters.containsKey(state)) {
                int newNumDisasters = stateToNumDisasters.get(state) + 1;
                stateToNumDisasters.put(state, newNumDisasters);
            } else {
                stateToNumDisasters.put(state, 1);
            }
        }

        int maxNumDisasters = 0;

        for (String state : stateToNumDisasters.keySet()) {
            int numDisasters = stateToNumDisasters.get(state);

            if (numDisasters > maxNumDisasters) {
                maxNumDisasters = numDisasters;
                statesWithMostDisasters.clear();
                statesWithMostDisasters.add(state);
            } else if (numDisasters == maxNumDisasters) {
                statesWithMostDisasters.add(state);
            }
        }

        statesWithMostDisasters.sort(String::compareToIgnoreCase);
        return statesWithMostDisasters.get(0);
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
        List<String> statesWithLeastDisasters = new ArrayList<String>();
        List<Disaster> disasters = getDisasters();

        // Map of state to number of disasters
        Map<String, Integer> stateToNumDisasters = new HashMap<String, Integer>();

        for (Disaster disaster : disasters) {
            String state = disaster.getState();

            if (stateToNumDisasters.containsKey(state)) {
                int newNumDisasters = stateToNumDisasters.get(state) + 1;
                stateToNumDisasters.put(state, newNumDisasters);
            } else {
                stateToNumDisasters.put(state, 1);
            }
        }

        int maxNumDisasters = Integer.MAX_VALUE;

        for (String state : stateToNumDisasters.keySet()) {
            int numDisasters = stateToNumDisasters.get(state);

            if (numDisasters < maxNumDisasters) {
                maxNumDisasters = numDisasters;
                statesWithLeastDisasters.clear();
                statesWithLeastDisasters.add(state);
            } else if (numDisasters == maxNumDisasters) {
                statesWithLeastDisasters.add(state);
            }
        }

        statesWithLeastDisasters.sort(String::compareToIgnoreCase);
        return statesWithLeastDisasters.get(0);
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
        List<Agent> agents = getAgents();
        Map<String, Integer> languageToNumAgents = new HashMap<String, Integer>();

        for (Agent agent : agents) {
            String state = agent.getState();
            String language1 = agent.getPrimary_language();
            String language2 = agent.getSecondary_language();

            if (state.equalsIgnoreCase(string)) {
                // Add primary language to map
                if (!language1.equalsIgnoreCase("English")) {
                    if (languageToNumAgents.containsKey(language1)) {
                    int newNumAgents = languageToNumAgents.get(language1) + 1;
                    languageToNumAgents.put(language1, newNumAgents);
                    } else {
                        languageToNumAgents.put(language1, 1);
                    }
                }

                // Add secondary language to map
                if (!language2.equalsIgnoreCase("English")) {
                    if (languageToNumAgents.containsKey(language2)) {
                    int newNumAgents = languageToNumAgents.get(language2) + 1;
                    languageToNumAgents.put(language2, newNumAgents);
                    } else {
                        languageToNumAgents.put(language2, 1);
                    }
                }
            }
        } 

        int maxNumAgents = 0;
        String mostSpokenLanguage = "";

        for (String language : languageToNumAgents.keySet()) {
            int numAgents = languageToNumAgents.get(language);

            if (numAgents > maxNumAgents) {
                maxNumAgents = numAgents;
                mostSpokenLanguage = language;
            }
        }

        return mostSpokenLanguage;

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
        if (minSeverityRating < 1 || minSeverityRating > 10) {
            return -1;
        }

        List<Claim> claims = getClaims();

        // Map of agent to number of open claims
        Map<Integer, Integer> agentToNumOpenClaims = new HashMap<Integer, Integer>();

        for (Claim claim : claims) {
            int claimAgentId = claim.getAgent_assigned_id();
            int claimSeverityRating = claim.getSeverity_rating();
            String claimStatus = claim.getStatus();

            if (claimAgentId == agentId && claimSeverityRating >= minSeverityRating && !claimStatus.equals("Closed")) {
                if (agentToNumOpenClaims.containsKey(claimAgentId)) {
                    int newNumOpenClaims = agentToNumOpenClaims.get(claimAgentId) + 1;
                    agentToNumOpenClaims.put(claimAgentId, newNumOpenClaims);
                } else {
                    agentToNumOpenClaims.put(claimAgentId, 1);
                }
            }
        }

        if (agentToNumOpenClaims.containsKey(agentId)) {
            return agentToNumOpenClaims.get(agentId);
        } else {
            return null;
        }
    }

    // endregion

    // region TestSet3

    /**
     * Gets the number of disasters where it was declared after it ended
     * 
     * @return number of disasters where the declared date is after the end date
     */
    public int getNumDisastersDeclaredAfterEndDate() {
        List<Disaster> disasters = getDisasters();
        int numDisastersDeclaredAfterEndDate = 0;

        for (Disaster disaster : disasters) {
            LocalDate declaredDate = disaster.getDeclared_date();
            LocalDate endDate = disaster.getEnd_date();

            if (declaredDate.isAfter(endDate)) {
                numDisastersDeclaredAfterEndDate++;
            }
        }
        return numDisastersDeclaredAfterEndDate;
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
        Map<Integer, Float> agentToTotalClaimCost = new HashMap<Integer, Float>();
        List<Claim> claims = getClaims();
        List<Agent> agents = getAgents();

        // Pre-Populate map with all agents
        for (Agent agent : agents) {
            Integer agentId = agent.getId();
            agentToTotalClaimCost.put(agentId, 0.0f);
        }

        for (Claim claim : claims) {
            int agentId = claim.getAgent_assigned_id();
            Float claimCost = claim.getEstimate_cost();

            if (agentToTotalClaimCost.containsKey(agentId)) {
                // DecimalFormat df = new DecimalFormat("0.00");
                // String claimCostString = df.format(claimCost);
                // claimCost = Float.parseFloat(claimCostString);
                // float newTotalClaimCost = agentToTotalClaimCost.get(agentId) + claimCost;
                Float newTotalClaimCost = Float.sum(agentToTotalClaimCost.get(agentId), claimCost);
                agentToTotalClaimCost.put(agentId, newTotalClaimCost);
            } else {
                agentToTotalClaimCost.put(agentId, claimCost);
            }
        }
        
        return agentToTotalClaimCost;
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
        List<Claim> claims = getClaims();
        List<Disaster> disasters = getDisasters();

        // Map of disaster to claims
        Map<Integer, List<Claim>> disasterToClaims = new HashMap<Integer, List<Claim>>();

        for (Claim claim : claims) {
            int disasterId = claim.getDisaster_id();

            if (disasterToClaims.containsKey(disasterId)) {
                List<Claim> newClaims = disasterToClaims.get(disasterId);
                newClaims.add(claim);
                disasterToClaims.put(disasterId, newClaims);
            } else {
                List<Claim> newClaims = new ArrayList<Claim>();
                newClaims.add(claim);
                disasterToClaims.put(disasterId, newClaims);
            }
        }

        // Map of disaster to impact radius
        Map<Integer, Float> disasterToImpactRadius = new HashMap<Integer, Float>();

        for (Disaster disaster : disasters) {
            int disasterId = disaster.getId();
            float impactRadius = disaster.getRadius_miles();

            disasterToImpactRadius.put(disasterId, impactRadius);
        }

        if (disasterToClaims.containsKey(id)) {
            List<Claim> claimsForDisaster = disasterToClaims.get(id);
            float impactRadius = disasterToImpactRadius.get(id);
            float area = (float) (Math.PI * Math.pow(impactRadius, 2));
            float density = claimsForDisaster.size() / area;

            BigDecimal bd = new BigDecimal(Float.toString(density));
            bd = bd.setScale(5, RoundingMode.HALF_UP);
            return bd.floatValue();
        } else {
            return null;
        }

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
