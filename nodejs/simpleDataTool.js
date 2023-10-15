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
        return -1;
    }

    /**
     * Calculates the number of claims assigned to a specific claim handler.
     *
     * @param {number} claimHandlerId - ID of the claim handler.
     * @returns {number} - Number of claims assigned to the claim handler.
     */
    getNumClaimsForClaimHandlerId(claimHandlerId) {
        return null;
    }

    /**
     * Calculates the number of disasters for a specific state.
     *
     * @param {string} state - Name of a state in the United States of America, including the District of Columbia.
     * @returns {number} - Number of disasters for the state.
     */
    getNumDisastersForState(state) {
        return null;
    }

    /**
     * Sums the estimated cost of a specific disaster by its claims.
     *
     * @param {number} disasterId - ID of disaster.
     * @returns {number|null} - Estimate cost of disaster, rounded to the nearest hundredths place,
     *                          or null if no claims are found.
     */
    getTotalClaimCostForDisaster(disasterId) {
        return -1;
    }

    /**
     * Gets the average estimated cost of all claims assigned to a claim handler.
     *
     * @param {number} claimHandlerId - ID of claim handler.
     * @returns {number|null} - Average cost of claims, rounded to the nearest hundredths place,
     *                          or null if no claims are found.
     */
    getAverageClaimCostForClaimHandler(claimHandlerId) {
        return -1;
    }

    /**
     * Returns the name of the state with the most disasters based on disaster data.
     * If two states have the same number of disasters, then sorts by alphabetical (a-z)
     * and takes the first.
     *
     * @returns {string} - Single name of state
     */
    getStateWithMostDisasters() {
        return null;
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
        return null;
    }

    /**
     * Returns the name of the most spoken language by agents (besides English) for a specific state.
     *
     * @param {string} state - Name of state.
     * @returns {string} - Name of language, or empty string if state doesn't exist.
     */
    getMostSpokenAgentLanguageByState(state) {
        return null;
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
        return -2;
    }

    /**
     * Gets the number of disasters where it was declared after it ended.
     *
     * @returns {number} - Number of disasters where the declared date is after the end date.
     */
    getNumDisastersDeclaredAfterEndDate() {
        return null;
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
        return null;
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
        return null;
    }
}

module.exports = SimpleDataTool;