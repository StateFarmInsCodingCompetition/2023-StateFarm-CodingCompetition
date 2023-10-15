const sfcc2023Agents = require("./data/sfcc_2023_agents.json");
const sfcc2023ClaimHandlers = require("./data/sfcc_2023_claim_handlers.json");
const sfcc2023Claims = require("./data/sfcc_2023_claims.json");
const sfcc2023Disasters = require("./data/sfcc_2023_disasters.json");

class SimpleDataTool {
    constructor() {
        this.REGION_MAP = {
            west: "Alaska,Hawaii,Washington,Oregon,California,Montana,Idaho,Wyoming,Nevada,Utah,Colorado,Arizona,New Mexico",
            midwest:
                "North Dakota,South Dakota,Minnesota,Wisconsin,Michigan,Nebraska,Iowa,Illinois,Indiana,Ohio,Missouri,Kansas",
            south:
                "Oklahoma,Texas,Arkansas,Louisiana,Kentucky,Tennessee,Mississippi,Alabama,West Virginia,Virginia,North Carolina,South Carolina,Georgia,Florida",
            northeast:
                "Maryland,Delaware,District of Columbia,Pennsylvania,New York,New Jersey,Connecticut,Massachusetts,Vermont,New Hampshire,Rhode Island,Maine",
        };
    }

    /**
     * Calculates the number of claims where the status is "Closed"
     *
     * @returns {number} number of closed claims
     */
    getNumClosedClaims() {
        let closedClaims = sfcc2023Claims.filter((x) => x.status == "Closed");
        return closedClaims.length;
    }

    /**
     * Calculates the number of claims assigned to a specific claim handler.
     *
     * @param {number} claimHandlerId - ID of the claim handler.
     * @returns {number} - Number of claims assigned to the claim handler.
     */
    getNumClaimsForClaimHandlerId(claimHandlerId) {
        let claims = sfcc2023Claims.filter((x) => x.claim_handler_assigned_id == claimHandlerId);
        return claims.length;
    }

    /**
     * Calculates the number of disasters for a specific state.
     *
     * @param {string} state - Name of a state in the United States of America, including the District of Columbia.
     * @returns {number} - Number of disasters for the state.
     */
    getNumDisastersForState(state) {
        let claims = sfcc2023Disasters.filter((x) => x.state == state);
        return claims.length;
    }

    /**
     * Sums the estimated cost of a specific disaster by its claims.
     *
     * @param {number} disasterId - ID of disaster.
     * @returns {number|null} - Estimate cost of disaster, rounded to the nearest hundredths place,
     *                          or null if no claims are found.
     */
    getTotalClaimCostForDisaster(disasterId) {
        let disasterClaims = sfcc2023Claims.filter((x) => x.disaster_id == disasterId);
        if(disasterClaims.length <= 0){
            return null;
        }
        let costSum = 0.0;
        for(let i = 0; i < disasterClaims.length; i++){
            costSum += disasterClaims[i].estimate_cost;
        }

        return Number(costSum.toFixed(2));
    }

    /**
     * Gets the average estimated cost of all claims assigned to a claim handler.
     *
     * @param {number} claimHandlerId - ID of claim handler.
     * @returns {number|null} - Average cost of claims, rounded to the nearest hundredths place,
     *                          or null if no claims are found.
     */
    getAverageClaimCostForClaimHandler(claimHandlerId) {
        let claims = sfcc2023Claims.filter((x) => x.claim_handler_assigned_id == claimHandlerId);
        if(claims.length < 1){
            return null;   
        }
        let total = 0;
        for(let i = 0; i < claims.length; i++){
            total = total + claims[i].estimate_cost
        }
        let avg = total / claims.length;

        return Number(avg.toFixed(2));
        
    }

    /**
     * Returns the name of the state with the most disasters based on disaster data.
     * If two states have the same number of disasters, then sorts by alphabetical (a-z)
     * and takes the first.
     *
     * @returns {string} - Single name of state
     */
    getStateWithMostDisasters() {
        let dict = {};
        sfcc2023Disasters.forEach( x => {
            if(!dict[x.state]){
                dict[x.state] = 0;
            }
            dict[x.state]++;
        })
        let highestVal = Number.MIN_VALUE;
        let highestKey = null;
        let keys = Object.keys(dict);
        let dictSize = keys.length;
        for(let i = 0; i < dictSize; i++){
            if(dict[keys[i]] >= highestVal){
                if(dict[keys[i]] != highestVal || (highestKey == null || keys[i] < highestKey)){
                    highestVal = dict[keys[i]];
                    highestKey = keys[i];
                }
            }
        }
        return highestKey;
    }

    /**
     * Returns the name of the state with the least disasters based on disaster data.
     * If two states have the same number of disasters, then sorts by alphabetical (a-z)
     * and takes the first.
     *
     * Example: Say New Mexico and West Virginia both have the least number of disasters at
     *          1 disaster each. Then, this method would return "New Mexico" since "N"
     *          comes before "W" in the alphabet.
     *
     * @returns {string} - Single name of state
     */
    getStateWithLeastDisasters() {
        let dict = {};
        sfcc2023Disasters.forEach( x => {
            if(!dict[x.state]){
                dict[x.state] = 0;
            }
            dict[x.state]++;
        })
        let lowestVal = Number.MAX_VALUE;
        let lowestKey = null;
        let keys = Object.keys(dict);
        let dictSize = keys.length;
        for(let i = 0; i < dictSize; i++){
            if(dict[keys[i]] <= lowestVal){
                if(dict[keys[i]] != lowestVal || (lowestKey == null || keys[i] < lowestKey)){
                    lowestVal = dict[keys[i]];
                    lowestKey = keys[i];
                }
            }
        }
        return lowestKey;
    }

