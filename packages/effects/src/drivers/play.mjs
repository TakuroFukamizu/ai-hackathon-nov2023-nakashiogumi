import player from 'node-wav-player';

export async function play(filepath) { 
    return new Promise((resolve, reject) => {
        player.play({
            path: filepath,
        }).then(() => {
            console.log('The wav file started to be played successfully.');
            resolve(true);
        }).catch((error) => {
            console.error(error);
            reject(error);
        });
    });
}