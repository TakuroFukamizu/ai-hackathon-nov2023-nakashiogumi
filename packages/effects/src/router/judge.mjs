import express from 'express';

const router = express.Router();

router.post('/speak', async (req, res, next) => {
    console.log(req);
    var param = {"値":"これはサンプルAPIです"};
    res.header('Content-Type', 'application/json; charset=utf-8');
    res.send(param);
});

export default router;