import express from 'express';
import Led from '../drivers/led.mjs';
import player from 'node-wav-player';
import { speach } from '../drivers/voicevox.mjs';

const router = express.Router();

router.post('/speak', async (req, res, next) => {
    console.log(req.body);
    try { 
        const text = req.body.text; // 発話内容
        const speakerId = 3; // ずんだもん // NOTE: 変更する？

        // LEDの演出開始
        await Led.send('3'); // EFFECT_MODE_JUDGE_INPROGRESS
    
        // 音声再生
        const filepath = await speach(text, speakerId);
        player.play({
            path: filepath,
        });

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

router.post('/select/:id', async (req, res, next) => {
    try { 
        // LEDの演出開始
        switch (req.params.id) {
            case 'a':
                await Led.send('4'); // EFFECT_MODE_C1_WIN
                break;
            case 'b':
                await Led.send('5'); // EFFECT_MODE_C2_WIN
                break;
            default:
                console.error('invalid id');
                // TODO: Error response
                break;
        }

        res.status(200);
        res.send();
    } catch (error) { 
        console.error("error", error); 
        res.status(500);
        res.send();
    } 
});

export default router;