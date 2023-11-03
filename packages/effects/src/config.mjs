import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const envpath = path.resolve(__dirname, '..', '.env');
console.log("envpath", envpath);
dotenv.config(envpath);
// console.log("env", process.env) // remove this 

export const Configs = {
    voicevoxUrl: process.env.VOICEVOX_URL,
    port: process.env.PORT,
    serialPath: process.env.SERIAL_PATH,
};