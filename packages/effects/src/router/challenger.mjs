import express from 'express';

const router = express.Router();

router.post('/:id/speak', async (req, res, next) => {
    console.log(req.body);
    try { 
        // NOTE: nameの値に応じてspeakerIdを変更する場合はここで実装
        const text = req.body.text; // 発話内容
        const name = req.body.name; // チャレンジャー名
        const speakerId = 3;

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

export default router;