import fs from "fs";

const sfcc2023Agents = JSON.parse(fs.readFileSync('./data/sfcc_2023_agents.json', 'utf8'));
const sfcc2023ClaimHandlers = JSON.parse(fs.readFileSync('./data/sfcc_2023_claim_handlers.json', 'utf8'));
const sfcc2023Claims = JSON.parse(fs.readFileSync('./data/sfcc_2023_claims.json', 'utf8'));
const sfcc2023Disasters = JSON.parse(fs.readFileSync('./data/sfcc_2023_disasters.json', 'utf8'));

const logicalOperators = {
	Equals:         Symbol("equals"),
	GreaterThan:    Symbol("greaterThan"),
	LessThan:       Symbol("lessThan"),
	NotEqual:       Symbol("notEqual"),
}
const stateList = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia',
    'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland',
    'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey',
    'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
    'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
  ];

export class SimpleDataTool {
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
    parseOnCondition(data, keyName, operator, targetValue){
        
        var matches = [];
        try{
            var dataSize = (data).length;
        }
        catch(e){
            throw new Error("unable to parse data in parseOnCondition")
        }

        try{
            let currentValue = null;
            switch (operator) {

                case logicalOperators.Equals:
                    for(let iter = 0 ; iter<dataSize; iter++){
                            currentValue = data[iter][keyName];
                        if(targetValue == currentValue){matches.push(data[iter])}
                    }
                break;

                case logicalOperators.GreaterThan:
                    for(let iter = 0 ; iter<dataSize; iter++){
                        currentValue = data[iter][keyName];
                    if(targetValue > currentValue){matches.push(data[iter])}
                }
                break;

                case logicalOperators.LessThan:
                    for(let iter = 0 ; iter<dataSize; iter++){
                        currentValue = data[iter][keyName];
                    if(targetValue < currentValue){matches.push(data[iter])}
                    }
                break;

                case logicalOperators.NotEqual:
                    for(let iter = 0 ; iter<dataSize; iter++){
                        currentValue = data[iter][keyName];
                    if(targetValue != currentValue){matches.push(data[iter])}
                    }
                break;

                default:
                    throw e.message("no operator found in parseOnCondition");
            }
        }
        catch(e){
            console.log(e);
        }
        return matches;
    }
    statisticsOnKey(data, idKeyName, idValue, targetKeyName){
        var results = [];
        var min = 10000;
        var max = 0;
        var average = 0.0;
        var sum = 0.0;
        var count = 0;
        var isNumeric = true;
        try{
            var dataSize = (data).length;
        }
        catch(e){
            throw new Error("unable to parse data in sumOnKey")
        }


        var currentValue = data[0][targetKeyName];
        if(isNaN(currentValue)){isNumeric = false}

        try{
            for(let iter = 0 ; iter<dataSize; iter++){
                let currentId = data[iter][idKeyName]
                currentValue = data[iter][targetKeyName];
                if(isNumeric){
                    if(idValue == currentId){
                        sum+=(currentValue);
                        count++;
                    }
                    if(currentValue > max){ max = currentValue;}                        
                    if(currentValue < min){ min = currentValue;}
                }
                else{
                    if(idValue == currentId){
                        count++;
                    }
                }
            }
        }  
        catch(e){
            console.log(e);
        }

        if(count == 0){return null;}
        average = sum/count;
        results = {"Count":count, "Sum":sum, "Average":average,"Min":min,"Max":max};
        return results;
    }
    // sumOnKey(data, targetKeyName, targetValue, sumKeyName){
    //     var sum = 0;
    //     try{
    //         var dataSize = (data).length;
    //     }
    //     catch(e){
    //         throw new Error("unable to parse data in sumOnKey")
    //     }
    //     try{
    //         let currentValue = 0;
    //         for(let iter = 0 ; iter<dataSize; iter++){
    //             currentValue = data[iter][targetKeyName];
    //                 if(targetValue == currentValue){sum+=(data[iter][sumKeyName])}
    //         }
    //     }
    //     catch(e){
    //         console.log(e);
    //     }
    //     if(sum == 0){
    //         return null;
    //     }
    //     return sum;
    // }



    /**
     * Calculates the number of claims where the status is "Closed"
     *
     * @returns {number} number of closed claims
     */
    getNumClosedClaims() {
        var claimCount = 0;
        try{
            let claims = this.parseOnCondition(sfcc2023Claims, "status", logicalOperators.Equals,"Closed")
            claimCount = claims.length;
        }
        catch(e){
            console.log(e);
        }        
        
        return claimCount;
    }

    /**
     * Calculates the number of claims assigned to a specific claim handler.
     *
     * @param {number} claimHandlerId - ID of the claim handler.
     * @returns {number} - Number of claims assigned to the claim handler.
     */
    getNumClaimsForClaimHandlerId(claimHandlerId) {
        var claimCount = 0;
        try{
            let claims = this.parseOnCondition(sfcc2023Claims, "claim_handler_assigned_id", logicalOperators.Equals, claimHandlerId);
            claimCount = claims.length;
        }
        catch(e){
            console.log(e);
        }        
        
        return claimCount;
    }

