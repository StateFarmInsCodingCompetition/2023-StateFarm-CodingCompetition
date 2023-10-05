package com.statefarm.codingcompetition.simpledatatool;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;

import java.math.BigDecimal;
import java.util.List;

import org.junit.Before;
import org.junit.Test;

import com.statefarm.codingcompetition.simpledatatool.controller.SimpleDataTool;
import com.statefarm.codingcompetition.simpledatatool.io.SimpleModel;

public class ApplicationTest {

    private static SimpleDataTool controller;

    @Before
    public void initialize() {
        controller = new SimpleDataTool();
    }

    // Example Test
    @Test
    public void readSimpleJson() {

        List<SimpleModel> simpleModels = controller.loadSimpleModels();

        assertNotNull("controller returned null", simpleModels);
        assertEquals("controller did not return expected number of simple models", 1, simpleModels.size());

        SimpleModel model1 = simpleModels.get(0);

        assertEquals("John Smith", model1.getName());
        assertEquals(1, model1.getInteger());
        assertEquals(new BigDecimal("1.99"), model1.getDecimal());
    }
}
