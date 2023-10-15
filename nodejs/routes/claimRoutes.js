import express from 'express';
import { SimpleDataTool } from '../simpleDataTool.js';
export const claimRoutes = () => {
    const router = express.Router();

    router.get('/numClosed', async (req, res) => {
        dataTool = new SimpleDataTool();
        results = dataTool.getNumClosedClaims()
        try {
            let result = simpleDataTool.getNumClosedClaims(sfcc)
            return res.status(200).json(result);
        } catch (error) {
            return res.status(500).json({"error": "Failed to fetch numClosed"});
        }
    });

    router.post('/NumClaimsForClaimHandlerId', async (req, res) => {
        try {

            return res.status(200).json(result);
        } catch (error) {
            return res.status(500).json({"error": "Failed to fetch NumClaimsForClaimHandlerId"});
        }
    });


    return router;
}