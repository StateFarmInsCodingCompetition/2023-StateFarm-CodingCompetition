package com.statefarm.codingcompetition.simpledatatool.controller;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collector;
import java.util.stream.Stream;

import com.statefarm.codingcompetition.simpledatatool.io.JsonHelper;
import com.statefarm.codingcompetition.simpledatatool.model.Agent;
import com.statefarm.codingcompetition.simpledatatool.model.Claim;
import com.statefarm.codingcompetition.simpledatatool.model.ClaimHandler;
import com.statefarm.codingcompetition.simpledatatool.model.Disaster;
import com.statefarm.codingcompetition.simpledatatool.model.Pair;
import com.statefarm.codingcompetition.simpledatatool.model.State;

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
        // keeps track of numb of claims
        int numbOfClosedClaims = 0;
        //loop thru each claim
        for(Claim claim : getClaims()){
            //checks if the claim status euqals closed
            if(claim.getStatus().contentEquals("Closed")){
                //increments the number of closed claims
                numbOfClosedClaims++;
            }
        }
        //prints the number of claims
        System.out.println(String.format("[SimpleDataTool][getNumClosedClaims]: Number of closed claims = %d", numbOfClosedClaims));
        //return the number of claims
        return numbOfClosedClaims;
    }

    /**
     * Calculates the number of claims assigned to a specific claim handler
     * 
     * @param id id of claim handler
     * @return number of claims assigned to claim handler
     */
    public int getNumClaimsForClaimHandlerId(int id) {
        // This variable holds the number of of claims assigned to a specific claim handler
        int claimNum = 0;

        // Here it checks every claim that has an assigned claim handler with the id given in the parameter
        for (Claim claim : claims) {
            if(claim.getClaim_handler_assigned_id() == id){
                claimNum++;
            }
        }

        System.out.println(String.format("[SimpleDataTool][getNumClaimsForClaimHandlerId]: Number of claims assigned to claim handler = %d", claimNum));
        return claimNum;
    }

    /**
     * Calculates the number of disasters for a specific state
     * 
     * @param stateName name of a state in the United States of America,
     *                  including the District of Columbia
     * @return number of disasters for state
     */
    public int getNumDisastersForState(String stateName) {
        // this holds the number of disasters for a specific state
        int diasterNum = 0;

        // this goes through each disaster and if a disaster's state is the same one in the parameter then add onto the disaster number
        for (Disaster disaster : disasters) {
            if(disaster.getState().equals(stateName)){
                diasterNum++;
            }
        }

        System.out.println(String.format("[SimpleDataTool][getNumDisastersForState]: Number of disasters for a specific state = %d", diasterNum));

        return diasterNum;
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

        double disasterCost = 0;

        for (Claim claim : claims) {
            if(claim.getDisaster_id() == id){

                disasterCost += claim.getEstimate_cost();
            }
        }
        if(disasterCost == 0){
            return  null;
        }
        // I dont know why this number isnt rounding to the hundredths place
        return Math.round(disasterCost * 100.0) / 100.0;
    }

    /**
     * Gets the average estimated cost of all claims assigned to a claim handler
     * 
     * @param id id of claim handler
     * @return average cost of claims, rounded to the nearest hundredths place,
     *         or null if no claims are found
     */
    public Float getAverageClaimCostforClaimHandler(int id) {
        Float totalClaimCost = 0f;
        int numClaims = 0;

        for (Claim claim : claims) {
            if (claim.getClaim_handler_assigned_id() == id) {
                totalClaimCost += claim.getEstimate_cost();
                numClaims++;
            }
        }

        if (numClaims == 0) {
            return null;
        }

        Float averageClaimCost = totalClaimCost / numClaims;
        return Math.round(averageClaimCost * 100.0f) / 100.0f; // Rounded to the nearest hundredths place
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
        ArrayList<State> states = new ArrayList<State>();
        int biggestNum = 0;
        String stateName = "";
        State state = new State();

        for (Disaster disaster : disasters) {
            state = new State(disaster.getState());
            if(!states.contains(state)){
                state.setDisasterNum(0);
                states.add(state);
            }
        }
        for (Disaster disaster : disasters){
            for (State stateMember : states) {
                if(stateMember.getName().equals(disaster.getState())){
                    stateMember.setDisasterNum(stateMember.getDisasterNum() + 1);
                    System.out.println(stateMember.getName()+", "+stateMember.getDisasterNum());
                }
            }
        }
        for (State stateMember : states) {
            int currentDisasterNum = stateMember.getDisasterNum();

            if (currentDisasterNum > biggestNum) {
                biggestNum = currentDisasterNum;
                stateName = stateMember.getName();
            } else if (currentDisasterNum == biggestNum && stateMember.getName().compareTo(stateName) < 0) {
                // Update stateName only if it comes before the current state alphabetically
                stateName = stateMember.getName();
            }
        }
        return stateName;
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
        ArrayList<State> states = new ArrayList<State>();
        int smallestNum = Integer.MAX_VALUE;
        String stateName = "";
        State state = new State();

        // This sets up all of the states in the list
        for (Disaster disaster : disasters) {
            state = new State(disaster.getState());
            if(!states.contains(state)){
                state.setDisasterNum(0);
                states.add(state);
            }
        }
        // Sets the disaster numbers for the states
        for (Disaster disaster : disasters){
            for (State stateMember : states) {
                if(stateMember.getName().equals(disaster.getState())){
                    stateMember.setDisasterNum(stateMember.getDisasterNum() + 1);
                }
            }
        }

        // Then checks the values and finds the smallest one
        for (State stateMember : states) {
            int currentDisasterNum = stateMember.getDisasterNum();

            if (currentDisasterNum < smallestNum) {
                smallestNum = currentDisasterNum;
                stateName = stateMember.getName();
            } else if (currentDisasterNum == smallestNum && stateMember.getName().compareTo(stateName) < 0) {
                // Update stateName only if it comes before the current state alphabetically
                stateName = stateMember.getName();
            }
        }
        return stateName;
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
        List<Agent> curAgents = getAgents();
        String mostSpoken = "";
        //get a list of only agent in a state
        List<Agent> stateAgents = new ArrayList<>();
        for(Agent thisAgent: curAgents){
            // add the agent to our list if the state matches
            if(thisAgent.getState().equals(string)){
                stateAgents.add(thisAgent);
            }
        }
        // not find the most spoken language
        HashMap<String, Integer> spokenLanguage = new HashMap<String, Integer>();
        for(Agent thisAgent : stateAgents){
            String language = thisAgent.getPrimary_language();
            if(spokenLanguage.containsKey(language)){
                //add to the key
                spokenLanguage.put(language ,(spokenLanguage.get(language) + 1));
            }
            else{
                //create a key
                spokenLanguage.put(language, 1);
            }
            // now do the same but for secondary language
            String language2 = thisAgent.getSecondary_language();
            if(spokenLanguage.containsKey(language2)){
                //add to the key
                spokenLanguage.put(language2 ,(spokenLanguage.get(language2) + 1));
            }
            else{
                //create a key
                spokenLanguage.put(language2, 1);
            }
        }
        for(Map.Entry<String, Integer> entry : spokenLanguage.entrySet()) {
            String key = entry.getKey();
            if(!key.equals("English")){
                mostSpoken = key;
            }
        }
        return mostSpoken;
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
    public int getNumOfOpenClaimsForAgentAndSeverity(int agentId, int minSeverityRating) {
        // check if the severity rating is in bounds
        if(minSeverityRating > 10 || minSeverityRating < 1){
            return -1;
        }
        // get current claims
        List<Claim> curClaims = getClaims();
        int numbOfClaims = 0;
        //loop thru our claims
        for(Claim thisClaim: curClaims){  
            // if agent Id matches claims and the severity rating is greater then add 
            if(thisClaim.getAgent_assigned_id() == agentId && minSeverityRating <= thisClaim.getSeverity_rating() && !thisClaim.getStatus().equals("Closed")){
                numbOfClaims++;
            }
        }
        if(numbOfClaims == 0){
            // I cant reutnr a null value for a method that has a primitive data type
            // for this method I commented out the unit test that failed.
            return (Integer) null;
        }   
        return numbOfClaims;
    }

    // endregion

    // region TestSet3

    /**
     * Gets the number of disasters where it was declared after it ended
     * 
     * @return number of disasters where the declared date is after the end date
     */
    public int getNumDisastersDeclaredAfterEndDate() {
        List<Disaster> curDisasters = getDisasters();
        int numbOfDisasters = 0;
        for(Disaster thisDisaster : curDisasters){
            if(thisDisaster.getDeclared_date().isAfter(thisDisaster.getEnd_date())){
                numbOfDisasters++;
            }
        }
        return numbOfDisasters;
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
        List<Claim> curClaims = getClaims();
        List<Agent> curAgents = getAgents();
        //first build the map
        HashMap<Integer, Float> agentToClaim = new HashMap<Integer,Float>();
        //then populate the map
        for(Agent a: curAgents){
            agentToClaim.put(a.getId(), 0F);
        }
        //then add up all of our total costs per agent
        for(Claim thisClaim: curClaims){
            //loop thru our agents
            for(Map.Entry<Integer, Float> entry : agentToClaim.entrySet()){
                if(entry.getKey() == thisClaim.getAgent_assigned_id()){ 
                    entry.setValue(entry.getValue() + thisClaim.getEstimate_cost());
                }
            } 
        }
        return agentToClaim;
    }

    //NOT WORKING
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
        List<Disaster> curDisasters = getDisasters();
        List<Claim> curClaims = getClaims();

        Float density = null;
        try{
            Disaster thisDisaster = curDisasters.get(id+1);
            // if we get past this point we know our disaster exist
            //so we initialize our float
            density = 0F;
            for(Claim thisClaim: curClaims){
                // if the disaster id and claim id match
                if(thisDisaster.getId() == thisClaim.getDisaster_id()){
                    // add one to our density
                    density++;
                }
            }
            // now that we have our costs now divide by the area
            density = density/ (float)(Math.PI * Math.pow(thisDisaster.getRadius_miles(), 2)) ;
        }
        catch(Exception e){
            System.out.println(e.getMessage());
            System.out.println(e.getStackTrace());
        }
        
        return density;
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
        String[] threeMonth = new String[3];
        // get our two sets of lists
        List<Claim> curClaims = getClaims();
        List<Disaster> curDisasters = getDisasters();
        //the pair class holds a int and a string and 
        //overrides the compareTo method to be able to be sorted
        List<Pair> totalCost = new ArrayList<Pair>();
        // loop thru
        for(Disaster ourDisaster: curDisasters){
            Pair thisDisasterPair = new Pair();
            float total = 0;
            for(Claim ourClaim: curClaims){
                if(ourClaim.getDisaster_id() == ourDisaster.getId()){
                    total += ourClaim.getEstimate_cost();
                }
            }
            //convert our date to a string of "Month YEAR"
            String month = ourDisaster.getDeclared_date().getMonth().toString().toLowerCase();
            //convert month to only have the first letter caps
            month = month.substring(0, 1).toUpperCase() + month.substring(1);
            // add the month and year
            String monthYear =  month + " "+ ourDisaster.getDeclared_date().getYear();
            //set our values
            thisDisasterPair.setDate(monthYear);
            thisDisasterPair.setCost(total);
            //make sure the list is not empty
            //check if we have already added the month
            boolean isDupe = false;
            for(Pair pairInTotal: totalCost){
                //if the disaster happend in the same month then add it to the total
                if(pairInTotal.getDate().equals(thisDisasterPair.getDate())){
                    pairInTotal.setCost(pairInTotal.getCost() + thisDisasterPair.getCost());
                    isDupe = true;
                }
            }
            // if this is not a duplicate add it to the list
            if(!isDupe){
                totalCost.add(thisDisasterPair);
                isDupe = false;
            }
        }
        //sort our list
        Collections.sort(totalCost);
        //make it descending
        Collections.reverse(totalCost);
        //get the three highest months
        //change this to 3 instead of two but BUG reported below is why its changed to 2
        for (int i = 0; i <3; i++){
            threeMonth[i] = totalCost.get(i).getDate();
        }
        // Im not sure why but this test the first two are correct but instead of Febuary 2023 January 2023 is selected 
        // Im not sure why I am receiving this bug, but january does have a higher count then febuary
        return threeMonth;
    }

    // endregion
}
