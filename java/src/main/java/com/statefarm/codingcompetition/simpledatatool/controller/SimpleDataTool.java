package com.statefarm.codingcompetition.simpledatatool.controller;

import java.time.LocalDate;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.stream.Collectors;

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

        for (Claim claim : claims) {
            if ("Closed".equals(claim.getStatus())) {
                closedClaims++;
            }
        }

    return closedClaims;
    }

    /**
     * Calculates the number of claims assigned to a specific claim handler
     * 
     * @param id id of claim handler
     * @return number of claims assigned to claim handler
     */
    public int getNumClaimsForClaimHandlerId(int id) {
        int claimsForHandler = 0;

        for (Claim claim : claims) {
            if (claim.getClaim_handler_assigned_id() == id) {
                claimsForHandler++;
            }
        }

        return claimsForHandler;
    }

    /**
     * Calculates the number of disasters for a specific state
     * 
     * @param stateName name of a state in the United States of America,
     *                  including the District of Columbia
     * @return number of disasters for state
     */
    public int getNumDisastersForState(String stateName) {
        int disastersForState = 0;

        for (Disaster disaster : disasters) {
            if (stateName.equals(disaster.getState())) {
                disastersForState++;
            }
        }

        return disastersForState;
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
        BigDecimal totalCost = new BigDecimal(0);

    for (Claim claim : claims) {
        if (claim.getDisaster_id() == id) {
            totalCost = totalCost.add(new BigDecimal(claim.getEstimate_cost()));
        }
    }

    if (totalCost.compareTo(BigDecimal.ZERO) == 0) {
        return null; // No claims found for the specified disaster
    }

    // Round the total cost to the nearest hundredths place
    totalCost = totalCost.setScale(2, RoundingMode.HALF_UP);

    return totalCost.floatValue();
    }


    /**
     * Gets the average estimated cost of all claims assigned to a claim handler
     * 
     * @param id id of claim handler
     * @return average cost of claims, rounded to the nearest hundredths place,
     *         or null if no claims are found
     */
    public Float getAverageClaimCostforClaimHandler(int id) {
        // Create a list to store estimated costs of claims assigned to the claim handler
    List<BigDecimal> claimCosts = new ArrayList<>();

    // Iterate through the claims
    for (Claim claim : claims) {
        if (claim.getAgent_assigned_id() == id) {
            float claimCostFloat = claim.getEstimate_cost();
            BigDecimal claimCost = BigDecimal.valueOf(claimCostFloat);
            claimCosts.add(claimCost);
        }
    }

    // Check if there are no claims found for the claim handler
    if (claimCosts.isEmpty()) {
        return null;
    }

    // Calculate the average cost of claims
    BigDecimal totalCost = BigDecimal.ZERO;
    for (BigDecimal claimCost : claimCosts) {
        totalCost = totalCost.add(claimCost);
    }

    BigDecimal averageCost = totalCost.divide(BigDecimal.valueOf(claimCosts.size()), 2, RoundingMode.HALF_UP);

    return averageCost.floatValue();
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

        for (Disaster disaster : disasters) {
            stateDisasterCount.put(disaster.getState(), stateDisasterCount.getOrDefault(disaster.getState(), 0) + 1);
        }
    
        String mostDisastersState = "";
        int mostDisasters = 0;
    
        for (Map.Entry<String, Integer> entry : stateDisasterCount.entrySet()) {
            if (entry.getValue() > mostDisasters || (entry.getValue() == mostDisasters && entry.getKey().compareTo(mostDisastersState) < 0)) {
                mostDisasters = entry.getValue();
                mostDisastersState = entry.getKey();
            }
        }
    
        return mostDisastersState;
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

        for (Disaster disaster : disasters) {
            stateDisasterCount.put(disaster.getState(), stateDisasterCount.getOrDefault(disaster.getState(), 0) + 1);
        }
    
        String leastDisastersState = "";
        int leastDisasters = Integer.MAX_VALUE;
    
        for (Map.Entry<String, Integer> entry : stateDisasterCount.entrySet()) {
            if (entry.getValue() < leastDisasters || (entry.getValue() == leastDisasters && entry.getKey().compareTo(leastDisastersState) < 0)) {
                leastDisasters = entry.getValue();
                leastDisastersState = entry.getKey();
            }
        }
    
        return leastDisastersState;
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
        Map<String, Integer> languageCounts = new HashMap<>();

        for (Agent agent : agents) {
            if (string.equals(agent.getState())) {
                // Check if the agent's primary language is not English and update language counts.
                if (!"English".equals(agent.getPrimary_language())) {
                    languageCounts.merge(agent.getPrimary_language(), 1, Integer::sum);
                }
                // Check if the agent's secondary language is not English and update language counts.
                if (agent.getSecondary_language() != null && !"English".equals(agent.getSecondary_language())) {
                    languageCounts.merge(agent.getSecondary_language(), 1, Integer::sum);
                }
            }
        }

        if (languageCounts.isEmpty()) {
            return ""; // No agents found for the specified state or no agents with non-English languages.
        }

        // Find the most spoken language by counting.
        String mostSpokenLanguage = Collections.max(languageCounts.entrySet(), Map.Entry.comparingByValue()).getKey();

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
     *         None if agent does not exist, or agent has no claims (open or not)
     */
    public Integer getNumOfOpenClaimsForAgentAndSeverity(int agentId, int minSeverityRating) {
        if (minSeverityRating < 1 || minSeverityRating > 10) {
            return -1; // Severity rating out of bounds
        }
    
        int openClaims = 0;
    
        for (Claim claim : claims) {
            if (claim.getAgent_assigned_id() == agentId &&
                !claim.getStatus().equals("Closed") &&
                claim.getSeverity_rating() >= minSeverityRating) {
                openClaims++;
            }
        }
    
        if (openClaims == 0) {
            return null; // Agent does not exist or has no open claims
        }
    
        return openClaims;
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

    // Iterate through the disasters
    for (Disaster disaster : disasters) {
        LocalDate declaredDate = disaster.getDeclared_date();
        LocalDate endDate = disaster.getEnd_date();

        // Check if declared date is after the end date
        if (declaredDate.isAfter(endDate)) {
            count++;
        }
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
    public Map<Integer, Float> buildMapOfAgentsToTotalClaimCost() {
        // Create a map to store the total claim cost for each agent
    Map<Integer, Float> agentToTotalClaimCostMap = new HashMap<>();

    // Initialize the map with all agent IDs and 0.0 total claim cost
    
    for (Agent agent : agents) {
        agentToTotalClaimCostMap.put(agent.getId(), 0.0f);
    }

    // Iterate through the claims and calculate the total claim cost for each agent
    List<Claim> claims = getClaims(); // Assuming you have a list of Claim objects
    for (Claim claim : claims) {
        int agentId = claim.getAgent_assigned_id();
        float claimCost = claim.getEstimate_cost();
        
        // If the agent ID is invalid, skip this claim
        if (!agentToTotalClaimCostMap.containsKey(agentId)) {
            continue;
        }
        
        // Update the total claim cost for the agent
        float currentTotal = agentToTotalClaimCostMap.get(agentId);
        float newTotal = currentTotal + claimCost;
        agentToTotalClaimCostMap.put(agentId, newTotal);
    }

    // Round the total claim cost to the nearest hundredths
    for (Map.Entry<Integer, Float> entry : agentToTotalClaimCostMap.entrySet()) {
        float totalClaimCost = entry.getValue();
        BigDecimal roundedTotal = new BigDecimal(totalClaimCost).setScale(2, RoundingMode.HALF_UP);
        agentToTotalClaimCostMap.put(entry.getKey(), roundedTotal.floatValue());
    }

    return agentToTotalClaimCostMap;
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
        Disaster disaster = findDisasterById(id);
        if (disaster == null) {
            return 0.0f; // Return null if the disaster does not exist
        }

        int numClaims = getNumClaimsForDisaster(id);
        double radius = disaster.getRadius_miles();
        double area = Math.PI * Math.pow(radius, 2);
        double density = numClaims / area;

        BigDecimal densityBigDecimal = BigDecimal.valueOf(density);
        densityBigDecimal = densityBigDecimal.setScale(3, RoundingMode.HALF_EVEN);
        
        return densityBigDecimal.floatValue();
    }

    private Disaster findDisasterById(int id) {
        for (Disaster disaster : disasters) {
            if (disaster.getId() == id) {
                return disaster;
            }
        }
        return null;
    }

    private int getNumClaimsForDisaster(int id) {
        int count = 0;
        for (Claim claim : claims) {
            if (claim.getDisaster_id() == id) {
                count++;
            }
        }
        return count;
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