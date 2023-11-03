import express from 'express';

const router = express.Router();

router.post('/reset', async (req, res, next) => {
    try { 
        // TODO: LEDの演出終了

        res.setStatus(200);
        res.send();
    } catch (error) { 
        console.error("error", error); 
        res.setStatus(500);
        res.send();
    } 
});

export default router;