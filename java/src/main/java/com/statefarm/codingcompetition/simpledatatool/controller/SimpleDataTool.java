package com.statefarm.codingcompetition.simpledatatool.controller;

import com.statefarm.codingcompetition.simpledatatool.io.JsonHelper;
import com.statefarm.codingcompetition.simpledatatool.model.Agent;
import com.statefarm.codingcompetition.simpledatatool.model.Claim;
import com.statefarm.codingcompetition.simpledatatool.model.ClaimHandler;
import com.statefarm.codingcompetition.simpledatatool.model.Disaster;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class SimpleDataTool {

    private static final String JSON_FILENAME_AGENTS = "sfcc_2023_agents.json";
    private static final String JSON_FILENAME_CLAIM_HANDLERS = "sfcc_2023_claim_handlers.json";
    private static final String JSON_FILENAME_CLAIMS = "sfcc_2023_claims.json";
    private static final String JSON_FILENAME_DISASTERS = "sfcc_2023_disasters.json";

    private final List<Agent> agents;
    private final List<ClaimHandler> claimHandlers;
    private final List<Claim> claims;
    private final List<Disaster> disasters;

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
        int count = 0;
        for (Claim c : claims) {
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
        return 0;
    }

    /**
     * Calculates the number of disasters for a specific state
     *
     * @param stateName name of a state in the United States of America,
     *                  including the District of Columbia
     * @return number of disasters for state
     */
    public int getNumDisastersForState(String stateName) {
        int count = 0;
        for (Disaster d : disasters) {
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
     * returns null if no claims are found
     */
    public Float getTotalClaimCostForDisaster(int id) {
        return -0.01f;
    }

    /**
     * Gets the average estimated cost of all claims assigned to a claim handler
     *
     * @param id id of claim handler
     * @return average cost of claims, rounded to the nearest hundredths place,
     * or null if no claims are found
     */
    public Double getAverageClaimCostforClaimHandler(int id) {
        BigDecimal cost = BigDecimal.ZERO;
        int vals = 0;
        for (Claim c : claims) {
            if (c.getClaim_handler_assigned_id() == id) {
                cost = cost.add(BigDecimal.valueOf(c.getEstimate_cost()));
                vals++;
            }
        }
        if (vals == 0) {
            return null;
        }
        cost = cost.divide(BigDecimal.valueOf(vals), 2, RoundingMode.HALF_UP);
        return cost.doubleValue();
    }

    /**
     * Returns the name of the state with the most disasters based on disaster data
     * <p>
     * If two states have the same number of disasters, then sort by alphabetical
     * (a-z) and take the first.
     * <p>
     * Example: Say New Jersey and Delaware both have the highest number of
     * disasters at 12 disasters each. Then, this method would return "Delaware"
     * since "D"comes before "N" in the alphabet.
     *
     * @return single name of state
     */
    public String getStateWithTheMostDisasters() {
        return null;
    }

    /**
     * Returns the name of the state with the least disasters based on disaster data
     * <p>
     * If two states have the same number of disasters, then sort by alphabetical
     * (a-z) and take the first.
     * <p>
     * Example: Say New Mexico and West Virginia both have the least number of
     * disasters at 1 disaster each. Then, this method would return "New Mexico"
     * since "N" comes before "W" in the alphabet.
     *
     * @return single name of state
     */
    public String getStateWithTheLeastDisasters() {
        HashMap<String, Integer> hm = new HashMap<>();
        for (Disaster d : disasters) {
            hm.put(d.getState(), hm.getOrDefault(d.getState(), 0) + 1);
        }
        String minState = "";
        int min = Integer.MAX_VALUE;
        for (Map.Entry<String, Integer> x : hm.entrySet()) {
            if (x.getValue() < min) {
                min = x.getValue();
                minState = x.getKey();
            } else if (x.getValue() == min) {
                if (x.getKey().compareTo(minState) < 0) {
                    minState = x.getKey();
                }
            }
        }
        return minState;
    }

    /**
     * Returns the name of the most spoken language by agents (besides English) for
     * a specific state
     *
     * @param string name of state
     * @return name of language
     * or empty string if state doesn't exist
     */
    public String getMostSpokenAgentLanguageByState(String string) {
        return null;
    }

    /**
     * Returns the number of open claims for a specific agent and for a minimum
     * severity level and higher
     * <p>
     * Note: Severity rating scale for claims is 1 to 10, inclusive.
     *
     * @param agentId           id of agent
     * @param minSeverityRating minimum claim severity rating
     * @return number of claims that are not closed and have minimum severity rating
     * or greater
     * -1 if severity rating out of bounds
     * None if agent does not exist, or agent has no claims (open or not)
     */
    public int getNumOfOpenClaimsForAgentAndSeverity(int agentId, int minSeverityRating) {
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
        int count = 0;
        for (Disaster d : disasters) {
            LocalDate end = d.getEnd_date();
            LocalDate declared = d.getDeclared_date();
            if (end.isBefore(declared)) count++;
        }
        return count;
    }

    /**
     * Builds a map of agent and their total claim cost
     * <p>
     * Hints:
     * - An agent with no claims should return 0
     * - Invalid agent id should have a value of null
     * - You should round your total_claim_cost to the nearest hundredths
     *
     * @return Map where key is agent id, value is total cost of claims associated
     * to the agent
     */
    public Map<Integer, Double> buildMapOfAgentsToTotalClaimCost() {
        Map<Integer, BigDecimal> hm = new HashMap<>();
        Map<Integer, Double> bds = new HashMap<>();

        for (int i = 1; i < 101; i++) {
            hm.put(i, BigDecimal.ZERO);
        }
        for (Claim c : claims) {
            hm.put(c.getAgent_assigned_id(), hm.getOrDefault(c.getAgent_assigned_id(), BigDecimal.ZERO).add(BigDecimal.valueOf(c.getEstimate_cost())));
            if(c.getAgent_assigned_id() == 3) {
                System.out.println(hm.get(3));
            }
        }
        for (Map.Entry<Integer, BigDecimal> y : hm.entrySet()) {
            BigDecimal bd = y.getValue();
            bds.put(y.getKey(), bd.setScale(2, RoundingMode.HALF_UP).doubleValue());
        }
        return bds;
    }

    /**
     * Calculates density of a disaster based on the number of claims and impact
     * radius
     * <p>
     * Hints:
     * - Assume uniform spacing between claims
     * - Assume disaster impact area is a circle
     *
     * @param id id of disaster
     * @return density of claims to disaster area, rounded to the nearest
     * thousandths place
     * null if disaster does not exist
     */
    public Float calculateDisasterClaimDensity(int id) {
        int numClaims = 0;
        for (Claim c : claims) {
            if (c.getDisaster_id() == id) numClaims++;
        }
        if (numClaims == 0) {
            return null;
        }
        for (Disaster d : disasters) {
            if (d.getId() != id) continue;
            return (float) (numClaims / (Math.PI * Math.pow(d.getRadius_miles(), 2)));
        }
        return null;
    }

    // endregion

    // region TestSet4

    /**
     * Gets the top three months with the highest total claim cost
     * <p>
     * Hint:
     * - Month should be full name like 01 is January and 12 is December
     * - Year should be full four-digit year
     * - List should be in descending order
     *
     * @return three strings of month and year, descending order of highest claims
     */
    public String[] getTopThreeMonthsWithHighestNumOfClaimsDesc() {
        HashMap<Integer, Integer> claimsToDisasters = new HashMap<>();
        for (Claim c : claims) {
            claimsToDisasters.put(c.getId(), c.getDisaster_id());
        }
        HashMap<Integer, LocalDate> disastersToDates = new HashMap<>();
        for (Disaster d : disasters) {
            disastersToDates.put(d.getId(), d.getDeclared_date());
        }
        Map<String, Float> xm = new HashMap<>();
        for (Map.Entry<Integer, Integer> x : claimsToDisasters.entrySet()) {
            String month = disastersToDates.get(x.getValue()).getMonth().toString();
            String formattedMonth = month.charAt(0) + month.substring(1).toLowerCase() + " ";
            String year = String.valueOf(disastersToDates.get(x.getValue()).getYear());
            xm.put(formattedMonth + year, xm.getOrDefault(formattedMonth + year, 0f) + 1);
        }

        String[] sol = new String[3];
        for (int i = 0; i < 3; i++) {
            String Month = "";
            float val = 0f;
            for (Map.Entry<String, Float> x : xm.entrySet()) {
                if (x.getValue() > val) {
                    val = x.getValue();
                    Month = x.getKey();
                }
            }
            sol[i] = Month;
            xm.remove(Month);
        }

        return sol;
    }

    // endregion
}