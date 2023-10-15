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
}

