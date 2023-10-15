package com.statefarm.codingcompetition.simpledatatool.model;

public class Pair implements Comparable<Pair> {
    private float cost;
    private String date;

    public Pair(Float cost, String date) {
        this.cost = cost;
        this.date = date;
    }

    public Pair() {
    }

    public void setCost(float cost) {
        this.cost = cost;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public float getCost() {
        return cost;
    }

    public String getDate() {
        return date;
    }

    @Override
    public int compareTo(Pair other) {
        // Compare based on cost
        int costComparison = Float.compare(this.cost, other.getCost());
        
        if (costComparison != 0) {
            // If costs are different, return the comparison result
            return costComparison;
        } else {
            // If costs are equal, compare based on date
            return this.date.compareTo(other.getDate());
        }
    }

    @Override
    public String toString() {
        return "Pair [cost=" + cost + ", date=" + date + "]";
    }
    
}