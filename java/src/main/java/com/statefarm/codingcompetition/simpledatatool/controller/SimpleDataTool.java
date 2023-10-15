package com.statefarm.codingcompetition.simpledatatool.controller;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.*;

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
        int numClosedClaims = 0;
        for(Claim claim : claims)
            if("Closed".equals(claim.getStatus()))
                numClosedClaims++;
        return numClosedClaims;
    }

    /**
     * Calculates the number of claims assigned to a specific claim handler
     *
     * @param id id of claim handler
     * @return number of claims assigned to claim handler
     */
    public int getNumClaimsForClaimHandlerId(int id) {
        int numOfClaims=0;
        for(Claim claim : claims)
            if(id == claim.getClaim_handler_assigned_id())
                numOfClaims++;
        return numOfClaims;
    }

    /**
     * Calculates the number of disasters for a specific state
     *
     * @param stateName name of a state in the United States of America,
     *                  including the District of Columbia
     * @return number of disasters for state
     */
    public int getNumDisastersForState(String stateName) {
        int disastersOfState = 0;
        for(Disaster disaster : disasters)
            if(stateName.equals(disaster.getState()))
                disastersOfState++;
        return disastersOfState;
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
        double sumOfCost = 0;
        for(Claim claim : claims) {
            if (id == claim.getDisaster_id())
                sumOfCost += claim.getEstimate_cost();
        }

        if(sumOfCost == 0)
            return null;
        return sumOfCost;
    }
    /**
     * Gets the average estimated cost of all claims assigned to a claim handler
     *
     * @param id id of claim handler
     * @return average cost of claims, rounded to the nearest hundredths place,
     *         or null if no claims are found
     */
    public Float getAverageClaimCostforClaimHandler(int id) {
        float sumOfAllClaims = 0;
        float avg = 0;
        int allClaims = getNumClaimsForClaimHandlerId(id);
        if(allClaims == 0)
            return null;
        for(Claim claim : claims)
            if(id == claim.getClaim_handler_assigned_id())
                sumOfAllClaims+=claim.getEstimate_cost();
        avg = sumOfAllClaims/allClaims;
        avg = Math.round(avg*100) / 100.0f;
        return avg;
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
        Map<String, Integer> stateDisasterCount = new HashMap<>();
        for(Disaster disaster : disasters) {
            String state = disaster.getState();
            stateDisasterCount.put(state,stateDisasterCount.getOrDefault(state,0)+1);
        }
        int max = 0;
        List<String> equalStates = new ArrayList<>();
        for(String state :stateDisasterCount.keySet()) {
            int disasterCount = stateDisasterCount.get(state);
            if(disasterCount > max) {
                max = disasterCount;
                equalStates.clear();
                equalStates.add(state);
            } else if (disasterCount == max)
                equalStates.add(state);
        }
        Collections.sort(equalStates);
        if(!equalStates.isEmpty())
            return equalStates.get(0);
        else return null;
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
        Map<String, Integer> stateDisasterCount = new HashMap<>();
        for(Disaster disaster : disasters) {
            String state = disaster.getState();
            stateDisasterCount.put(state,stateDisasterCount.getOrDefault(state,0)+1);
        }
        int min = Integer.MAX_VALUE;
        List<String> equalStates = new ArrayList<>();
        for(String state :stateDisasterCount.keySet()) {
            int disasterCount = stateDisasterCount.get(state);
            if(disasterCount < min) {
                min = disasterCount;
                equalStates.clear();
                equalStates.add(state);
            } else if (disasterCount == min)
                equalStates.add(state);
        }
        Collections.sort(equalStates);
        if(!equalStates.isEmpty())
            return equalStates.get(0);
        else return null;
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
        Map<String, Integer> biLingual = new HashMap<>();
        for(Agent agent : agents) {
            if(string.equals(agent.getState()))
                biLingual.put(agent.getSecondary_language(), biLingual.getOrDefault(agent.getSecondary_language(), 0)+1);
        }
        int max = 0;
        String popLanguage = "";
        for(String language :biLingual.keySet()) {
            int popular = biLingual.get(language);
            if (popular > max)
                max = popular;
            popLanguage = language;
        }
        return popLanguage;
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
        int openClaims = 0;
        if(minSeverityRating < 1 || minSeverityRating > 10)
            return -1;
        for(Claim claim : claims) {
            if (agentId == claim.getAgent_assigned_id() && minSeverityRating <= claim.getSeverity_rating()) {
                if (!claim.getStatus().equals("Closed"))
                    openClaims++;
            }
        }
        if(openClaims > 0)
            return openClaims;
        else
            return null;
    }

    // endregion

    // region TestSet3

    /**
     * Gets the number of disasters where it was declared after it ended
     * 
     * @return number of disasters where the declared date is after the end date
     */
    public int getNumDisastersDeclaredAfterEndDate() {
        int count = 0;
        for(Disaster disaster : disasters) {
            LocalDate declared = disaster.getDeclared_date();
            LocalDate end = disaster.getEnd_date();
            if(declared.isAfter(end))
                count++;
        }
        return count;
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
        Map<Integer,Double> agentsToCost = new HashMap<>();
        for(Claim claim : claims) {
            if (!agentsToCost.containsKey(claim.getAgent_assigned_id()))
                agentsToCost.put(claim.getAgent_assigned_id(), claim.getEstimate_cost());
            else if (agentsToCost.containsKey(claim.getAgent_assigned_id()))
                agentsToCost.replace(claim.getAgent_assigned_id(), agentsToCost.getOrDefault(claim.getAgent_assigned_id(), Double.valueOf(0)) + claim.getEstimate_cost());
        }
        return agentsToCost;
    }

    /**
     * Calculates density of a disaster based on the number of claims and impact
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
