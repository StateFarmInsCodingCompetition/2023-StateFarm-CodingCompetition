package com.statefarm.codingcompetition;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import com.statefarm.codingcompetition.simpledatatool.controller.SimpleDataTool;

@RestController
public class RestEntryPoint {

    SimpleDataTool dataService = new SimpleDataTool();

    
    @GetMapping("/numberClosedClaims")
    public int getNumClosedClaims() {
        return dataService.getNumClosedClaims();
    }
    
    @GetMapping("/numClaims/{id}")
    public int getNumClaims(@PathVariable("id") int id) {
        return dataService.getNumClaimsForClaimHandlerId(id);
    }

    @GetMapping("/numDisasters/{state}")
    public int getNumDisasters(@PathVariable("state") String state) {
        return dataService.getNumDisastersForState(state);
    }

    @GetMapping("/disasterTotalCost/{id}")
    public Float getDisasterTotalCost(@PathVariable("id") int id) {
        return dataService.getTotalClaimCostForDisaster(id);
    }

    @GetMapping("/averageClaimCost/{id}")
    public Float getAverageClaimCost(@PathVariable("id") int id) {
        return dataService.getAverageClaimCostforClaimHandler(id);
    }

    @GetMapping("/stateWithMostDisasters")
    public String getStateWithMostDisasters() {
        return dataService.getStateWithTheMostDisasters();
    }

    @GetMapping("/stateWithLeastDisasters")
    public String getStateWithLeastDisasters() {
        return dataService.getStateWithTheLeastDisasters();
    }

    @GetMapping("/mostSpokenLanguage/{state}")
    public String getMostSpokenLanguage(@PathVariable("state") String state) {
        return dataService.getMostSpokenAgentLanguageByState(state);
    }

    @GetMapping("/numOpenClaims/{id}/{minSeverity}")
    public int getNumOpenClaims(@PathVariable("id") int id, @PathVariable("minSeverity") int minSeverity) {
        return dataService.getNumOfOpenClaimsForAgentAndSeverity(id, minSeverity);
    }

    @GetMapping("/numDistastersDeclaredAfterEndDate")
    public int getNumDistastersDeclaredAfterEndDate() {
        return dataService.getNumDisastersDeclaredAfterEndDate();
    }

    // Map method??

    @GetMapping("/disasterClaimDensity/{id}")
    public Float getDisasterClaimDensity(@PathVariable("id") int id) {
        return dataService.calculateDisasterClaimDensity(id);
    }
}