    /**
     * Returns the name of the most spoken language by agents (besides English) for a specific state.
     *
     * @param {string} state - Name of state.
     * @returns {string} - Name of language, or empty string if state doesn't exist.
     */
    getMostSpokenAgentLanguageByState(state) {
        let langCount = {};

        let bilinguals = sfcc2023Agents.filter(x => (x.state === state && x.secondary_language));
        if(bilinguals.length < 1){
            return "";
        }

        bilinguals.forEach(x => {
            if(!langCount[x.secondary_language]){
                langCount[x.secondary_language] = 0;
            }
            langCount[x.secondary_language]++;
        });

        let highestVal = Number.MIN_VALUE;
        let highestKey = "";
        let keys = Object.keys(langCount);
        let dictSize = keys.length;

        for(let i = 0; i < dictSize; i++){
            if(langCount[keys[i]] >= highestVal){
                if(langCount[keys[i]] != highestVal || (highestKey == "" || keys[i] < highestKey)){
                    highestVal = langCount[keys[i]];
                    highestKey = keys[i];
                }
            }
        }
        return highestKey;
    }

    /**
     * Returns the number of open claims for a specific agent and for a minimum severity level and higher.
     *
     * Note: Severity rating scale for claims is 1 to 10, inclusive.
     *
     * @param {number} agentId - ID of the agent.
     * @param {number} minSeverityRating - Minimum severity rating to consider.
     * @returns {number|null} - Number of claims that are not closed and have minimum severity rating or greater,
     *                          -1 if severity rating out of bounds,
     *                          null if agent does not exist, or agent has no claims (open or not).
     */
    getNumOfOpenClaimsForAgentAndSeverity(agentId, minSeverityRating) {
        if(minSeverityRating < 1 || minSeverityRating > 10){
            return -1;
        }
        let claims = sfcc2023Claims.filter((x) => {return (x.agent_assigned_id == agentId )&&(x.severity_rating >= minSeverityRating)&&(x.status != "Closed")})
        if(claims.length < 1){
            return null;
        }
        return claims.length;
    }

    /**
     * Gets the number of disasters where it was declared after it ended.
     *
     * @returns {number} - Number of disasters where the declared date is after the end date.
     */
    getNumDisastersDeclaredAfterEndDate() {
        let count = 0;
        sfcc2023Disasters.forEach(x => {
            let d_day = this.dateHelper(x.declared_date);
            let e_day = this.dateHelper(x.end_date)
            if(d_day > e_day){
                count++;
            }
        })
        return count;
    }

    /** Builds a map of agent and their total claim cost
     *
     * Hints:
     *     An agent with no claims should return 0
     *     Invalid agent id should have a value of Undefined
     *     You should round your totalClaimCost to the nearest hundredths
     *
     *  @returns {Object}: key is agent id, value is total cost of claims associated to the agent
     */
    buildMapOfAgentsToTotalClaimCost() {
        let dict = {};
        sfcc2023Agents.forEach(x => {dict[x.id] = 0});
        sfcc2023Claims.forEach( x =>{
            if(x.agent_assigned_id > 0 && x.agent_assigned_id < 101){
                dict[x.agent_assigned_id] =  Number((dict[x.agent_assigned_id]+ x.estimate_cost).toFixed(2));
            }
        });
        
        return dict;
    }

    /**  Calculates density of a disaster based on the number of claims and impact radius
     *
     * Hints:
     *     Assume uniform spacing between claims
     *     Assume disaster impact area is a circle
     *
     * @param {number} disasterId - ID of disaster.
     * @returns {number} density of claims to disaster area, rounded to the nearest thousandths place
     * null if disaster does not exist
     */
    calculateDisasterClaimDensity(disasterId) {
        let disaster = sfcc2023Disasters.filter(x => x.id == disasterId);
        if(disaster.length == 0) {
            return null;
        }
        let claimCount = 0;
        sfcc2023Claims.forEach(x => {
            if(x.disaster_id == disasterId){
                claimCount++;
            }
        })
        let disasterArea = (Math.PI * Math.pow(disaster[0].radius_miles,2))
        return Number((claimCount / disasterArea).toFixed(5));
        
    }

    /**
     * Gets the top three months with the highest total claim cost.
     *
     * Hint:
     *     Month should be full name like 01 is January and 12 is December.
     *     Year should be full four-digit year.
     *     List should be in descending order.
     *
     * @returns {Array} - An array of three strings of month and year, descending order of highest claims.
     */
    getTopThreeMonthsWithHighestNumOfClaimsDesc() {
        let disasterMap = {}
        let dateMap = {}
        let arr = [];
        let dateOptions = {year: 'numeric', month:'long'}

        sfcc2023Disasters.forEach(x => {
            let date = this.dateHelper(x.declared_date)
            let dateStr = date.toLocaleDateString(undefined,dateOptions)
            disasterMap[x.id] = dateStr;
            if(dateMap[dateStr] == undefined){
                dateMap[dateStr] = arr.push({str:dateStr,count:0,claims:[]}) - 1;
            }
        });

        sfcc2023Claims.forEach( x => {
            let key = dateMap[disasterMap[x.disaster_id]];
            arr[key].count++;
            arr[key].claims.push(x.id);
        });

        arr.sort( (x,y) => {return y.count - x.count});
        arr.splice(3);
        let fin = arr.map(x => x.str);

        return fin;
    }

    dateHelper(dateStr){
        let splitStr = dateStr.split('-');
        return new Date(splitStr[0],splitStr[1] - 1,splitStr[2]);
    }

    
}

module.exports = SimpleDataTool;