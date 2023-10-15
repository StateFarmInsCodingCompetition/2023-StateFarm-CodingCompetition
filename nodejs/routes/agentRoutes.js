import express from 'express';
import { SimpleDataTool } from '../simpleDataTool.js';
export const agentRoutes = () => {
    const router = express.Router();

    router.get('/AverageClaimCost/:id', async (req, res) => {
        
        try {
            dataTool = new SimpleDataTool();
            results = dataTool.getAverageClaimCostForClaimHandler(req.params['id'])
            return res.status(200).json(result);
        } catch (error) {
            return res.status(500).json({"error": "Failed to fetch AverageClaimCost"});
        }
    });

    router.post('/NumOfOpenClaim', async (req, res) => {
        try {

            return res.status(200).json(result);
        } catch (error) {
            return res.status(500).json({"error": "Failed to fetch NumOfOpenClaim"});
        }
    });

    router.get('/buildMap', async (req, res) => {
        try {
 
            return res.status(200).json(result);
        } catch (error) {
            return res.status(500).json({"error": "Failed to buildMap"});
        }
    });

    return router;
}