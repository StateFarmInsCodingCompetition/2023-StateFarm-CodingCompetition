package com.statefarm.codingcompetition.simpledatatool.model;

import java.time.LocalDate;

import com.google.gson.Gson;
import com.google.gson.annotations.SerializedName;

public class Disaster {

    private static final Gson GSON = new Gson();

    private int id, radius_miles;
    private String type, state, name, description;
    private float lat;
    @SerializedName("long")
    private float _long;
    private LocalDate start_date, end_date, declared_date;

    public int getId() {
        return this.id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getRadius_miles() {
        return this.radius_miles;
    }

    public void setRadius_miles(int radius_miles) {
        this.radius_miles = radius_miles;
    }

    public String getType() {
        return this.type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getState() {
        return this.state;
    }

    public void setState(String state) {
        this.state = state;
    }

    public String getName() {
        return this.name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDescription() {
        return this.description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public float getLat() {
        return this.lat;
    }

    public void setLat(float lat) {
        this.lat = lat;
    }

    public float getLong() {
        return this._long;
    }

    public void setLong(float _long) {
        this._long = _long;
    }

    public LocalDate getStart_date() {
        return this.start_date;
    }

    public void setStart_date(LocalDate start_date) {
        this.start_date = start_date;
    }

    public LocalDate getEnd_date() {
        return this.end_date;
    }

    public void setEnd_date(LocalDate end_date) {
        this.end_date = end_date;
    }

    public LocalDate getDeclared_date() {
        return this.declared_date;
    }

    public void setDeclared_date(LocalDate declared_date) {
        this.declared_date = declared_date;
    }

    @Override
    public String toString() {
        return GSON.toJson(this);
    }

}
