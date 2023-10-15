const express = require("express");
const router = express.Router();

module.exports = (dataTool) => {
  router.get("/topThreeMonths", function (req, res) {
    res.json(dataTool.getTopThreeMonthsWithHighestNumOfClaimsDesc());
  });

  return router;
};
