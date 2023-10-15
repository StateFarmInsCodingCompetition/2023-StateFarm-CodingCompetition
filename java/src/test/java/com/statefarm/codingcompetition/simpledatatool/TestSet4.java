package com.statefarm.codingcompetition.simpledatatool;

import static org.junit.Assert.assertEquals;

import org.junit.Before;
import org.junit.Test;

import com.statefarm.codingcompetition.simpledatatool.controller.SimpleDataTool;

public class TestSet4 {

    private static SimpleDataTool controller;

    @Before
    public void initialize() {
        controller = new SimpleDataTool();
    }

    /**
     * OPTIONAL! OPTIONAL! OPTIONAL!
     * AS OF 9:21CDT, TEST IS OPTIONAL. SEE GITHUB ISSUE #8 FOR MORE DETAILS
     */
    @Test
    public void test12_getTopThreeMonthsWithHighestNumOfClaimsDesc() {
        String[] topThreeMonths = controller.getTopThreeMonthsWithHighestNumOfClaimsDesc();
        assertEquals(3, topThreeMonths.length);
        assertEquals("April 2023", topThreeMonths[0]);
        assertEquals("November 2022", topThreeMonths[1]);
        assertEquals("February 2023", topThreeMonths[2]);

    }
}
