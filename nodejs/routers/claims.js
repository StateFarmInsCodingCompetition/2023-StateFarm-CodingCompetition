const express = require("express");
const router = express.Router();

const claims = require("../data/sfcc_2023_claims.json");
const handlers = require("../data/sfcc_2023_claim_handlers.json");

module.exports = (dataTool) => {
  router.get("/id/:id", function (req, res) {
    const { id } = req.params;
    const foundClaim = claims.find((a) => a.id == id);
    if (!foundClaim) {
      return res.json(
        {
          success: false,
          reason: "Claim not found.",
        },
        404
      );
    }
    res.json(foundClaim);
  });

  router.get("/count/closed", function (req, res) {
    const API_Response = dataTool.getNumClosedClaims();
    res.json({ amountClosed: API_Response });
  });

  router.get("/handler/:handlerId/count", function (req, res) {
    const { handlerId } = req.params;
    const foundHandler = handlers.find((handler) => handler.id == handlerId);
    if (!foundHandler) {
      return res.json(
        {
          success: false,
          reason: "Handler not found.",
        },
        400
      );
    }

    const handledAmount = dataTool.getNumClaimsForClaimHandlerId(handlerId);
    res.json({ handledAmount });
  });

  router.get("/handler/:handlerId/cost/average", function (req, res) {
    const { handlerId } = req.params;
    const foundHandler = handlers.find((handler) => handler.id == handlerId);
    if (!foundHandler) {
      return res.json(
        {
          success: false,
          reason: "Handler not found.",
        },
        400
      );
    }

    const averageCost = dataTool.getAverageClaimCostForClaimHandler(handlerId);
    res.json({ averageCost });
  });

  router.get(
    "/agent/:agentId/count/severity/:severityAmount",
    function (req, res) {
      const { agentId, severityAmount } = req.params;
      const handledAmount = dataTool.getNumClaimsForClaimHandlerId(
        agentId,
        parseInt(severityAmount)
      );
      if (handledAmount == -1) {
        return res.json(
          {
            success: false,
            reason: "Severity must be 1-10.",
          },
          400
        );
      }
      if (handledAmount == null) {
        return res.json(
          {
            success: false,
            reason: "Agent does not exist, or has no open claim.",
          },
          400
        );
      }

      res.json({ amount: handledAmount });
    }
  );

  return router;
};
