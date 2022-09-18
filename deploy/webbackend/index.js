"use strict";
const cors = require('cors');
const express = require('express');
const passport = require('passport');
const LocalStrategy = require('passport-local');
const session = require('express-session');
const fs = require('fs');

const PORT = 3001;
const passwords=["ytSIO8IjtEzPq88rqK9nGR1F6vBnDjaC", "JWWiiewlflUAEPxeegY1QnJUlEFpZqty", "GGC38aq8lHxbrabL4q6G24eXUUdrQDeM", "ZZrB5M0ypa9Bb5pUjUPjlw81LQk5ufzI", "t14fuoepH1p6fJUHZrISw9wERfuiA5W2", "kB1C0Q7zdbAcA9gfIa36CZJgKu681gsD", "6TezQR5Nm4aAaQMC7OSNBwlkKuUXHo1i", "Qlg615XfjnxT8W7CZUvcHccOc39e7Ur0", "nvaZgIvoJnMHkIfn7rSUJY7porDNW9OV", "CQVhZNyCks33eTLhyI4FCFH2LSUbzAEK", "V7h5GBLqNpsKM9rk2hSWbKu2FTfEKYu8", "6hLQVNQaq1KXf3pLu6ALvfWHNp9HeFQM", "5TWEKVxt1CMh3S4kQE2PDR6c3gu4oPlJ", "K4qWo4Qxip8YBcIIIhEIALN2WTqn5YvB", "BBIUV6GyjRpE8dI3ZEg7KDjGh1le2aB5", "h4A8XwTwtIpFxE00kttqHPVjnW34m2Y8"]
const users = {
    "Alberto247": [passwords[0], 1],
    "mr96": [passwords[1], 2],
    "matpro": [passwords[2], 3],
    "0000matteo0000": [passwords[3], 4],
    "hdesk": [passwords[4], 5],
    "Matte23": [passwords[5], 6],
    "SolidCinder7914": [passwords[6], 7],
    "Xato": [passwords[7], 8],
    "Drago_1729": [passwords[8], 9],
    "Ravn": [passwords[9], 10],
    "team11": [passwords[10], 11],
    "team12": [passwords[11], 12],
    "team13": [passwords[12], 13],
    "team14": [passwords[13], 14],
    "team15": [passwords[14], 15],
    "team16": [passwords[15], 16],
}
console.log(users);

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