    /**
     * Calculates the number of disasters for a specific state.
     *
     * @param {string} state - Name of a state in the United States of America, including the District of Columbia.
     * @returns {number} - Number of disasters for the state.
     */
    getNumDisastersForState(state) {
        var claimCount = 0;
        try{
            let claims = this.parseOnCondition(sfcc2023Disasters, "state", logicalOperators.Equals, state);
            claimCount = claims.length;
        }
        catch(e){
            console.log(e);
        }        
        
        return claimCount;
    }

    /**
     * Sums the estimated cost of a specific disaster by its claims.
     *
     * @param {number} disasterId - ID of disaster.
     * @returns {number|null} - Estimate cost of disaster, rounded to the nearest hundredths place,
     *                          or null if no claims are found.
     */
    getTotalClaimCostForDisaster(disasterId) {
        var costOfDisaster = 0;
        try{
            let stats = this.statisticsOnKey(sfcc2023Claims, "disaster_id",  disasterId, "estimate_cost");
            if(stats == null){
                return null;
            }
            else{
                costOfDisaster = +(stats.Sum).toFixed(2);
            }
        }
        catch(e){
            console.log(e);
        }

        return costOfDisaster;
    }

    /**
     * Gets the average estimated cost of all claims assigned to a claim handler.
     *
     * @param {number} claimHandlerId - ID of claim handler.
     * @returns {number|null} - Average cost of claims, rounded to the nearest hundredths place,
     *                          or null if no claims are found.
     */
    getAverageClaimCostForClaimHandler(claimHandlerId) {
        var claimCostAvg = 0;
        try{
            let stats = this.statisticsOnKey(sfcc2023Claims, "claim_handler_assigned_id",  claimHandlerId, "estimate_cost");
            if(stats == null){
                return null;
            }
            else{
                claimCostAvg = +(stats.Average).toFixed(2);
            }
        }
        catch(e){
            console.log(e);        
        }
        
        
        return claimCostAvg;
    }

    /**
     * Returns the name of the state with the most disasters based on disaster data.
     * If two states have the same number of disasters, then sorts by alphabetical (a-z)
     * and takes the first.
     *
     * @returns {string} - Single name of state
     */
    getStateWithMostDisasters() {
        var numDisasters = 0;
        var stateName = null;
        try{
            for (let iter = 0; iter < stateList.length; iter++) {
                let stats = this.statisticsOnKey(sfcc2023Disasters, "state",  stateList[iter], "id");
                if(stats){
                    if(stats.Count > numDisasters){ 
                        stateName = stateList[iter];
                        numDisasters = stats.Count;
                    }
                }
            }
        }
        catch(e){
            throw e;
            console.log(e);
        }

        return stateName;
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
        var numDisasters = 100;
        var stateName = null;
        try{
            for (let iter = 0; iter < stateList.length; iter++) {
                let stats = this.statisticsOnKey(sfcc2023Disasters, "state",  stateList[iter], "id");
                if(stats){
                    if(stats.Count < numDisasters){ 
                        stateName = stateList[iter];
                        numDisasters = stats.Count;
                    }
                }
            }
        }
        catch(e){
            console.log(e);
        }

        return stateName;
    }

    /**
     * Returns the name of the most spoken language by agents (besides English) for a specific state.
     *
     * @param {string} state - Name of state.
     * @returns {string} - Name of language, or empty string if state doesn't exist.
     */
    getMostSpokenAgentLanguageByState(state) {
        var speackerCount = 0;
        var stateName = null;
        try{
            for (let iter = 0; iter < stateList.length; iter++) {

            }
        }
        catch(e){
            throw e;
            console.log(e);
        }
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
        var claimCount = 0;
        var severity = null;
        try{

        }
        catch(err){
            throw err.message("error in calculateDisasterClaimDensity")
        }
        return null;
    }

    /**
     * Gets the number of disasters where it was declared after it ended.
     *
     * @returns {number} - Number of disasters where the declared date is after the end date.
     */
    getNumDisastersDeclaredAfterEndDate() {
        var disasterCount = 0;
        try{

        }
        catch(err){
            throw err.message("error in calculateDisasterClaimDensity")
        }
        return disasterCount;
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
        var agentToClaimMap = [];
        try{

        }
        catch(err){
            throw err.message("error in calculateDisasterClaimDensity")
        }
        return agentToClaimMap;
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
        var disasterClaimDensity = 0;
        try{

        }
        catch(err){
            throw err.message("error in calculateDisasterClaimDensity")
        }

        return -1;
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
        var topThreeMonths = [];
        try{

        }
        catch(err){
            throw err.message("error in getTopThreeMonthsWithHighestNumOfClaimsDesc")
        }

        return topThreeMonths;
    }
}

