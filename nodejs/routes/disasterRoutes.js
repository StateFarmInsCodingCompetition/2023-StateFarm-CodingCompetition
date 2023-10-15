import express from 'express';

export const disasterRoutes = () => {
    const router = express.Router();

    router.get('/TotalClaimCost', async (req, res) => {
        
        try {

            return res.status(200).json(result);
        } catch (error) {
            return res.status(500).json({"error": "Failed to fetch TotalClaimCost"});
        }
    });

    router.post('/DeclaredAfterEndDate', async (req, res) => {
        try {

            return res.status(200).json(result);
        } catch (error) {
            return res.status(500).json({"error": "Failed to fetch DeclaredAfterEndDate"});
        }
    });

    router.get('/ClaimDensity', async (req, res) => {
        try {
 
            return res.status(200).json(result);
        } catch (error) {
            return res.status(500).json({"error": "Failed to fetch ClaimDensity"});
        }
    });

    return router;
}