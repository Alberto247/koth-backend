"use strict";
const express = require('express');
const fs = require('fs');

const PORT = 3001;

const app = new express();

app.use(express.json());
app.set('trust proxy', 1);

app.get("/scoreboard", async (req, res)=>{
    try{
        let rawdata = fs.readFileSync("/results/current_scoreboard.json");
        res.status(200).json(JSON.parse(rawdata));
    } catch (err) {
        let rawdata = [{"teamId": 0, "score": 0}, {"teamId": 1, "score": 0}, {"teamId": 2, "score": 0}, {"teamId": 3, "score": 0}, {"teamId": 4, "score": 0}, {"teamId": 5, "score": 0}, {"teamId": 6, "score": 0}, {"teamId": 7, "score": 0}, {"teamId": 8, "score": 0}, {"teamId": 9, "score": 0}, {"teamId": 10, "score": 0}, {"teamId": 11, "score": 0}]
        res.status(200).json(rawdata);
    }
})

app.get("/user-scoreboard", async (req, res)=>{
    try{
        let rawdata = fs.readFileSync("/results/user_scoreboard.json");
        res.status(200).json(JSON.parse(rawdata));
    } catch (err) {
        let rawdata = [{"teamId": 0, "score": 0}, {"teamId": 1, "score": 0}, {"teamId": 2, "score": 0}, {"teamId": 3, "score": 0}, {"teamId": 4, "score": 0}, {"teamId": 5, "score": 0}, {"teamId": 6, "score": 0}, {"teamId": 7, "score": 0}, {"teamId": 8, "score": 0}, {"teamId": 9, "score": 0}, {"teamId": 10, "score": 0}, {"teamId": 11, "score": 0}]
        res.status(200).json(rawdata);
    }
})

app.listen(PORT, '0.0.0.0', () => console.log(`Server running on http://0.0.0.0:${PORT}/`));