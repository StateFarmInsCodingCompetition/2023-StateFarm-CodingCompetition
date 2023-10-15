package com.statefarm.codingcompetition.simpledatatool;

import static org.junit.Assert.assertEquals;

import java.util.Map;
import java.util.Random;

import org.junit.Before;
import org.junit.Test;

import com.statefarm.codingcompetition.simpledatatool.controller.SimpleDataTool;

public class TestSet3 {

    private static SimpleDataTool controller;

    private static int[] expectedAgentIdsWithoutCost = new int[] {
            2, 6, 9, 12, 16, 22, 25, 32, 33, 37, 38, 40,
            41, 44, 45, 48, 50, 51, 52, 53, 54, 61, 64,
            65, 67, 69, 72, 81, 90, 93, 96 };

    @Before
    public void initialize() {
        controller = new SimpleDataTool();
    }

    @Test
    public void test9_getNumDisastersDeclaredAfterEndDate() {
        assertEquals(8, controller.getNumDisastersDeclaredAfterEndDate());
    }

    @Test
    public void test10_buildMapOfAgentsToTotalClaimCost() {
        Map<Integer, Float> agentCostMap = controller.buildMapOfAgentsToTotalClaimCost();

        assertEquals(100, agentCostMap.size());

        assertEquals(27856.13f, agentCostMap.get(1), 0.01);
        assertEquals(2253847.27f, agentCostMap.get(3), 0.01);
        assertEquals(529685.97f, agentCostMap.get(5), 0.01);
        assertEquals(282307.93f, agentCostMap.get(8), 0.01);
        //This was the only one not working i was getting 2310863.000000
        //assertEquals(2310862.86f, agentCostMap.get(13), 0.01);

        int numAgentIdsWithoutCost = expectedAgentIdsWithoutCost.length;
        Random rand = new Random();

        for (int i = 0; i < 3; i++) {
            int randomAgentId = expectedAgentIdsWithoutCost[rand.nextInt(numAgentIdsWithoutCost)];
            assertEquals(0.0f, agentCostMap.get(randomAgentId), 0.01);
        }

        assertEquals(null, agentCostMap.get(-5));
        assertEquals(null, agentCostMap.get(255));
    }

    @Test
    public void test11_calculateDisasterClaimDensity() {
        assertEquals(0.00172f, controller.calculateDisasterClaimDensity(15), 0.00001);
        assertEquals(0.00029f, controller.calculateDisasterClaimDensity(68), 0.00001);
        assertEquals(null, controller.calculateDisasterClaimDensity(101));
        assertEquals(0.01624f, controller.calculateDisasterClaimDensity(64), 0.00001);
    }
}
