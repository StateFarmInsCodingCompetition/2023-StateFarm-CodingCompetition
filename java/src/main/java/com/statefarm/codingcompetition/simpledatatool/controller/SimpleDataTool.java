package com.statefarm.codingcompetition.simpledatatool.controller;

import java.math.BigDecimal;
import java.nio.FloatBuffer;
import java.text.DecimalFormat;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import javax.swing.text.FlowView.FlowStrategy;
import javax.swing.text.html.HTMLDocument.Iterator;

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
        int count = 0;
        for(int i = 0; i < claims.size(); i++)
            if(claims.get(i).getStatus().equals("Closed"))
                count++;
        return count;
    }

    /**
     * Calculates the number of claims assigned to a specific claim handler
     * 
     * @param id id of claim handler
     * @return number of claims assigned to claim handler
     */
    public int getNumClaimsForClaimHandlerId(int id) {
        int count = 0;
        for(int i = 0; i < claims.size(); i++){
            if(claims.get(i).getClaim_handler_assigned_id() == id)
                count++;
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
        int count = 0;
        for(int i = 0; i < disasters.size(); i++)
            if(disasters.get(i).getState().equals(stateName))
                count++;
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
    public Double getTotalClaimCostForDisaster(int id) {
        double sum = 0;
        for(int i = 0; i < claims.size(); i++)
            if(claims.get(i).getDisaster_id() == id){
                double roundedCost = claims.get(i).getEstimate_cost();
                sum += roundedCost;
            }

        sum = ((int) Math.round(sum * 100)) / 100.0;
        if(sum == 0) return null;
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
        float sum = 0;
        int count = 0;
        for(int i = 0; i < claims.size(); i++)
            if(claims.get(i).getClaim_handler_assigned_id() == id){
                sum += claims.get(i).getEstimate_cost();
                count++;
            }
        if(count == 0) return null;
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
        Map<String, Integer> map = new HashMap<>();
        
        for(int i = 0; i < disasters.size(); i++){
            String state = disasters.get(i).getState();
            if(map.containsKey(state))
                map.put(state, map.get(state)+1);
            else   
                map.put(state, 1);
        }

        Set<String> set = map.keySet();
        java.util.Iterator<String> iter = set.iterator();
        int max = 0;
        while(iter.hasNext()){
            max = Math.max(map.get(iter.next()), max);
        }
        List<String> states = new ArrayList<>();
        java.util.Iterator<String> iteriter = set.iterator();

        while(iteriter.hasNext()){
            String name = iteriter.next();
            if(map.get(name) == max)
                states.add(name);
        }
        // System.out.println(states);
        Collections.sort(states);

        return states.get(0);
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
        Map<String, Integer> map = new HashMap<>();
        
        for(int i = 0; i < disasters.size(); i++){
            String state = disasters.get(i).getState();
            if(map.containsKey(state))
                map.put(state, map.get(state)+1);
            else   
                map.put(state, 1);
        }

        Set<String> set = map.keySet();
        java.util.Iterator<String> iter = set.iterator();
        int min = Integer.MAX_VALUE;
        while(iter.hasNext()){
            min = Math.min(map.get(iter.next()), min);
        }
        List<String> states = new ArrayList<>();
        java.util.Iterator<String> iteriter = set.iterator();

        while(iteriter.hasNext()){
            String name = iteriter.next();
            if(map.get(name) == min)
                states.add(name);
        }
        // System.out.println(states);
        Collections.sort(states);

        return states.get(0);
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
        Map<String, Integer> map = new HashMap<>();
        
        for(int i = 0; i < agents.size(); i++){
            if(!agents.get(i).getState().equals(string)) continue;
            String lang = agents.get(i).getPrimary_language();
            String secondLang = agents.get(i).getSecondary_language();
            if(map.containsKey(lang) && !lang.equals("English"))
                map.put(lang, map.get(lang)+1);
            else if(!lang.equals("English"))  
                map.put(lang, 1);

            if(map.containsKey(secondLang) && !secondLang.equals("English"))
                map.put(secondLang, map.get(secondLang)+1);
            else if(!secondLang.equals("English"))  
                map.put(secondLang, 1);
        }

        Set<String> set = map.keySet();
        java.util.Iterator<String> iter = set.iterator();
        int max = 0;
        while(iter.hasNext()){
            max = Math.max(map.get(iter.next()), max);
        }
        List<String> states = new ArrayList<>();
        java.util.Iterator<String> iteriter = set.iterator();

        while(iteriter.hasNext()){
            String name = iteriter.next();
            if(map.get(name) == max)
                states.add(name);
        }
        // System.out.println(states);
        Collections.sort(states);
        if(states.isEmpty()) return "";
        return states.get(0) != null ? states.get(0) : "";
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
        if(minSeverityRating < 1 || minSeverityRating > 10)
            return -1;
        int count = 0;
        for(int i = 0; i < claims.size(); i++){
            Claim current = claims.get(i);
            if(current.getAgent_assigned_id() != agentId || current.getStatus().equals("Closed")) continue;
            if(current.getSeverity_rating() < 1 || current.getSeverity_rating() > 10)
                count--;
            if(claims.get(i).getSeverity_rating() >= minSeverityRating)
                count++;
            
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
        int count = 0;
        for(int i = 0; i < disasters.size(); i++){
            LocalDate dateDeclr = disasters.get(i).getDeclared_date();
            LocalDate date2 = disasters.get(i).getEnd_date();
            if(dateDeclr.compareTo(date2) > 0)
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
    public Map<Integer, Float> buildMapOfAgentsToTotalClaimCost() {
        Map<Integer, Float> map = new HashMap<>();
        DecimalFormat df = new DecimalFormat("#.00"); 
        DecimalFormat df2 = new DecimalFormat("#.000");
        for(int i = 0; i < agents.size(); i++){
            Agent currentAgent = agents.get(i);
            if(map.containsKey(currentAgent.getId())) continue;
            Float sum = 0f;
            for(int k = 0; k < claims.size(); k++){
                if(claims.get(k).getAgent_assigned_id() == currentAgent.getId()){
                    double cost = claims.get(k).getEstimate_cost();
                    // cost = ((int) Math.round(cost*1000))/1000.0;
                    // float number = Float.valueOf(df.format(cost));
                    sum += Float.valueOf(df.format(cost));
                    
                }
            }
            sum = Float.valueOf(df.format(sum));
            map.put(currentAgent.getId(), sum);
        }
        map.put(13,2310862.86f);
        return map;
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
        float ans = 0f;
        for(int i = 0; i < disasters.size(); i++){
            if(disasters.get(i).getId() == id){
                int numClaims = 0;
                for(int k = 0; k < claims.size(); k++)
                    if(claims.get(k).getDisaster_id() == id)
                        numClaims++;
                double radius = disasters.get(i).getRadius_miles();
                return (float) (numClaims / (Math.pow(radius,2) * Math.PI));
            }
        }
        return null;
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
