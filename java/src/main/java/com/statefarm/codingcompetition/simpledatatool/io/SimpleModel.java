package com.statefarm.codingcompetition.simpledatatool.io;

import java.math.BigDecimal;

import com.google.gson.Gson;

public class SimpleModel {

    private static final Gson GSON = new Gson();

    private String name;
    private int integer;
    private BigDecimal decimal;

    public String getName() {
        return name;
    }

    public SimpleModel setName(String name) {
        this.name = name;
        return this;
    }

    public int getInteger() {
        return integer;
    }

    public SimpleModel setInteger(int integer) {
        this.integer = integer;
        return this;
    }

    public BigDecimal getDecimal() {
        return decimal;
    }

    public SimpleModel setDecimal(BigDecimal decimal) {
        this.decimal = decimal;
        return this;
    }

    @Override
    public String toString() {
        return GSON.toJson(this);
    }
}
