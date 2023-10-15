const SimpleDataTool = require("./simpleDataTool");

let controller;

beforeAll(() => {
    controller = new SimpleDataTool();
});

describe("Test Set One", () => {
    test("Test 1 - getNumClosedClaims", () => {
        const actualNumClosedClaims = controller.getNumClosedClaims();
        expect(actualNumClosedClaims).toBe(362);
    });

    test("Test 2 - getNumClaimsForClaimHandlerId", () => {
        expect(controller.getNumClaimsForClaimHandlerId(1)).toBe(9);
        expect(controller.getNumClaimsForClaimHandlerId(93)).toBe(4);
        expect(controller.getNumClaimsForClaimHandlerId(127)).toBe(6);
    });

    test("Test 3 - getNumDisastersForState", () => {
        expect(controller.getNumDisastersForState("Arizona")).toBe(2);
        expect(controller.getNumDisastersForState("Georgia")).toBe(5);
        expect(controller.getNumDisastersForState("Illinois")).toBe(2);
        expect(controller.getNumDisastersForState("Texas")).toBe(9);
        expect(controller.getNumDisastersForState("District of Columbia")).toBe(2);
    });
});

describe("Test Set Two", () => {
    test("Test 4 - getTotalClaimCostForDisaster", () => {
        expect(controller.getTotalClaimCostForDisaster(5)).toBe(377726.38);
        expect(controller.getTotalClaimCostForDisaster(0)).toBe(null);
        expect(controller.getTotalClaimCostForDisaster(56)).toBe(1287476.19);
        expect(controller.getTotalClaimCostForDisaster(101)).toBe(null);
        expect(controller.getTotalClaimCostForDisaster(78)).toBe(614822.68);
    });

    test("Test 5 - getAverageClaimCostForClaimHandler", () => {
        expect(controller.getAverageClaimCostForClaimHandler(2)).toBe(87330.89);
        expect(
            Math.round(controller.getAverageClaimCostForClaimHandler(42) * 100) / 100
        ).toBe(122195.9);
        expect(controller.getAverageClaimCostForClaimHandler(-5)).toBe(null);
        expect(controller.getAverageClaimCostForClaimHandler(225)).toBe(null);
        expect(
            Math.round(controller.getAverageClaimCostForClaimHandler(151) * 100) / 100
        ).toBe(242134.96);
    });

    test("Test 6 - getStateWithMostAndLeastDisasters", () => {
        expect(controller.getStateWithMostDisasters()).toBe("California");
        expect(controller.getStateWithLeastDisasters()).toBe("Alaska");
    });

    test("Test 7 - getMostSpokenAgentLanguageByState", () => {
        expect(controller.getMostSpokenAgentLanguageByState("New Hampshire")).toBe(
            "Arabic"
        );
        expect(controller.getMostSpokenAgentLanguageByState("Wisconsin")).toBe("");
        expect(controller.getMostSpokenAgentLanguageByState("Florida")).toBe(
            "Spanish"
        );
    });

    test("Test 8 - getNumOfOpenClaimsForAgentAndSeverity", () => {
        expect(controller.getNumOfOpenClaimsForAgentAndSeverity(0, 0)).toBe(-1);
        expect(controller.getNumOfOpenClaimsForAgentAndSeverity(25, 11)).toBe(-1);
        expect(controller.getNumOfOpenClaimsForAgentAndSeverity(65, 3)).toBe(null);
        expect(controller.getNumOfOpenClaimsForAgentAndSeverity(24, 1)).toBe(16);
        expect(controller.getNumOfOpenClaimsForAgentAndSeverity(87, 6)).toBe(3);
        expect(controller.getNumOfOpenClaimsForAgentAndSeverity(85, 6)).toBe(2);
    });
});

describe("Test Set Three", () => {
    test("Test 9 - getNumDisastersDeclaredAfterEndDate", () => {
        expect(controller.getNumDisastersDeclaredAfterEndDate()).toBe(8);
    });

    test("Test 10 - buildMapOfAgentsToTotalClaimCost", () => {
        const agentCostMap = controller.buildMapOfAgentsToTotalClaimCost();
        expect(Object.keys(agentCostMap).length).toBe(100);

        // Normal cases
        expect(agentCostMap[1]).toBe(27856.13);
        expect(agentCostMap[3]).toBe(2253847.27);
        expect(agentCostMap[5]).toBe(529685.97);
        expect(agentCostMap[8]).toBe(282307.93);
        expect(agentCostMap[13]).toBe(2310862.86);

        // Spot-check random agent ids that we expect to have no cost
        const expectedAgentIdsWithoutCost = [
            2, 6, 9, 12, 16, 22, 25, 32, 33, 37, 38, 40, 41, 44, 45, 48, 50, 51, 52,
            53, 54, 61, 64, 65, 67, 69, 72, 81, 90, 93, 96,
        ];

        for (let i = 0; i < 3; i++) {
            const randomIndex = Math.floor(
                Math.random() * expectedAgentIdsWithoutCost.length
            );
            const randomAgentId = expectedAgentIdsWithoutCost[randomIndex];
            expect(agentCostMap[randomAgentId]).toBe(0);
        }

        // Testing invalid agent ids
        expect(agentCostMap[-5]).toBe(undefined);
        expect(agentCostMap[255]).toBe(undefined);
    });

    test("Test 11 - calculateDisasterClaimDensity", () => {
        expect(controller.calculateDisasterClaimDensity(15)).toBe(0.00172);
        expect(controller.calculateDisasterClaimDensity(68)).toBe(0.00029);
        expect(controller.calculateDisasterClaimDensity(101)).toBe(null);
        expect(controller.calculateDisasterClaimDensity(64)).toBe(0.01624);
    });
});

describe("Test Set Four", () => {
    test("Test 12 - getTopThreeMonthsWithHighestNumOfClaimsDesc", () => {
        const topThreeMonths =
            controller.getTopThreeMonthsWithHighestNumOfClaimsDesc();
        expect(topThreeMonths.length).toBe(3);
        expect(topThreeMonths[0]).toBe("April 2023");
        expect(topThreeMonths[1]).toBe("November 2022");
        expect(topThreeMonths[2]).toBe("February 2023");
    });
});
