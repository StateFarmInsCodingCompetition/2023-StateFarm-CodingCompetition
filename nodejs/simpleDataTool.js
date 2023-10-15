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
        let numClosedClaims = sfcc2023Claims.filter(claim => claim.status === 'Closed').length;
        return numClosedClaims;
    }

    /**
     * Calculates the number of claims assigned to a specific claim handler.
     *
     * @param {number} claimHandlerId - ID of the claim handler.
     * @returns {number} - Number of claims assigned to the claim handler.
     */
    getNumClaimsForClaimHandlerId(claimHandlerId) {
        return sfcc2023Claims.filter(claim => claim.claim_handler_assigned_id === claimHandlerId).length;
    }

    /**
     * Calculates the number of disasters for a specific state.
     *
     * @param {string} state - Name of a state in the United States of America, including the District of Columbia.
     * @returns {number} - Number of disasters for the state.
     */
    getNumDisastersForState(state) {
        return sfcc2023Disasters.filter(disaster => disaster.state === state).length;
    }

    /**
     * Sums the estimated cost of a specific disaster by its claims.
     *
     * @param {number} disasterId - ID of disaster.
     * @returns {number|null} - Estimate cost of disaster, rounded to the nearest hundredths place,
     *                          or null if no claims are found.
     */
    getTotalClaimCostForDisaster(disasterId) {
        let claimsLinkedToDisaster = sfcc2023Claims.filter(claim => claim.disaster_id === disasterId);
        if (claimsLinkedToDisaster.length > 0) {
            let disasterCostSum = 0;
            claimsLinkedToDisaster.forEach(claim => {
                disasterCostSum = disasterCostSum + claim.estimate_cost;
            })
            return disasterCostSum;
        }
        return null;
    }

    /**
     * Gets the average estimated cost of all claims assigned to a claim handler.
     *
     * @param {number} claimHandlerId - ID of claim handler.
     * @returns {number|null} - Average cost of claims, rounded to the nearest hundredths place,
     *                          or null if no claims are found.
     */
    getAverageClaimCostForClaimHandler(claimHandlerId) {
        let claimsLinkedToClaimHandler = sfcc2023Claims.filter(claim => claim.claim_handler_assigned_id === claimHandlerId);
        if (claimsLinkedToClaimHandler.length > 0) {
            let averageCost = 0;
            claimsLinkedToClaimHandler.forEach(claim => {
                averageCost = averageCost + claim.estimate_cost;
            })
            averageCost = averageCost / claimsLinkedToClaimHandler.length;
            return Math.round(averageCost * 100) / 100;
        }
        return null;
    }

    /**
     * Returns the name of the state with the most disasters based on disaster data.
     * If two states have the same number of disasters, then sorts by alphabetical (a-z)
     * and takes the first.
     *
     * @returns {string} - Single name of state
     */
    getStateWithMostDisasters() {
        let stateDisasterCount = {};
        sfcc2023Disasters.forEach(disaster => {
            stateDisasterCount[disaster.state] = (stateDisasterCount[disaster.state] || 0) + 1;
        })

        let maxState = null;
        let maxCount = 0;

        for (const state in stateDisasterCount) {
            if (stateDisasterCount[state] > maxCount || (stateDisasterCount[state] === maxCount && state < maxState)) {
                maxState = state;
                maxCount = stateDisasterCount[state];
            }
        }

        return maxState;
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
        let stateDisasterCount = {};
        sfcc2023Disasters.forEach(disaster => {
            stateDisasterCount[disaster.state] = (stateDisasterCount[disaster.state] || 0) + 1;
        })
        
        let leastState = null;
        // High number
        let leastCount = 1000;

        for (const state in stateDisasterCount) {
            if (stateDisasterCount[state] < leastCount || (stateDisasterCount[state] === leastCount && state < leastState)) {
                leastState = state;
                leastCount = stateDisasterCount[state];
            }
        }

        return leastState;
    }

    /**
     * Returns the name of the most spoken language by agents (besides English) for a specific state.
     *
     * @param {string} state - Name of state.
     * @returns {string} - Name of language, or empty string if state doesn't exist.
     */
    getMostSpokenAgentLanguageByState(state) {

        const agentsInState = sfcc2023Agents.filter(agent => agent.state === state);
        if ( agentsInState.length > 0 ) {
            let languageCount = {};
    
            agentsInState.forEach(agent => {
                languageCount[agent.primary_language] = (languageCount[agent.primary_language] || 0) + 1;
                languageCount[agent.secondary_language] = (languageCount[agent.secondary_language] || 0) + 1;
            })
    
            let maxLanguage = null;
            let maxCount = 0;
    
            for (const language in languageCount) {
                if (languageCount[language] > maxCount && language !== "English") {
                    maxLanguage = language;
                    maxCount = languageCount[language];
                }
            }
    
            return maxLanguage;
        }

        return "";
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

        if (minSeverityRating < 1 || minSeverityRating > 10) {
            return -1
        }        

        const agentsOpenClaims = sfcc2023Claims.filter(claim => claim.agent_assigned_id === agentId && claim.status !== "Closed");

        if(agentsOpenClaims.length > 0) {
            const claimsWithinSeverityRating = agentsOpenClaims.filter(claim => claim.severity_rating >= minSeverityRating);
            if(claimsWithinSeverityRating.length > 0) {
                return claimsWithinSeverityRating.length;
            }
            return -1;
        }

        return null;
    }

    /**
     * Gets the number of disasters where it was declared after it ended.
     *
     * @returns {number} - Number of disasters where the declared date is after the end date.
     */
    getNumDisastersDeclaredAfterEndDate() {

        return sfcc2023Disasters.filter(disaster => disaster.end_date < disaster.declared_date).length;
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
        const agentClaimsCostMap = {};
        sfcc2023Agents.forEach(agent => {
            agentClaimsCostMap[agent.id] = 0;
        })
        sfcc2023Claims.forEach(claim => {
            agentClaimsCostMap[claim.agent_assigned_id] = Math.round((agentClaimsCostMap[claim.agent_assigned_id] + claim.estimate_cost) * 100) / 100 ;
        })
        return agentClaimsCostMap;
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
        const disaster = sfcc2023Disasters.find(disaster => disaster.id === disasterId);
        if (disaster) {
            const areaOfDisaster = Math.pow(disaster.radius_miles, 2) * Math.PI;
            const claimsLinkedToDisaster = sfcc2023Claims.filter(claim => claim.disaster_id === disasterId);
    
            return Math.round(claimsLinkedToDisaster.length / areaOfDisaster * 100000) / 100000;
        }
        return null;
    }

    /**
     * Gets the top three months with the highest total claim cost.
     * 
     * OPTIONAL! OPTIONAL! OPTIONAL!
     * AS OF 9:21 CDT, TEST IS OPTIONAL. SEE GITHUB ISSUE #8 FOR MORE DETAILS
     * 
     * Hint:
     *     Month should be full name like 01 is January and 12 is December.
     *     Year should be full four-digit year.
     *     List should be in descending order.
     *
     * @returns {Array} - An array of three strings of month and year, descending order of highest claims.
     */
    getTopThreeMonthsWithHighestNumOfClaimsDesc() {

        const monthAndYearMap = {}

        
        const getDisasterMonthAndYear = (disasterDate) => {
            let declaredDate = new Date(disasterDate);
            return declaredDate.toLocaleString('default', { month: 'long' }) + " " + declaredDate.getFullYear();
        }

        sfcc2023Claims.forEach(claim => {
            let disaster = sfcc2023Disasters.find( disaster => disaster.id === claim.disaster_id);

            const monthAndYear = getDisasterMonthAndYear(disaster.declared_date);

            monthAndYearMap[monthAndYear] = (monthAndYearMap[monthAndYear] || 0) + claim.estimate_cost;
        })

        const monthAndYearArray = Object.entries(monthAndYearMap);

        monthAndYearArray.sort((a, b) => b[1] - a[1]);

        const top3MonthsWithHighestClaimCost = monthAndYearArray.slice(0, 3).map(entry => entry[0]);

        return top3MonthsWithHighestClaimCost;
    }
}

module.exports = SimpleDataTool;