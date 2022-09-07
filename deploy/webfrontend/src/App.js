import './App.css';
import { apiGetGames, apiGetGameFinalScoreboard, apiGetGameRounds, apiGetGameRoundScoreboard, apiGetGamesScoreboard } from './api.js'
import { Container, Row, Spinner } from 'react-bootstrap';
import { useEffect, useState } from 'react';
import { BrowserRouter, Route, Routes, Navigate } from 'react-router-dom';
import GamesTable from './components/GamesTable/GamesTable.js'
import { ToastContainer, toast } from "react-toastify";
import Topbar from "./components/Topbar/Topbar.js"
import GameRenderer from './components/GameRenderer/GameRenderer';
import "react-toastify/dist/ReactToastify.css";

let gamesID=[]

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [mapStatus, setMapStatus] = useState({});
  const [gameHistory, setGameHistory] = useState([]);
  const [gameScoreboard, setGameScoreboard] = useState([]);

  useEffect(() => {
    async function getGames() {
      const res = await apiGetGames();
      let tmp_games = await apiGetGamesScoreboard(res);
      let games_data = []
      for (const [game, data] of Object.entries(tmp_games)) {
        let scoreboard = data["scoreboard"];
        let tmp_rounds = []
        for (const [round, round_data] of Object.entries(data["rounds"])) {
          let round_scoreboard = round_data;
          tmp_rounds.push({ ID: round, scoreboard: round_scoreboard });
        }
        games_data.push({ ID: game, scoreboard: scoreboard, rounds: tmp_rounds })
      }

      games_data = games_data.sort((a, b) => b["ID"] - a["ID"]);
      gamesID=games_data.map((x) => parseInt(x["ID"]))
      setGames(games_data);
      setLoading(false);
    }
    getGames();
  }, []);

  setInterval(async () => {
    console.log("Checking for new games ")
    const res = await apiGetGames();
    for (const game of res) {

      if (!(gamesID.includes(game))) {
        console.log(game)
        let tmp_games = await apiGetGamesScoreboard([game]);
        let games_data = []
        let data = tmp_games[game]
        let scoreboard = data["scoreboard"];
        let tmp_rounds = []
        for (const [round, round_data] of Object.entries(data["rounds"])) {
          let round_scoreboard = round_data;
          tmp_rounds.push({ ID: round, scoreboard: round_scoreboard });
        }
        games_data={ ID: game, scoreboard: scoreboard, rounds: tmp_rounds }
        console.log(games_data)
        setGames((oldGames)=>{oldGames.push(games_data); return oldGames});
        gamesID.push(game)
      }
    }
  }, 10000)

function showError(message) {
  toast.error(message, { position: "top-center" }, { toastId: 0 });
}

if (loading) {
  return <Container fluid style={{ height: "100vh" }} className="d-flex align-items-center justify-content-center">
    <Row>
      <Spinner animation="border" variant="primary" className="spin-load" size="lg" />
    </Row>
  </Container>;
}

return (
  <BrowserRouter>
    <ToastContainer />
    <Container fluid className='px-0'>
      <Topbar loggedIn={loggedIn} setLoggedIn={setLoggedIn} />
      <Routes>
        <Route path="*" element={<Navigate to="/" replace />}></Route>
        <Route path="/" element={<GamesTable setMapStatus={setMapStatus} setGameScoreboard={setGameScoreboard} setGameHistory={setGameHistory} games={games} setLoading={setLoading} showError={showError} />} ></Route>
        <Route path="/play/:game/:round" element={<GameRenderer mapStatus={mapStatus} gameScoreboard={gameScoreboard} gameHistory={gameHistory} setMapStatus={setMapStatus} setGameScoreboard={setGameScoreboard} setGameHistory={setGameHistory} setLoading={setLoading} showError={showError} />} ></Route>
      </Routes>
    </Container>
  </BrowserRouter>
);
}

export default App;
