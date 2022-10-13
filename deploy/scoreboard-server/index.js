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
        res.status(500).end();
    }
})

app.get("/user-scoreboard", async (req, res)=>{
    try{
        let rawdata = fs.readFileSync("/results/user_scoreboard.json");
        res.status(200).json(JSON.parse(rawdata));
    } catch (err) {
        res.status(500).end();
    }
})

app.listen(PORT, '0.0.0.0', () => console.log(`Server running on http://0.0.0.0:${PORT}/`));