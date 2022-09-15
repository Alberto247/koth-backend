"use strict";
const cors = require('cors');
const express = require('express');
const passport = require('passport');
const LocalStrategy = require('passport-local');
const session = require('express-session');
const fs = require('fs');

const PORT = 3001;
const users = {
    "team1": ["team1", 1],
    "team2": ["team2", 2],
    "team3": ["team3", 3],
    "team4": ["team4", 4],
    "team5": ["team5", 5],
    "team6": ["team6", 6],
    "team7": ["team7", 7],
    "team8": ["team8", 8],
    "team9": ["team9", 9],
    "team10": ["team10", 10],
    "team11": ["team11", 11],
    "team12": ["team12", 12],
    "team13": ["team13", 13],
    "team14": ["team14", 14],
    "team15": ["team15", 15],
    "team16": ["team16", 16],
}

passport.use(new LocalStrategy(function verify(username, password, callback) {
    if (username in users && users[username][0] == password) {
        return callback(null, { ID: users[username][1] })
    }
    return callback(null, false, { message: 'Incorrect username or password' })
}))

passport.serializeUser((user, cb) => {
    cb(null, { ID: user.ID });
})

passport.deserializeUser((user, cb) => {
    return cb(null, user);
})

const app = new express();

var whitelist = ['https://frontend.registry.alberto247.xyz:7394', 'http://10.0.1.4:3000']
app.use(cors({
    origin: function (origin, callback) {
        if (whitelist.indexOf(origin) !== -1) {
            callback(null, true)
        } else {
            callback(new Error('Not allowed by CORS'))
        }
    },
    credentials: true
}));

app.use(express.json());
app.set('trust proxy', 1);
app.use(session({
    cookie: {
        sameSite: 'none', // lax or strict
        secure: true, // Crucial
        maxAge: 1000 * 60 * 60 * 24 * 30, // 30 days
    },
    proxy: true, // Crucial
    resave: false,
    saveUninitialized: true,
    secret: 'just a secret',
}));
app.use(passport.authenticate('session'))

const isLoggedIn = (req, res, next) => {
    if (req.isAuthenticated()) {
        return next();
    }
    return res.status(401).json({ message: "Not authenticated" });
}

app.post("/login", passport.authenticate('local'), (req, res) => {
    try {
        res.status(200).json({ ID: req.user.ID });
    }
    catch (err) {
        res.status(500).end();
    }
})

app.get("/logout", (req, res) => {
    try {
        req.logout(() => {
            res.status(200).end();
        })
    }
    catch (err) {
        res.status(500).end();
    }
})

app.get("/me", isLoggedIn, async (req, res) => {
    try {
        res.status(200).json({ ID: req.user.ID });
    }
    catch (err) {
        res.status(500).end();
    }
})

app.get("/games", async (req, res) => {
    try {
        let rawdata = fs.readFileSync('/results/complete_rounds.json');
        res.status(200).json(JSON.parse(rawdata))
    } catch (err) {
        res.status(500).end();
    }
})


app.get("/games/:game/rounds", async (req, res) => {
    try {
        const game = parseInt(req.params.game);
        let data;
        try {
            data = fs.readFileSync("/results/" + game + "/available_games.json")
            res.status(200).json(JSON.parse(data))
        } catch (err) {
            res.status(404).json({ "error": "game does not exists" })
        }
    } catch (err) {
        res.status(500).end()
    }
})

app.get("/games/:game/scoreboard", async (req, res) => {
    try {
        const game = req.params.game;
        if (!/^[a-z0-9]+$/.test(game)) {
            return res.status(404).json({ "error": "game does not exists" })
        }
        let data;
        try {
            data = fs.readFileSync("/results/" + game + "/scoreboard_final.json")
            res.status(200).json(JSON.parse(data))
        } catch (err) {
            res.status(404).json({ "error": "game does not exists" })
        }
    } catch (err) {
        res.status(500).end()
    }
})

app.get("/games/:game/:round/scoreboard", async (req, res) => {
    try {
        const game = req.params.game;
        const round = req.params.round;
        if (!/^[a-z0-9]+$/.test(game) || !/^[a-z0-9]+$/.test(round)) {
            return res.status(404).json({ "error": "game does not exists" })
        }
        let data;
        try {
            data = fs.readFileSync("/results/" + game + "/scoreboard_game_" + round + ".json")
            res.status(200).json(JSON.parse(data))
        } catch (err) {
            res.status(404).json({ "error": "game does not exists" })
        }
    } catch (err) {
        res.status(500).end()
    }
})

app.post("/games/scoreboards", async (req, res) => {
    try {
        let games = req.body.games;
        let result = {}
        for (const game of games) {
            if (/^[a-z0-9]+$/.test(game)) {
                result[game] = {}
                try {
                    const data = fs.readFileSync("/results/" + game + "/scoreboard_final.json");
                    result[game]["scoreboard"] = JSON.parse(data);
                } catch (err) {

                }
                let rounds = [];
                try {
                    rounds = JSON.parse(fs.readFileSync("/results/" + game + "/available_games.json"))
                } catch (err) {

                }

                result[game]["rounds"] = {}
                for (const round of rounds) {
                    try {
                        const data = fs.readFileSync("/results/" + game + "/scoreboard_game_" + round + ".json")
                        result[game]["rounds"][round] = JSON.parse(data)
                    } catch (err) {

                    }
                }
            }
        }
        res.status(200).json(result)
    } catch (err) {
        res.status(500).end();
    }
})

app.get("/games/:game/:round/history", async (req, res) => {
    try {
        const game = req.params.game;
        const round = req.params.round;
        if (!/^[a-z0-9]+$/.test(game) || !/^[a-z0-9]+$/.test(round)) {
            return res.status(404).json({ "error": "game does not exists" })
        }
        let data;
        try {
            data = fs.readFileSync("/results/" + game + "/history_game_" + round + ".json")
            res.status(200).json(JSON.parse(data))
        } catch (err) {
            res.status(404).json({ "error": "game does not exists" })
        }
    } catch (err) {
        res.status(500).end()
    }
})

app.get("/games/:game/:round/output", isLoggedIn, async (req, res) => {
    try {
        const game = req.params.game;
        const round = req.params.round;
        if (!/^[a-z0-9]+$/.test(game) || !/^[a-z0-9]+$/.test(round)) {
            return res.status(404).json({ "error": "game does not exists" })
        }
        const id = req.user.ID
        let data;
        try {
            data = fs.readFileSync("/results/" + game + "/logs/team-" + id + "-game-" + round + ".logs")
            res.status(200).json(data.toString('base64'))
        } catch (err) {
            res.status(404).json({ "error": "game does not exists" })
        }
    } catch (err) {
        res.status(500).end()
    }
})



app.listen(PORT, '0.0.0.0', () => console.log(`Server running on http://0.0.0.0:${PORT}/`));