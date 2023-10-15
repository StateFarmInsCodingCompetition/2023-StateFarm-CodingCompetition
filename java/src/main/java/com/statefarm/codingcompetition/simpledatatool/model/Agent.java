package com.statefarm.codingcompetition.simpledatatool.model;

import com.google.gson.Gson;

public class Agent {

    private static final Gson GSON = new Gson();

    private int id, years_active;
    private String first_name, last_name, state, region, primary_language, secondary_language;

    public int getId() {
        return this.id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getYears_active() {
        return this.years_active;
    }

    public void setYears_active(int years_active) {
        this.years_active = years_active;
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

    public String getState() {
        return this.state;
    }

    public void setState(String state) {
        this.state = state;
    }

    public String getRegion() {
        return this.region;
    }

    public void setRegion(String region) {
        this.region = region;
    }

    public String getPrimary_language() {
        return this.primary_language;
    }

    public void setPrimary_language(String primary_language) {
        this.primary_language = primary_language;
    }

    public String getSecondary_language() {
        return this.secondary_language;
    }

    public void setSecondary_language(String secondary_language) {
        this.secondary_language = secondary_language;
    }

    @Override
    public String toString() {
        return GSON.toJson(this);
    }
}
