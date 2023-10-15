package com.statefarm.codingcompetition.simpledatatool;

import com.statefarm.codingcompetition.simpledatatool.controller.SimpleDataTool;
import com.statefarm.codingcompetition.simpledatatool.model.Agent;

public class Application {

    public static void main(String[] args) {
        SimpleDataTool sdt = new SimpleDataTool();
        for (Agent agent: sdt.getAgents()) {
            System.out.println(agent.getFirst_name());
        }
        System.out.println("working");
    }
}
