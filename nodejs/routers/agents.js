const express = require("express");
const router = express.Router();

const agents = require("../data/sfcc_2023_agents.json");
const handlers = require("../data/sfcc_2023_claim_handlers.json");

module.exports = (dataTool) => {
  router.get("/id/:id", function (req, res) {
    const { id } = req.params;
    const foundAgent = agents.find((a) => a.id == id);
    if (!foundAgent) {
      return res.json(
        {
          success: false,
          reason: "Agent not found.",
        },
        404
      );
    }
    res.json(foundAgent);
  });
  router.get("/handler/id/:id", function (req, res) {
    const { id } = req.params;
    const foundHandler = handlers.find((a) => a.id == id);
    if (!foundHandler) {
      return res.json(
        {
          success: false,
          reason: "Handler not found.",
        },
        404
      );
    }
    res.json(foundHandler);
  });

  router.get("/top_language/:state", function (req, res) {
    const { state } = req.params;
    const API_Response = dataTool.getMostSpokenAgentLanguageByState(state);
    if (API_Response == "") {
      return res.json(
        {
          success: false,
          reason: "State likely doesn't exist.",
        },
        404
      );
    }
    res.json({ topLanguage: API_Response });
  });

  router.get("/list_of_claim_costs", function (req, res) {
    const API_Response = dataTool.buildMapOfAgentsToTotalClaimCost();
    res.json(API_Response);
  });

  return router;
};
