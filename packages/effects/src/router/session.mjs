import express from 'express';
import Led from '../drivers/led.mjs';

const router = express.Router();

router.post('/reset', async (req, res, next) => {
    try { 
        // LEDの演出終了
        Led.send('0'); // EFFECT_MODE_NONE

        res.status(200);
        res.send();
    } catch (error) { 
        console.error("error", error); 
        res.status(500);
        res.send();
    } 
});

export default router;