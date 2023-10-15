package com.statefarm.codingcompetition.simpledatatool.model;

public class State {
    String name;
    int disasterNum;


    public State() {
    }

    public State(String name) {
        this.name = name;
    }

    public State(String name, int disasterNum) {
        this.name = name;
        this.disasterNum = disasterNum;
    }

    public String getName() {
        return name;
    }
    public int getDisasterNum() {
        return disasterNum;
    }
    public void setName(String name) {
        this.name = name;
    }
    public void setDisasterNum(int disasterNum) {
        this.disasterNum = disasterNum;
    }
}