package com.statefarm.codingcompetition.simpledatatool;

import static org.junit.Assert.assertEquals;

import org.junit.Before;
import org.junit.Test;

import com.statefarm.codingcompetition.simpledatatool.controller.SimpleDataTool;

public class TestSet2 {

    private static SimpleDataTool controller;

    @Before
    public void initialize() {
        controller = new SimpleDataTool();
    }

    @Test
    public void test4_getTotalClaimCostForDisaster() {
        assertEquals(377726.38, controller.getTotalClaimCostForDisaster(5), 0.01);
        assertEquals(null, controller.getTotalClaimCostForDisaster(0));
        assertEquals(1287476.19, controller.getTotalClaimCostForDisaster(56), 0.01);
        assertEquals(null, controller.getTotalClaimCostForDisaster(101));
        assertEquals(614822.68, controller.getTotalClaimCostForDisaster(78), 0.01);
    }

    @Test
    public void test5_getAverageClaimCostforClaimHandler() {
        assertEquals(87330.89, controller.getAverageClaimCostforClaimHandler(2), 0.01);
        assertEquals(122195.90, controller.getAverageClaimCostforClaimHandler(42), 0.01);
        assertEquals(null, controller.getAverageClaimCostforClaimHandler(-5));
        assertEquals(null, controller.getAverageClaimCostforClaimHandler(225));
        assertEquals(242134.96, controller.getAverageClaimCostforClaimHandler(151), 0.01);
    }

    @Test
    public void test6_getStateWithMostAndLeastDisasters() {
        assertEquals("California", controller.getStateWithTheMostDisasters());
        assertEquals("Alaska", controller.getStateWithTheLeastDisasters());
    }

    @Test
    public void test7_getMostSpokenAgentLanguageByState() {
        assertEquals("Arabic", controller.getMostSpokenAgentLanguageByState("New Hampshire"));
        assertEquals("", controller.getMostSpokenAgentLanguageByState("Wisconsin"));
        assertEquals("Spanish", controller.getMostSpokenAgentLanguageByState("Florida"));
    }

    @Test
    public void test8_getNumOfOpenClaimsForAgentAndSeverity() {
        assertEquals(Integer.valueOf(-1), controller.getNumOfOpenClaimsForAgentAndSeverity(0, 0));
        assertEquals(Integer.valueOf(-1), controller.getNumOfOpenClaimsForAgentAndSeverity(25, 11));
        assertEquals(null, controller.getNumOfOpenClaimsForAgentAndSeverity(65, 3));
        assertEquals(Integer.valueOf(16), controller.getNumOfOpenClaimsForAgentAndSeverity(24, 1));
        assertEquals(Integer.valueOf(3), controller.getNumOfOpenClaimsForAgentAndSeverity(87, 6));
        assertEquals(Integer.valueOf(2), controller.getNumOfOpenClaimsForAgentAndSeverity(85, 6));
    }
}