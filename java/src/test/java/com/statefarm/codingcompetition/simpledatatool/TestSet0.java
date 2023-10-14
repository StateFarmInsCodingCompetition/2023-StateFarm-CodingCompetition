package com.statefarm.codingcompetition.simpledatatool;

import static org.junit.Assert.assertEquals;

import org.junit.Before;
import org.junit.Test;

import com.statefarm.codingcompetition.simpledatatool.controller.SimpleDataTool;

public class TestSet0 {

    private static SimpleDataTool controller;

    @Before
    public void initialize() {
        controller = new SimpleDataTool();
    }

    /**
     * Making sure that JSON files load properly. This test does not count towards
     * your score.
     */
    @Test
    public void test0_readDataFiles() {
        assertEquals(100, controller.getAgents().size());
        assertEquals(156, controller.getClaimHandlers().size());
        assertEquals(1000, controller.getClaims().size());
        assertEquals(100, controller.getDisasters().size());
    }
}
