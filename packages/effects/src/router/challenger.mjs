import express from 'express';

const router = express.Router();

router.post('challenger/:name/speak', async (req, res, next) => {
    console.log(req);
    try { 
        const text = "これはnodeから呼び出すテストの２回目なのだ";
        const speakerId = 3;
    
        const filepath = await speach(text, speakerId);
        player.play({
            path: filepath,
        });
        res.setStatus(200);
        res.send();
    } catch (error) { 
        console.error("error", error); 
        res.setStatus(500);
        res.send();
    } 
});

export default router;