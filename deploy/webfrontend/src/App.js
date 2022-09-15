import './App.css';
import { apiGetGames, apiGetGamesScoreboard, apiIsLoggedIn } from './api.js'
import { Container, Row, Spinner } from 'react-bootstrap';
import { useEffect, useState } from 'react';
import { BrowserRouter, Route, Routes, Navigate } from 'react-router-dom';
import GamesTable from './components/GamesTable/GamesTable.js'
import { ToastContainer, toast } from "react-toastify";
import Topbar from "./components/Topbar/Topbar.js"
import GameRenderer from './components/GameRenderer/GameRenderer';
import LoginForm from './components/Login/Login';
import "react-toastify/dist/ReactToastify.css";
import OutputRenterer from './components/OutputRenderer/OutputRenderer';
import AutoPlayer from './components/AutoPlayer/AutoPlayer';
import FilePlayer from './components/FilePlayer/FilePlayer';

let gamesID=[]

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [mapStatus, setMapStatus] = useState({});
  const [gameHistory, setGameHistory] = useState([]);
  const [gameScoreboard, setGameScoreboard] = useState([]);
  const [topText, setTopText] = useState("Games list")
  const [userID, setUserID] = useState(-1);

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
    apiIsLoggedIn().then((res) => {
      if(res){
        setLoggedIn(true);
        setUserID(res["ID"])
        console.log(res)
      }
    })
    getGames();

    const interval = setInterval(async () => {
      console.log("Checking for new games ")
      const res = await apiGetGames();
      let newGames=[]
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
            newGames.push([game, round]);
          }
          games_data={ ID: game, scoreboard: scoreboard, rounds: tmp_rounds }
          
          setGames((oldGames)=>{let newGames=oldGames.slice(); newGames.push(games_data); newGames = newGames.sort((a, b) => b["ID"] - a["ID"]); return newGames});
          gamesID.push(game)
        }
      }
    }, 10000)

    
    return () => clearInterval(interval);
  }, []);


function showError(message) {
  toast.error(message, { position: "top-center" }, { toastId: 0 });
}

function showSuccess(message) {
  toast.success(message, { position: "top-center" }, { toastId: 0 });
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
      <Topbar topText={topText} loggedIn={loggedIn} setUserID={setUserID} setLoggedIn={setLoggedIn} />
      <Routes>
        <Route path="*" element={<Navigate to="/" replace />}></Route>
        <Route path="/login" element={loggedIn?<Navigate to="/" replace></Navigate>:<LoginForm setTopText={setTopText} showError={showError} showSuccess={showSuccess} setLoggedIn={setLoggedIn} setUserID={setUserID}></LoginForm>}></Route>
        <Route path="/" element={<GamesTable setTopText={setTopText} userID={userID} setMapStatus={setMapStatus} setGameScoreboard={setGameScoreboard} setGameHistory={setGameHistory} games={games} setLoading={setLoading} showError={showError} />} ></Route>
        <Route path="/play/:game/:round" element={<GameRenderer mapStatus={mapStatus} loadNext={undefined} gameScoreboard={gameScoreboard} gameHistory={gameHistory} setMapStatus={setMapStatus} setGameScoreboard={setGameScoreboard} setGameHistory={setGameHistory} setLoading={setLoading} showError={showError} />} ></Route>
        <Route path="/output/:game/:round" element={<OutputRenterer setTopText={setTopText}></OutputRenterer>}></Route>
        <Route path="/autoplay" element={<AutoPlayer setTopText={setTopText}></AutoPlayer>}></Route>
        <Route path="/player" element={<FilePlayer setTopText={setTopText}></FilePlayer>}></Route>
      </Routes>
    </Container>
  </BrowserRouter>
);
}

export default App;
