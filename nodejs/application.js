const SimpleDataTool = require("./simpleDataTool");
const api = require('lambda-api')();
const {
    getAgent,
    getClaim,
    getHandler,
    getDisaster,
    getClaimDensity,
    getTopMonths
} = require("./handler.js");

console.log("I'm working");

const controller = new SimpleDataTool();
controller.loadSimpleModels();

api.get("/health", async (req, res) => { res.sendStatus(200) });

api.get("/agent/:id", getAgent);
api.get("/claim/:id", getClaim);
api.get("/handler/:id", getHandler);
api.get("/disaster/:id", getDisaster);

api.get("/stats/claim/top_months", getTopMonths);
api.get("/stats/disaster/claim_density/:id", getClaimDensity);

exports.handler = async (event, context) => {
    return await api.run(event, context)
}