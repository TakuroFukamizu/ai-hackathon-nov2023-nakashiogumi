import axios from 'axios'; 
import fs from 'fs';
import { Configs } from '../config.mjs';

export async function speach(text, speakerId) { 
    const baseUrl = Configs.voicevoxUrl;
    try { 
        // get query
        const encodedText = encodeURIComponent(text);
        const query = await axios.post(`${baseUrl}/audio_query?speaker=${speakerId}&text=${encodedText}`);
        // console.log("query", query.data);

        // get audio data
        console.time('synthesis');
        const audioData = await axios.post(
            `${baseUrl}/synthesis?speaker=${speakerId}`,
            query.data,
            {
                responseType: 'arraybuffer',
            }
        );
        console.timeEnd('synthesis');
        const outfilePaht = './out.wav';
        console.log(audioData.data);
        fs.writeFileSync(outfilePaht, audioData.data, 'binary');
        return outfilePaht;
    } catch (error) { 
        console.error("error", error); 
    } 
}