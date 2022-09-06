import './App.css';
import {apiGetGames, apiGetGameFinalScoreboard, apiGetGameRounds, apiGetGameRoundScoreboard} from './api.js'
import { Container, Row, Spinner } from 'react-bootstrap';
import { useEffect, useState } from 'react';
import { BrowserRouter, Route, Routes, Navigate } from 'react-router-dom';
import GamesTable from './components/GamesTable/GamesTable.js'
import { ToastContainer, toast } from "react-toastify";
import Topbar from "./components/Topbar/Topbar.js"
import GameRenderer from './components/GameRenderer/GameRenderer';
import "react-toastify/dist/ReactToastify.css";

function App() {
  const [loggedIn, setLoggedIn]=useState(false);
  const [games, setGames]=useState([]);
  const [loading, setLoading]=useState(true);
  const [gameHistory, setGameHistory] = useState([]);
  const [currentGameScoreboard, setCurrentGameScoreboard]=useState([]);
  
  useEffect(() => {  
    async function getGames() {
      const res = await apiGetGames();
      let tmp_games=[]
      for(const game of res){
        let scoreboard=await apiGetGameFinalScoreboard(game);
        let rounds=await apiGetGameRounds(game);
        let tmp_rounds=[]
        for(const round of rounds){
          let round_scoreboard=await apiGetGameRoundScoreboard(game, round);
          tmp_rounds.push({ID:round, scoreboard:round_scoreboard});
        }
        tmp_games.push({ID:game, scoreboard:scoreboard, rounds:tmp_rounds})
      }
      tmp_games=tmp_games.sort((a, b)=>b["ID"]-a["ID"]);
      setGames(tmp_games);
      setLoading(false);
    }
    getGames();
  }, []);

  function showError(message) {
    toast.error(message, { position: "top-center" }, { toastId: 0 });
  }

  if(loading){
    return <Container fluid style={{height:"100vh"}} className="d-flex align-items-center justify-content-center">
      <Row>
        <Spinner animation="border" variant="primary" className="spin-load" size="lg" />
      </Row>
    </Container>;
  }

  return (
    <BrowserRouter>
      <ToastContainer />
      <Container fluid className='px-0'>
        <Topbar loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>
        <Routes>
          <Route path="*" element={<Navigate to="/" replace />}></Route>
          <Route path="/" element={<GamesTable games={games} setCurrentGameScoreboard={setCurrentGameScoreboard} setLoading={setLoading} setGameHistory={setGameHistory} showError={showError}/>} ></Route>
          <Route path="/play" element={<GameRenderer currentGameScoreboard={currentGameScoreboard} gameHistory={gameHistory} showError={showError}/>} ></Route>                        
        </Routes>
      </Container>
    </BrowserRouter>
  );
}

export default App;
