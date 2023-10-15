import express from 'express';

export const stateRoutes = () => {
    const router = express.Router();

    router.get('/NumDisastersForState', async (req, res) => {
        
        try {

            return res.status(200).json(result);
        } catch (error) {
            return res.status(500).json({"error": "Failed to fetch NumDisastersForState"});
        }
    });

    router.get('/MostDisasters', async (req, res) => {
        try {

            return res.status(200).json(result);
        } catch (error) {
            return res.status(500).json({"error": "Failed to fetch MostDisasters"});
        }
    });

    router.get('/LeastDisasters', async (req, res) => {
        try {
 
            return res.status(200).json(result);
        } catch (error) {
            return res.status(500).json({"error": "Failed to fetch LeastDisasters"});
        }
    });

    router.get('/MostSpokenAgentLanguage', async (req, res) => {
        try {
 
            return res.status(200).json(result);
        } catch (error) {
            return res.status(500).json({"error": "Failed to fetch MostSpokenAgentLanguage"});
        }
    });

    return router;
}
