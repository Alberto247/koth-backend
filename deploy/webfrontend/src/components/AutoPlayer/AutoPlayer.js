import { useNavigate, useLocation } from 'react-router-dom';
import { useEffect, useState } from 'react';
import {apiGetGames, apiGetGameRoundHistory, apiGetGameRoundScoreboard, apiGetGameRounds} from "../../api.js"
import GameRenderer from '../GameRenderer/GameRenderer.js';
import { GridGenerator } from 'react-hexgrid';
import { Container, Row, Spinner, Button } from 'react-bootstrap';


let ignoredRounds=[];
let gameQueue=[];

function AutoPlayer(props){
    const navigate = useNavigate();
    const [enabled, setEnabled] = useState(false);
    const [mapStatus, setMapStatus] = useState({});
    const [gameHistory, setGameHistory] = useState([]);
    const [gameScoreboard, setGameScoreboard] = useState([]);
    const [gameRunning, setGameRunning] = useState(false);

    async function loadNewGames(){
        setGameRunning(false);
        while(gameQueue.length<=0){
            console.log("Autoplay checking for new games")
            const res = await apiGetGames();
            for (const game of res){
                if (!ignoredRounds.includes(game)){
                    ignoredRounds.push(game);
                    let tmp_rounds = await apiGetGameRounds(game);
                    for (const round of tmp_rounds){
                        gameQueue.push([game, round]);
                    }
                }
            }
            if(gameQueue.length<=0){
                await new Promise(r => setTimeout(r, 10000));
            }
        }
        console.log("New games found, autoplaying")
        console.log(gameQueue);
        
    }

    async function enableAutoPlay(e){
        e.preventDefault();
        setEnabled(true);
        const res = await apiGetGames();
        ignoredRounds=res.slice();
        gameQueue=[];
        await nextGame();
    }

    async function nextGame(){
        if(gameQueue.length<=0){
            await loadNewGames();
        }
        const dest = gameQueue.pop(0).slice();
        const game = dest[0];
        const round = dest[1];
        let round_scoreboard=await apiGetGameRoundScoreboard(game, round);
        let gameHistory = await apiGetGameRoundHistory(game, round);
        let hexagonMap = {};
        const hexagons = GridGenerator.hexagon(10);
        for (const hexagon of hexagons) {
            hexagonMap[[hexagon.q, hexagon.r, hexagon.s].toString()] = { "hex": hexagon }
        }
        for (const hexagon of gameHistory[0]) {
            hexagonMap[hexagon[0]]["point_type"] = hexagon[1]
            hexagonMap[hexagon[0]]["owner_ID"] = hexagon[2]
            hexagonMap[hexagon[0]]["current_value"] = hexagon[3]
            hexagonMap[hexagon[0]]["tuple"] = hexagon[0]
        }
        setMapStatus(hexagonMap);
        setGameScoreboard(round_scoreboard);
        setGameHistory(gameHistory);
        setGameRunning(true);
    }

    if(!enabled){
        return <h1>Autoplay is disabled. <Button onClick={enableAutoPlay}>Enable autoplay</Button></h1>
    }

    if(!gameRunning){
        return <Container fluid style={{ height: "100vh" }} className="d-flex align-items-center justify-content-center">
          <Row>
            <Spinner animation="border" variant="primary" className="spin-load" size="lg" />
          </Row>
        </Container>;
    }

    return <GameRenderer externalLoad={true} autoPlay={true} mapStatus={mapStatus} loadNext={nextGame} gameScoreboard={gameScoreboard} gameHistory={gameHistory} setMapStatus={setMapStatus} setGameScoreboard={setGameScoreboard} setGameHistory={setGameHistory}/>
}


export default AutoPlayer