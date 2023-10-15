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
    return sfcc2023Claims.filter((claim) => claim.status === "Closed").length;
  }

  /**
   * Calculates the number of claims assigned to a specific claim handler.
   *
   * @param {number} claimHandlerId - ID of the claim handler.
   * @returns {number} - Number of claims assigned to the claim handler.
   */
  getNumClaimsForClaimHandlerId(claimHandlerId) {
    return sfcc2023Claims.filter(
      (a) => a.claim_handler_assigned_id == claimHandlerId
    ).length;
  }

  /**
   * Calculates the number of disasters for a specific state.
   *
   * @param {string} state - Name of a state in the United States of America, including the District of Columbia.
   * @returns {number} - Number of disasters for the state.
   */
  getNumDisastersForState(state) {
    const disastersForState = sfcc2023Disasters.filter(
      (disaster) => disaster.state === state
    );
    return disastersForState.length;
  }

  /**
   * Sums the estimated cost of a specific disaster by its claims.
   *
   * @param {number} disasterId - ID of disaster.
   * @returns {number|null} - Estimate cost of disaster, rounded to the nearest hundredths place,
   *                          or null if no claims are found.
   */
  getTotalClaimCostForDisaster(disasterId) {
    const claims = sfcc2023Claims.filter((a) => a.disaster_id == disasterId);
    if (claims.length == 0) return null;
    const estimatedCosts = claims
      .map((a) => a.estimate_cost)
      .reduce((a, b) => a + b);
    return parseFloat(estimatedCosts.toFixed(2));
  }

  /**
   * Gets the average estimated cost of all claims assigned to a claim handler.
   *
   * @param {number} claimHandlerId - ID of claim handler.
   * @returns {number|null} - Average cost of claims, rounded to the nearest hundredths place,
   *                          or null if no claims are found.
   */
  getAverageClaimCostForClaimHandler(claimHandlerId) {
    const claims = sfcc2023Claims.filter(
      (a) => a.claim_handler_assigned_id == claimHandlerId
    );
    if (claims.length == 0) return null;
    const totalCosts = claims
      .map((claim) => claim.estimate_cost)
      .reduce((a, b) => a + b);

    const average = totalCosts / claims.length;
    return parseFloat(average.toFixed(2));
  }

  /**
   * Returns the name of the state with the most disasters based on disaster data.
   * If two states have the same number of disasters, then sorts by alphabetical (a-z)
   * and takes the first.
   *
   * @returns {string} - Single name of state
   */
  getStateWithMostDisasters() {
    const stateAmounts = {};
    for (const disaster of sfcc2023Disasters) {
      if (!stateAmounts[disaster.state]) stateAmounts[disaster.state] = 0;
      stateAmounts[disaster.state]++;
    }

    let sortableAmounts = [];
    for (const state in stateAmounts) {
      sortableAmounts.push([state, stateAmounts[state]]);
    }

    sortableAmounts.sort(function (a, b) {
      if (a[1] === b[1]) {
        return a[0].localeCompare(b[0]); // compare names to sort them alphabetically
      } else {
        return b[1] - a[1];
      }
    });

    return sortableAmounts[0][0];
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
    const stateAmounts = {};
    for (const disaster of sfcc2023Disasters) {
      if (!stateAmounts[disaster.state]) stateAmounts[disaster.state] = 0;
      stateAmounts[disaster.state]++;
    }

    let sortableAmounts = [];
    for (const state in stateAmounts) {
      sortableAmounts.push([state, stateAmounts[state]]);
    }

    sortableAmounts.sort(function (a, b) {
      if (a[1] === b[1]) {
        return a[0].localeCompare(b[0]);
      } else {
        return a[1] - b[1];
      }
    });

    return sortableAmounts[0][0];
  }

  /**
   * Returns the name of the most spoken language by agents (besides English) for a specific state.
   *
   * @param {string} state - Name of state.
   * @returns {string} - Name of language, or empty string if state doesn't exist.
   */
  getMostSpokenAgentLanguageByState(state) {
    const agents = sfcc2023Agents.filter((agent) => agent.state == state);
    if (agents.length == 0) return "";
    const languageAmounts = {};
    for (const agent of agents) {
      const language =
        agent.primary_language == "English"
          ? agent.secondary_language
          : agent.primary_language;
      languageAmounts[language] = languageAmounts[language]
        ? languageAmounts[language] + 1
        : 1;
    }

    const languageCountArray = Object.entries(languageAmounts);
    languageCountArray.sort((a, b) => b[1] - a[1]);

    return languageCountArray[0][0];
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
    const MIN_SEVERITY = 1;
    const MAX_SEVERITY = 10;
    if (minSeverityRating < MIN_SEVERITY || minSeverityRating > MAX_SEVERITY)
      return -1;
    if (!sfcc2023Agents.find((agent) => agent.id === agentId)) return null;

    const claims = sfcc2023Claims.filter(
      (claim) => claim.agent_assigned_id === agentId
    );
    if (claims.length === 0) return null;

    return claims.filter(
      (claim) =>
        claim.severity_rating >= minSeverityRating && claim.status !== "Closed"
    ).length;
  }

  /**
   * Gets the number of disasters where it was declared after it ended.
   *
   * @returns {number} - Number of disasters where the declared date is after the end date.
   */
  getNumDisastersDeclaredAfterEndDate() {
    return sfcc2023Disasters.filter((a) => a.end_date < a.declared_date).length;
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
    const agentsCosts = {};
    for (const claim of sfcc2023Claims) {
      agentsCosts[claim.agent_assigned_id] = agentsCosts[
        claim.agent_assigned_id
      ]
        ? agentsCosts[claim.agent_assigned_id] + claim.estimate_cost
        : claim.estimate_cost;
    }
    for (const agent of sfcc2023Agents) {
      if (!agentsCosts[agent.id]) agentsCosts[agent.id] = 0;
    }
    for (const cost of Object.keys(agentsCosts)) {
      agentsCosts[cost] = parseFloat(agentsCosts[cost].toFixed(2));
    }
    return agentsCosts;
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
    const disaster = sfcc2023Disasters.find(
      (disaster) => disaster.id === disasterId
    );
    if (!disaster) return null;

    const claims = sfcc2023Claims.filter(
      (claim) => claim.disaster_id === disasterId
    );
    const radius = disaster.radius_miles;
    const claimCount = claims.length;
    const area = Math.PI * Math.pow(radius, 2);

    if (area === 0) return 0;
    const density = claimCount / area;

    return parseFloat(density.toFixed(5));
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
    const monthYearClaimCost = {};

    // Loop through the claims to calculate the total claim cost for each month and year
    for (const claim of sfcc2023Claims) {
      const disaster = sfcc2023Disasters.find(
        (d) => d.id === claim.disaster_id
      );

      const declaredDate = new Date(disaster.declared_date);
      const month = declaredDate.toLocaleString("default", { month: "long" }); // Get the string representation of the month
      const year = declaredDate.getFullYear();
      const monthYear = `${month} ${year}`;

      monthYearClaimCost[monthYear] = monthYearClaimCost[monthYear]
        ? monthYearClaimCost[monthYear] + claim.estimate_cost
        : claim.estimate_cost;
    }

    // Sort the months by total claim cost in descending order
    const sortedMonths = Object.entries(monthYearClaimCost).sort(
      (a, b) => b[1] - a[1]
    );

    // Get the top three months
    const topThreeMonths = sortedMonths
      .slice(0, 3)
      .map((monthCost) => monthCost[0]);

    return topThreeMonths;
  }
}

module.exports = SimpleDataTool;
