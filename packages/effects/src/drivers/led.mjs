import { SerialPort } from 'serialport';

class LED { 
    constructor() { 
        this.initialized = false;
    }

    open(path, baudRate = 115200) { 
        this.port = new SerialPort({ path, baudRate });
        this.initialized = true;
    }

    send(cmd) { 
        if (!this.initialized) return false;
        return new Promise((resolve, reject) => {
            this.port.write(cmd, (err) => {
                if (err) {
                    reject(err.message);
                    return;
                }
                resolve(true);
            })
        })
    }
}

const Led = new LED();

export default Led;
