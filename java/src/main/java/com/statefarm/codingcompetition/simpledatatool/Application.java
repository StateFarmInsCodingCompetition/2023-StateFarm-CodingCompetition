package com.statefarm.codingcompetition.simpledatatool;

import com.statefarm.codingcompetition.simpledatatool.controller.SimpleDataTool;

public class Application {

    public static void main(String[] args) {
        SimpleDataTool sdt = new SimpleDataTool();

        System.out.println("working");

        System.out.println(sdt.getNumClosedClaims());
        // System.out.println(sdt.getNumClaimsForClaimHandlerId(19));
        // System.out.println(sdt.getNumDisastersForState("Texas"));
        // System.out.println(sdt.getTotalClaimCostForDisaster(19));
        // System.out.println(sdt.getAverageClaimCostforClaimHandler(12));
        // System.out.println(sdt.getStateWithTheMostDisasters());
        System.out.println(sdt.getStateWithTheLeastDisasters());
    }
}
