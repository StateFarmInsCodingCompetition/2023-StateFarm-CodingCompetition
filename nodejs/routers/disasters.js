const express = require("express");
const router = express.Router();

const disasters = require("../data/sfcc_2023_disasters.json");

module.exports = (dataTool) => {
  router.get("/id/:id", function (req, res) {
    const { id } = req.params;
    const foundDisaster = disasters.find((a) => a.id == id);
    if (!foundDisaster) {
      return res.json(
        {
          success: false,
          reason: "Disaster not found.",
        },
        404
      );
    }
    res.json(foundDisaster);
  });
  router.get("/id/:id/claimDensity", function (req, res) {
    const { id } = req.params;
    const disasterClaimDensity = dataTool.calculateDisasterClaimDensity(
      parseInt(id)
    );
    res.json({ disasterClaimDensity });
  });

  router.get("/id/:id/cost", function (req, res) {
    const { id } = req.params;
    const disasterAmount = dataTool.getTotalClaimCostForDisaster(parseInt(id));
    res.json({ disasterAmount });
  });

  router.get("/state/count/:state", function (req, res) {
    const { state } = req.params;
    const stateDisasterCounts = dataTool.getNumDisastersForState(state);
    res.json({ stateDisasterCounts });
  });

  router.get("/state/counts", function (req, res) {
    const stateAmounts = {};
    for (const disaster of disasters) {
      if (!stateAmounts[disaster.state]) stateAmounts[disaster.state] = 0;
      stateAmounts[disaster.state]++;
    }

    let sortableAmounts = [];
    for (const state in stateAmounts) {
      sortableAmounts.push([state, stateAmounts[state]]);
    }
    res.json({ stateDisasterCounts: sortableAmounts });
  });

  router.get("/state/high", function (req, res) {
    const stateWithMostDisasters = dataTool.getStateWithMostDisasters();
    res.json({ stateWithMostDisasters });
  });

  router.get("/state/low", function (req, res) {
    const stateWithLeastDisasters = dataTool.getStateWithLeastDisasters();
    res.json({ stateWithLeastDisasters });
  });

  router.get("/date/after_end", function (req, res) {
    const declaredAfterEndAmount =
      dataTool.getNumDisastersDeclaredAfterEndDate();
    res.json({ declaredAfterEndAmount });
  });

  return router;
};
