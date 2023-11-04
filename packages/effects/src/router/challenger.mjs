import express from 'express';
import player from 'node-wav-player';
import Led from '../drivers/led.mjs';
import { speach } from '../drivers/voicevox.mjs';

const router = express.Router();

router.post('/:id/speak', async (req, res, next) => {
    console.log(req.body);
    try { 
        // NOTE: nameの値に応じてspeakerIdを変更する場合はここで実装
        const text = req.body.text; // 発話内容
        const name = req.body.name; // チャレンジャー名
        const speakerId = 3;

        // LEDの演出開始
        switch (req.params.id) {
            case 'a':
                await Led.send('1'); // EFFECT_MODE_C1_SPK
                break;
            case 'b':
                await Led.send('2'); // EFFECT_MODE_C2_SPK
                break;
            default:
                console.error('invalid id');
                // TODO: Error response
                break;
        }
    
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

export default router;