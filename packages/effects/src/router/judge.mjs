import express from 'express';

const router = express.Router();

router.post('/speak', async (req, res, next) => {
    console.log(req.body);
    try { 
        const text = req.body.text; // 発話内容
        const speakerId = 3; // NOTE: 変更する？

        // TODO: LEDの演出開始
    
        // 音声再生
        const filepath = await speach(text, speakerId);
        player.play({
            path: filepath,
        });

        // TODO: LEDの演出終了

        res.setStatus(200);
        res.send();
    } catch (error) { 
        console.error("error", error); 
        res.setStatus(500);
        res.send();
    } 
});

router.post('/select/:id', async (req, res, next) => {
    try { 
        // TODO: LEDの演出開始

        res.setStatus(200);
        res.send();
    } catch (error) { 
        console.error("error", error); 
        res.setStatus(500);
        res.send();
    } 
});

export default router;