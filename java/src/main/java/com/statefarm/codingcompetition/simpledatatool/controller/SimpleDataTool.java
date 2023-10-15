package com.statefarm.codingcompetition.simpledatatool.controller;

import java.text.CollationElementIterator;
import java.text.SimpleDateFormat;
import java.time.LocalDate;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicReference;
import java.util.stream.Collectors;

import com.statefarm.codingcompetition.simpledatatool.io.JsonHelper;
import com.statefarm.codingcompetition.simpledatatool.model.Agent;
import com.statefarm.codingcompetition.simpledatatool.model.Claim;
import com.statefarm.codingcompetition.simpledatatool.model.ClaimHandler;
import com.statefarm.codingcompetition.simpledatatool.model.Disaster;

import static java.util.stream.Collectors.toList;

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
        return (int) this.claims.stream().filter(claim -> claim.getStatus().equals("Closed")).count();
    }

    /**
     * Calculates the number of claims assigned to a specific claim handler
     * 
     * @param id id of claim handler
     * @return number of claims assigned to claim handler
     */
    public int getNumClaimsForClaimHandlerId(int id) {
        return (int) this.claims.stream().filter(claim -> claim.getClaim_handler_assigned_id() == id ).count();
    }

    /**
     * Calculates the number of disasters for a specific state
     * 
     * @param stateName name of a state in the United States of America,
     *                  including the District of Columbia
     * @return number of disasters for state
     */
    public int getNumDisastersForState(String stateName) {

        return (int) this.disasters.stream().filter(disaster -> disaster.getState().equals(stateName)).count();
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
        if (this.claims.stream().anyMatch(claim -> claim.getDisaster_id() == id)) {
            return this.claims.stream().filter(claim -> claim.getDisaster_id() == id).mapToDouble(Claim::getEstimate_cost).sum();
        }
        return null;
    }

    /**
     * Gets the average estimated cost of all claims assigned to a claim handler
     * 
     * @param id id of claim handler
     * @return average cost of claims, rounded to the nearest hundredths place,
     *         or null if no claims are found
     */
    public Float getAverageClaimCostforClaimHandler(int id) {
        if (this.claims.stream().anyMatch(claim -> claim.getClaim_handler_assigned_id() == id)) {
            return (float) this.claims.stream().filter(claim -> claim.getClaim_handler_assigned_id() == id).mapToDouble(Claim::getEstimate_cost).average().orElse(0.0);
        }
        return null;
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
        Map<String, Long> stateAndDisasterCount = this.disasters.stream()
                .collect(Collectors.groupingBy(disaster -> disaster.getState(), Collectors.counting()));

        List<String> orderedStates = stateAndDisasterCount.entrySet().stream()
                .sorted(Map.Entry.<String, Long>comparingByValue().reversed().thenComparing(Map.Entry.comparingByKey()))
                .map(Map.Entry::getKey)
                .collect(toList());

        return orderedStates.get(0);
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
        Map<String, Long> stateAndDisasterCount = this.disasters.stream()
                .collect(Collectors.groupingBy(disaster -> disaster.getState(), Collectors.counting()));

        List<String> orderedStates = stateAndDisasterCount.entrySet().stream()
                .sorted(Map.Entry.<String, Long>comparingByValue().thenComparing(Map.Entry.comparingByKey()))
                .map(Map.Entry::getKey)
                .collect(toList());

        return orderedStates.get(0);
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
        Map<String, Long> languageCount = this.agents.stream()
                .filter(agent -> agent.getState().equals(string))
                .collect(Collectors.groupingBy(agent -> agent.getSecondary_language(), Collectors.counting()));

        List<String> orderedLanguages = languageCount.entrySet().stream()
                .sorted(Map.Entry.<String, Long>comparingByValue().reversed().thenComparing(Map.Entry.comparingByKey()))
                .map(Map.Entry::getKey)
                .collect(toList());

        if (languageCount.size() == 0 || orderedLanguages.get(0) == "null")
            return "";

        return orderedLanguages.get(0);
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
        } else if(this.agents.stream().noneMatch(agent -> agent.getId() == agentId) ||
                this.claims.stream().noneMatch(claim -> claim.getAgent_assigned_id() == agentId)) {
            return null;
        } else {
            return (int) this.claims.stream().filter(claim -> claim.getAgent_assigned_id() == agentId
                    && !claim.getStatus().equals("Closed") &&
                    claim.getSeverity_rating() >= minSeverityRating).count();
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
        return (int) this.disasters.stream()
                .filter(disaster -> disaster.getDeclared_date().compareTo(disaster.getEnd_date()) > 0)
                .count();
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

        Map<Integer, Double> agents_WithClaims_To_ClaimCost = this.claims.stream()
                .collect(Collectors.groupingBy(claim -> claim.getAgent_assigned_id(), Collectors.summingDouble(Claim::getEstimate_cost)));

        Map<Integer, Float> agents_To_Total_ClaimCost = new HashMap<>();

        for (Agent agent: this.agents) {
            agents_To_Total_ClaimCost.put(agent.getId(), (float) agents_WithClaims_To_ClaimCost.getOrDefault(agent.getId(), Double.valueOf(0)).doubleValue());
        }
        return agents_To_Total_ClaimCost;
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
        if (this.disasters.stream().noneMatch(disaster -> disaster.getId() == id)) return -1;

        List<Disaster> disasterRecord = this.disasters.stream().filter(disaster -> disaster.getId() == id).collect(Collectors.toList());

        double area = Math.PI * Math.pow(disasterRecord.get(0).getRadius_miles(), 2);

        double numOfClaims = this.claims.stream().filter(claim -> claim.getDisaster_id() == id).count();

        return (float) ((float) numOfClaims/area);

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

        Map<Integer, String> id_To_monthYear = new HashMap<>();

        for (Disaster disaster : this.disasters) {
            id_To_monthYear.put(disaster.getId(), getMonthAndYear(disaster.getDeclared_date()));
        }

        Map<String, Double> monthYear_To_TotalCost = new HashMap<>();

        for (Claim claim: this.claims) {
            String key = id_To_monthYear.get(claim.getDisaster_id());

            if (monthYear_To_TotalCost.containsKey(key)) {
                monthYear_To_TotalCost.put(key, monthYear_To_TotalCost.get(key) + claim.getEstimate_cost());
            } else {
                monthYear_To_TotalCost.put(key, claim.getEstimate_cost());
            }
        }

        List<String> monthYear_Desc_Order = monthYear_To_TotalCost.entrySet().stream()
                .sorted(Map.Entry.<String, Double>comparingByValue().reversed())
                .map(Map.Entry::getKey)
                .collect(toList());


        return monthYear_Desc_Order.subList(0, 3).toArray(new String[0]);
    }

    static String getMonthAndYear(LocalDate date) {
        return convertToSupperCase(String.valueOf(date.getMonth())) + " " + date.getYear();
    }

    static String convertToSupperCase(String input) {
        String firstLetter = input.substring(0, 1).toUpperCase();
        String restOfWord = input.substring(1).toLowerCase();
        return firstLetter + restOfWord;
    }

    // endregion
}
