package com.statefarm.codingcompetition.simpledatatool.model;

import com.google.gson.Gson;

public class ClaimHandler {

    private static final Gson GSON = new Gson();

    private int id;
    private String first_name;
    private String last_name;

    public int getId() {
        return this.id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getFirst_name() {
        return this.first_name;
    }

    public void setFirst_name(String first_name) {
        this.first_name = first_name;
    }

    public String getLast_name() {
        return this.last_name;
    }

    public void setLast_name(String last_name) {
        this.last_name = last_name;
    }

    @Override
    public String toString() {
        return GSON.toJson(this);
    }
}
