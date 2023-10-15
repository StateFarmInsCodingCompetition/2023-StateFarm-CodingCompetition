const SimpleDataTool = require("./simpleDataTool");
const express = require("express");
const api = express();
const port = process.env.PORT || 1234;

console.log("I'm working");

const controller = new SimpleDataTool();
//controller.loadSimpleModels(); This has to be disabled to run :(

api.get("/", (req, res) => {
  res.json({
    name: "StatJAKE FROM STATE FARM API :)",
    description: "Allows for reading data... that's about it.",
    paths: [
      {
        id: "/claims",
        description: "Deals with claims",
        subpaths: [
          "/id/:id",
          "/count/closed",
          "/handler/:handlerId/count",
          "/handler/:handlerId/cost/average",
          "/agent/:agentId/count/severity/:severityAmount",
        ],
      },
      {
        id: "/disasters",
        description: "Deals with disasters",
        subpaths: [
          "/id/:id",
          "/id/:id/claimDensity",
          "/id/:id/cost",
          "/state/count/:state",
          "/state/counts",
          "/state/high",
          "/state/low",
          "/date/after_end",
        ],
      },
      {
        id: "/agents",
        description: "Deals with agents",
        subpaths: [
          "/id/:id",
          "/handler/id/:handlerId",
          "/top_language/:state",
          "/list_of_claim_costs",
        ],
      },
      {
        id: "/time",
        description: "Some strange ones.",
        subpaths: ["/topThreeMonths"],
      },
    ],
  });
});

api.use("/claims", require("./routers/claims")(controller));
api.use("/disasters", require("./routers/disasters")(controller));
api.use("/agents", require("./routers/agents")(controller));
api.use("/time", require("./routers/time")(controller));

api.listen(port, () => {
  console.log(`Started the JAKE FROM STATE FARM API on port ${port}`);
});
