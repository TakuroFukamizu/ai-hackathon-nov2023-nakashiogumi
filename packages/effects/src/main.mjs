import express from 'express';
import createError from 'http-errors';
import challenger from './router/challenger.mjs';
import judge from './router/judge.mjs';
import { Configs } from './config.mjs';

const port = Configs.port;
const app = express();

app.get('/hello', (req, res) => {
    res.send('Hello World!')
});

app.use('/challenger', challenger);
app.use('/judge', judge);

// catch 404 and forward to error handler
app.use(function (req, res, next) {
    next(createError(404));
});
  
app.listen(port, () => {
    console.log("listen:", port);
});
  