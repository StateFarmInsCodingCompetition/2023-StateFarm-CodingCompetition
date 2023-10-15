package com.statefarm.codingcompetition.simpledatatool;

import static org.junit.Assert.assertEquals;

import org.junit.Before;
import org.junit.Test;

import com.statefarm.codingcompetition.simpledatatool.controller.SimpleDataTool;

public class TestSet1 {

    private static SimpleDataTool controller;

    @Before
    public void initialize() {
        controller = new SimpleDataTool();
    }

    @Test
    public void test1_getNumClosedClaims() {
        assertEquals(362, controller.getNumClosedClaims());
    }

    @Test
    public void test2_getNumClaimsForClaimHandlerId() {
        assertEquals(9, controller.getNumClaimsForClaimHandlerId(1));
        assertEquals(4, controller.getNumClaimsForClaimHandlerId(93));
        assertEquals(6, controller.getNumClaimsForClaimHandlerId(127));
    }

    @Test
    public void test3_getNumDisastersForState() {
        assertEquals(2, controller.getNumDisastersForState("Arizona"));
        assertEquals(5, controller.getNumDisastersForState("Georgia"));
        assertEquals(2, controller.getNumDisastersForState("Illinois"));
        assertEquals(9, controller.getNumDisastersForState("Texas"));
        assertEquals(2, controller.getNumDisastersForState("District of Columbia"));
    }
}
