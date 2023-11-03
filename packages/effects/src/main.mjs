import express from 'express';
import createError from 'http-errors';
import bodyParser from 'body-parser';
import challenger from './router/challenger.mjs';
import judge from './router/judge.mjs';
import session from './router/session.mjs';
import Led from './drivers/led.mjs';
import { Configs } from './config.mjs';

const port = Configs.port;
const serialPath = Configs.serialPath;

const app = express();

// body-parser
app.use(bodyParser.urlencoded({ extended: true }))

app.get('/hello', (req, res) => {
    res.send('Hello World!')
});

app.use('/challenger', challenger);
app.use('/judge', judge);
app.use('/session', session);

// catch 404 and forward to error handler
app.use(function (req, res, next) {
    next(createError(404));
});

// connect to LED controller
if (serialPath && serialPath.length > 0) { 
    Led.open(serialPath);
}
  
app.listen(port, () => {
    console.log("listen:", port);
});
  
