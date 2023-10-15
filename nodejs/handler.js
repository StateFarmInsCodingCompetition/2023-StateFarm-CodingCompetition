const SimpleDataTool = require("./simpleDataTool");
const dataTool = new SimpleDataTool();



const getAgent = async (req, res) => {
    try {
        let data = dataTool.getAgent(req.params.id);
        if (data.length != 1) {
            res.status(500).send({
                success: false,
                agent: null
            })
        } else {
            res.status(200).send({
                success: true,
                agent: data[0]
            })
        }
    } catch (err) {
        res.status(500).send({
            success: false,
            density: -1,
            message: "Error Invalid Query"
        })
    }
}

const getClaim = async (req, res) => {
    try {
        let data = dataTool.getAgent(req.params.id);
        if (data.length != 1) {
            res.status(500).send({
                success: false,
                disaster: null
            })
        } else {
            res.status(200).send({
                success: true,
                claim: data[0]
            })
        }
    } catch (err) {
        res.status(500).send({
            success: false,
            density: -1,
            message: "Error Invalid Query"
        })
    }

}
const getHandler = async (req, res) => {
    try {
        let data = dataTool.getClaimHandler(req.params.id);
        if (data.length != 1) {
            res.status(500).send({
                success: false,
                handler: null
            })
        } else {
            res.status(200).send({
                success: true,
                handler: data[0]
            })
        }
    } catch (err) {
        res.status(500).send({
            success: false,
            density: -1,
            message: "Error Invalid Query"
        })
    }

}
const getDisaster = async (req, res) => {
    try {
        let data = dataTool.getDisaster(req.params.id);
        if (data.length != 1) {
            res.status(500).send({
                success: false,
                disaster: null
            })
        } else {
            res.status(200).send({
                success: true,
                disaster: data[0]
            })
        }
    } catch (err) {
        res.status(500).send({
            success: false,
            density: -1,
            message: "Error Invalid Query"
        })
    }

}

const getTopMonths = async (req, res) => {
    try {
        let data = dataTool.getTopThreeMonthsWithHighestNumOfClaimsDesc();

        res.status(200).send({
            success: true,
            topMonths: data
        })
    } catch (err) {
        res.status(500).send({
            success: false,
            density: -1,
            message: "Error Invalid Query"
        })
    }

}

const getClaimDensity = async (req, res) => {
    try {
        let data = dataTool.calculateDisasterClaimDensity();
        res.status(200).send({

        })
    } catch (err) {
        res.status(500).send({
            success: false,
            density: -1,
            message: "Error Invalid Query"
        })
    }
}



module.exports = {
    getAgent,
    getClaim,
    getHandler,
    getDisaster,
    getTopMonths,
};