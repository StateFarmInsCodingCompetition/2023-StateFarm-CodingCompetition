package com.statefarm.codingcompetition.simpledatatool.model;

import com.google.gson.Gson;

public class Claim {

    private static final Gson GSON = new Gson();

    private int id, disaster_id, severity_rating, agent_assigned_id, claim_handler_assigned_id;
    private Double estimate_cost;
    private boolean total_loss, loss_of_life;
    private String status, type;

    public int getId() {
        return this.id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getDisaster_id() {
        return this.disaster_id;
    }

    public void setDisaster_id(int disaster_id) {
        this.disaster_id = disaster_id;
    }

    public int getSeverity_rating() {
        return this.severity_rating;
    }

    public void setSeverity_rating(int severity_rating) {
        this.severity_rating = severity_rating;
    }

    public int getAgent_assigned_id() {
        return this.agent_assigned_id;
    }

    public void setAgent_assigned_id(int agent_assigned_id) {
        this.agent_assigned_id = agent_assigned_id;
    }

    public int getClaim_handler_assigned_id() {
        return this.claim_handler_assigned_id;
    }

    public void setClaim_handler_assigned_id(int claim_handler_assigned_id) {
        this.claim_handler_assigned_id = claim_handler_assigned_id;
    }

    public Double getEstimate_cost() {
        return this.estimate_cost;
    }

    public void setEstimate_cost(Double estimate_cost) {
        this.estimate_cost = estimate_cost;
    }

    public boolean isTotal_loss() {
        return this.total_loss;
    }

    public boolean getTotal_loss() {
        return this.total_loss;
    }

    public void setTotal_loss(boolean total_loss) {
        this.total_loss = total_loss;
    }

    public boolean isLoss_of_life() {
        return this.loss_of_life;
    }

    public boolean getLoss_of_life() {
        return this.loss_of_life;
    }

    public void setLoss_of_life(boolean loss_of_life) {
        this.loss_of_life = loss_of_life;
    }

    public String getStatus() {
        return this.status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getType() {
        return this.type;
    }

    public void setType(String type) {
        this.type = type;
    }

    @Override
    public String toString() {
        return GSON.toJson(this);
    }
}
