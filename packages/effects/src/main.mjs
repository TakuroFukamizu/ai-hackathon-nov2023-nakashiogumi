import { speach } from './drivers/voicevox.mjs';
import player from 'node-wav-player';

(async () => { 
    try { 
        const text = "これはnodeから呼び出すテストの２回目なのだ";
        const speakerId = 3;

        const filepath = await speach(text, speakerId);
        player.play({
            path: filepath,
        });
    } catch (error) { 
        console.error("error", error); 
    } 
})();