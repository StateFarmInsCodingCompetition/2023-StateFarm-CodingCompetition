package com.statefarm.codingcompetition.simpledatatool;

import com.statefarm.codingcompetition.simpledatatool.controller.SimpleDataTool;

public class Application {

    public static void main(String[] args) {
        SimpleDataTool sdt = new SimpleDataTool();

        System.out.println(sdt.buildMapOfAgentsToTotalClaimCost());
        System.out.println("working");
    }
}
