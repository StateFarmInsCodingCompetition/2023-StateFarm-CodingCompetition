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
            south: "Oklahoma,Texas,Arkansas,Louisiana,Kentucky,Tennessee,Mississippi,Alabama,West Virginia,Virginia,North Carolina,South Carolina,Georgia,Florida",
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
        return sfcc2023Claims.filter((claim) => claim.status == "Closed")
            .length;
    }

    /**
     * Calculates the number of claims assigned to a specific claim handler.
     *
     * @param {number} claimHandlerId - ID of the claim handler.
     * @returns {number} - Number of claims assigned to the claim handler.
     */
    getNumClaimsForClaimHandlerId(claimHandlerId) {
        return sfcc2023Claims.filter(
            (claim) => claim.claim_handler_assigned_id == claimHandlerId
        ).length;
    }

    /**
     * Calculates the number of disasters for a specific state.
     *
     * @param {string} state - Name of a state in the United States of America, including the District of Columbia.
     * @returns {number} - Number of disasters for the state.
     */
    getNumDisastersForState(state) {
        return sfcc2023Disasters.filter((disaster) => disaster.state == state)
            .length;
    }

    /**
     * Sums the estimated cost of a specific disaster by its claims.
     *
     * @param {number} disasterId - ID of disaster.
     * @returns {number|null} - Estimate cost of disaster, rounded to the nearest hundredths place,
     *                          or null if no claims are found.
     */
    getTotalClaimCostForDisaster(disasterId) {
        // Filter claims for this disaster
        const claimsForDisaster = sfcc2023Claims.filter(
            (claim) => claim.disaster_id == disasterId
        );

        if (claimsForDisaster.length == 0) {
            // No claims are found
            return null;
        } else {
            return this.#getTotalCostOfClaims(claimsForDisaster);
        }
    }

    /**
     * Gets the average estimated cost of all claims assigned to a claim handler.
     *
     * @param {number} claimHandlerId - ID of claim handler.
     * @returns {number|null} - Average cost of claims, rounded to the nearest hundredths place,
     *                          or null if no claims are found.
     */
    getAverageClaimCostForClaimHandler(claimHandlerId) {
        // Filter claims for this claim handler
        const claimsForClaimHandler = sfcc2023Claims.filter(
            (claim) => claim.claim_handler_assigned_id == claimHandlerId
        );

        if (claimsForClaimHandler.length == 0) {
            // No claims are found
            return null;
        } else {
            const totalCost = this.#getTotalCostOfClaims(claimsForClaimHandler);
            // Average = total / length
            const average = totalCost / claimsForClaimHandler.length;
            // Return the average round to 2 decimal places
            return Math.round(average * 100) / 100;
        }
    }

    /**
     * Returns the name of the state with the most disasters based on disaster data.
     * If two states have the same number of disasters, then sorts by alphabetical (a-z)
     * and takes the first.
     *
     * @returns {string} - Single name of state
     */
    getStateWithMostDisasters() {
        const statesListSortedByDisasters =
            this.#getSortStatesByDisasterCount(false);
        // The array of states is sort decreasing by
        // number of disasters, thus we just need to return the first state.
        return statesListSortedByDisasters[0];
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
        const statesListSortedByDisasters =
            this.#getSortStatesByDisasterCount();
        // The array of states is sort increasing by
        // number of disasters, thus we just need to return the first state.
        return statesListSortedByDisasters[0];
    }

    /**
     * Returns the name of the most spoken language by agents (besides English) for a specific state.
     *
     * @param {string} state - Name of state.
     * @returns {string} - Name of language, or empty string if state doesn't exist.
     */
    getMostSpokenAgentLanguageByState(state) {
        // Map from a language to number of agents that speaks that language.
        const languageMap = new Map();
        // List of agents of the given state.
        const agentsOfState = sfcc2023Agents.filter(
            (agent) => agent.state == state
        );
        agentsOfState.forEach((agent) => {
            // Update the language map
            this.#increaseValueForMap(languageMap, agent.primary_language);
            this.#increaseValueForMap(languageMap, agent.secondary_language);
        });

        // Sort languages descreasing by number of agents that speaks that language.
        const sortedSpokenLanguages = this.#sortMapByValue(languageMap, false);
        if (sortedSpokenLanguages.length == 0) {
            return "";
        } else {
            // If the most spoken language is English
            // then return the second-most spoken language.
            return sortedSpokenLanguages[0] == "English"
                ? sortedSpokenLanguages[1]
                : sortedSpokenLanguages[0];
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
        if (minSeverityRating < 1 || minSeverityRating > 10) {
            // Severity out of bounds.
            return -1;
        }

        const claimsForAgentAndSeverity = sfcc2023Claims.filter((claim) => {
            return (
                claim.status != "Closed" &&
                claim.agent_assigned_id == agentId &&
                claim.severity_rating >= minSeverityRating
            );
        });

        if (claimsForAgentAndSeverity.length == 0) {
            // Agent does not exist/agent has no claims
            return null;
        } else {
            return claimsForAgentAndSeverity.length;
        }
    }

    /**
     * Gets the number of disasters where it was declared after it ended.
     *
     * @returns {number} - Number of disasters where the declared date is after the end date.
     */
    getNumDisastersDeclaredAfterEndDate() {
        return sfcc2023Disasters.filter(
            (disaster) => disaster.declared_date > disaster.end_date
        ).length;
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
        const agentsToTotalCost = {};

        sfcc2023Agents.forEach((agent) => (agentsToTotalCost[agent.id] = 0));

        sfcc2023Claims.forEach((claim) => {
            const agentId = claim.agent_assigned_id;

            agentsToTotalCost[agentId] += claim.estimate_cost;
            agentsToTotalCost[agentId] =
                Math.round(agentsToTotalCost[agentId] * 100) / 100;
        });

        return agentsToTotalCost;
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
        const givenDisaster = sfcc2023Disasters.find(
            (disaster) => disaster.id == disasterId
        );
        if (!givenDisaster) {
            // Disaster does not exist.
            return null;
        }
        // Find the area of the disaster.
        const area =
            Math.PI * givenDisaster.radius_miles * givenDisaster.radius_miles;
        // Number of claims of the given disaster.
        const numClaims = sfcc2023Claims.filter(
            (claim) => claim.disaster_id == disasterId
        ).length;

        // Return density rounded by 5 decimal places.
        return Math.round((numClaims / area) * 100000) / 100000;
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
        // Map from months to number of claims.
        const monthsToClaims = new Map();

        sfcc2023Disasters.forEach((disaster) => {
            const declaredMonth = this.#convertToMonth(disaster.declared_date);
           
            // Get number of claims of this disaster.
            // const numClaims = sfcc2023Claims.filter((claim) => claim.disaster_id == disaster.id);
            const numClaims = 1;
            this.#increaseValueForMap(monthsToClaims, declaredMonth, numClaims);
        });

        const sortedList = this.#sortMapByValue(monthsToClaims, false);
        console.log(sortedList);
        return sortedList.slice(0, 3);
    }

    /**
     * Returns the total cost of a array of claims.
     *
     * @param {Array} claims - The array of claims to calculate the total cost.
     * @returns {double} - The total cost.
     */
    #getTotalCostOfClaims(claims) {
        let totalCost = 0;
        claims.forEach((claim) => (totalCost += claim.estimate_cost));
        return totalCost;
    }

    /**
     * Returns an array of states sorted by number of disaters.
     *
     * @param {boolean} increasing - True if sort increasingly. Otherwise, sort decreasingly.
     * @returns {Array} - States sorted by number of disaters.
     */
    #getSortStatesByDisasterCount(increasing = true) {
        // Map from state to the number of disaster at that state.
        const stateToNumDisaster = new Map();

        sfcc2023Disasters.forEach((disaster) => {
            this.#increaseValueForMap(stateToNumDisaster, disaster.state);
        });

        return this.#sortMapByValue(stateToNumDisaster, increasing);
    }

    /**
     * Safely updates a map by adding val to m[key].
     *
     * @param {Map} m - The map to update.
     * @param {string} key - The key where value needs to be updated.
     * @param {int} val - The val to add to current value.
     */
    #increaseValueForMap(m, key, val = 1) {
        if (!m.has(key)) {
            m.set(key, val);
        } else {
            m.set(key, m.get(key) + val);
        }
    }

    /**
     * Returns an array of keys sorted by its value.
     * If two keys have the same value, then sorts by alphabetical (a-z)
     * and takes the first.
     *
     * @param {Map} m - The map to sort.
     * @param {boolean} increasing - True if sort increasingly.
     */
    #sortMapByValue(m, increasing = true) {
        const sortedList = [...m.entries()].sort((a, b) => {
            if (
                (!increasing && a[1] > b[1]) ||
                (increasing && a[1] < b[1]) ||
                (a[1] == b[1] && a[0] < b[0])
            ) {
                return -1;
            } else {
                return 1;
            }
        });
        // Only returns the array of keys.
        return sortedList.map((entry) => entry[0]);
    }

    /**
     * Return the date in "month YYYY" format.
     * 
     * @param {*} dateStr - The date to convert
     * @returns The month extracts from the given date.
     */
    #convertToMonth(dateStr) {
        const monthNames = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ];
        const date = new Date(dateStr);

        return monthNames[date.getMonth()] + " " + date.getFullYear();
    }
}

module.exports = SimpleDataTool;
