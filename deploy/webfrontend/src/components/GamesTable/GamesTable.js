import Table from 'react-bootstrap/Table';
import { Button, OverlayTrigger } from "react-bootstrap";
import { Play } from 'react-bootstrap-icons';
import { useNavigate } from 'react-router-dom';
import {apiGetGameRoundHistory, apiGetGameRoundScoreboard} from "../../api.js"
import { GridGenerator } from 'react-hexgrid';


const ID_map = { 1: "team1", 2: "team2", 3: "team3", 4: "team4", 5: "team5", 6: "team6", 7: "team7", 8: "team8", 9: "team9", 10: "team10", 11: "team11", 12: "team12", 13: "team13", 14: "team14", 15: "team15", 16: "team16" }
const PLAYER_COLORS = { null: "none", 1: "#008000", 2: "#0000FF", 3: "#FF0000", 4: "#00FFFF", 5: "#FF00FF", 6: "#FFFF00", 7: "salmon", 8: "darkorange", 9: "lime", 10: "violet", 11: "pink", 12: "grey", 13: "royalblue", 14: "palegreen", 15: "peru", 16: "orangered" }

function RoundScoreboardOverlay(props) {
    let rows = []
    for (const [key, value] of Object.entries(props.scoreboard)) {
        rows.push(<tr key={props.ID + value["real_ID"].toString()} style={{ backgroundColor: PLAYER_COLORS[value["real_ID"]] }}><td>{parseInt(key)+1}</td><td>{value["name"]}</td><td>{value["preferred_name"]}</td></tr>)
    }
    return (<Table striped bordered hover>
        <thead>
            <tr style={{backgroundColor:"grey"}}>
                <th>#</th>
                <th>Name</th>
                <th>Nick</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </Table>)
}

function ScoreboardOverlay(props) {
    let rows = []
    for (const [key, value] of Object.entries(props.scoreboard)) {
        for(const row of value){
            rows.push(<tr key={props.ID + row["real_ID"].toString()} style={{ backgroundColor: PLAYER_COLORS[row["real_ID"]] }}><td>{parseInt(key)}</td><td>{row["name"]}</td><td>{row["preferred_name"]}</td></tr>)
        }
    }
    return (<Table striped bordered hover>
        <thead>
            <tr style={{backgroundColor:"grey"}}>
                <th>#</th>
                <th>Name</th>
                <th>Nick</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </Table>)
}



function GamesTableRow(props) {
    const game = props.game;
    const navigate = useNavigate();


    async function doNavigate(game, round, scoreboard){
        props.setLoading(true);
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
        props.setMapStatus(hexagonMap);
        props.setGameScoreboard(round_scoreboard);
        props.setGameHistory(gameHistory);
        props.setLoading(false);
        
        props.setTopText("Game "+game+" - Round " +round);
        navigate("/play/"+game+"/"+round);
    }

    async function doNavigateOutput(game, round){
        navigate("/output/"+game+"/"+round);
    }

    return (
        <tr >
            <td>
                {game["ID"]}
            </td>
            <td >
                {ID_map[game["scoreboard"]["1"][0]["real_ID"]]}
            </td>
            <td>
                <OverlayTrigger
                    placement="right"
                    delay={{ show: 250, hide: 400 }}
                    overlay={<div><ScoreboardOverlay scoreboard={game["scoreboard"]} ID={game["ID"] + "final"} /></div>}
                >
                    <Button variant="success">See Scoreboard</Button>
                </OverlayTrigger>
            </td>
            <td>
                <OverlayTrigger
                    placement="right"
                    delay={{ show: 250, hide: 400 }}
                    overlay={<div><RoundScoreboardOverlay scoreboard={game["rounds"][0]["scoreboard"]} ID={game["ID"] + "0"} /></div>}
                >
                    <Button variant="success">See Scoreboard</Button>
                </OverlayTrigger>
                <Button variant="success" className={"mx-2"} onClick={() => {doNavigate(game["ID"], 0, game["rounds"][0]["scoreboard"])}}><Play></Play></Button>
                {Object.entries(game["rounds"][0]["scoreboard"]).map((e)=>e[1]["real_ID"]).includes(props.userID)?<Button variant="success" onClick={()=>{doNavigateOutput(game["ID"], 0)}}>output</Button>:<></>}
            </td>
            <td>
                <OverlayTrigger
                    placement="right"
                    delay={{ show: 250, hide: 400 }}
                    overlay={<div><RoundScoreboardOverlay scoreboard={game["rounds"][1]["scoreboard"]} ID={game["ID"] + "1"} /></div>}
                >
                    <Button variant="success">See Scoreboard</Button>
                </OverlayTrigger>
                <Button variant="success" className={"mx-2"} onClick={() => {doNavigate(game["ID"], 1, game["rounds"][1]["scoreboard"])}}><Play></Play></Button>
                {Object.entries(game["rounds"][1]["scoreboard"]).map((e)=>e[1]["real_ID"]).includes(props.userID)?<Button variant="success" onClick={()=>{doNavigateOutput(game["ID"], 1)}}>output</Button>:<></>}
            </td>
            <td>
                <OverlayTrigger
                    placement="right"
                    delay={{ show: 250, hide: 400 }}
                    overlay={<div><RoundScoreboardOverlay scoreboard={game["rounds"][2]["scoreboard"]} ID={game["ID"] + "2"} /></div>}
                >
                    <Button variant="success">See Scoreboard</Button>
                </OverlayTrigger>
                <Button variant="success" className={"mx-2"} onClick={() => {doNavigate(game["ID"], 2, game["rounds"][2]["scoreboard"])}}><Play></Play></Button>
                {Object.entries(game["rounds"][2]["scoreboard"]).map((e)=>e[1]["real_ID"]).includes(props.userID)?<Button variant="success" onClick={()=>{doNavigateOutput(game["ID"], 2)}}>output</Button>:<></>}
            </td>
            <td>
                <OverlayTrigger
                    placement="right"
                    delay={{ show: 250, hide: 400 }}
                    overlay={<div><RoundScoreboardOverlay scoreboard={game["rounds"][3]["scoreboard"]} ID={game["ID"] + "3"} /></div>}
                >
                    <Button variant="success">See Scoreboard</Button>
                </OverlayTrigger>
                <Button variant="success" className={"mx-2"} onClick={() => {doNavigate(game["ID"], 3, game["rounds"][3]["scoreboard"])}}><Play></Play></Button>
                {Object.entries(game["rounds"][3]["scoreboard"]).map((e)=>e[1]["real_ID"]).includes(props.userID)?<Button variant="success" onClick={()=>{doNavigateOutput(game["ID"], 3)}}>output</Button>:<></>}
            </td>
            <td>
                <OverlayTrigger
                    placement="right"
                    delay={{ show: 250, hide: 400 }}
                    overlay={<div><RoundScoreboardOverlay scoreboard={game["rounds"][4]["scoreboard"]} ID={game["ID"] + "final"} /></div>}
                >
                    <Button variant="success">See Scoreboard</Button>
                </OverlayTrigger>
                <Button variant="success" className={"mx-2"} onClick={() => {doNavigate(game["ID"], "final", game["rounds"][4]["scoreboard"])}}><Play></Play></Button>
                {Object.entries(game["rounds"][4]["scoreboard"]).map((e)=>e[1]["real_ID"]).includes(props.userID)?<Button variant="success" onClick={()=>{doNavigateOutput(game["ID"], "final")}}>output</Button>:<></>}
            </td>
        </tr>
    )
}

function GamesTable(props) {
    props.setTopText("Available games");
    var list = props.games.map(  // exam list to exam component list
        (game) => <GamesTableRow setTopText={props.setTopText} userID={props.userID} setMapStatus={props.setMapStatus} setGameScoreboard={props.setGameScoreboard} setGameHistory={props.setGameHistory} setLoading={props.setLoading} showError={props.showError} game={game} key={game["ID"]}></GamesTableRow>
    )
    const navigate = useNavigate();
    var autoplaybtn=<Button onClick={(e)=>{navigate("/autoplay")}} style={{ position: "fixed", zIndex: "9", "bottom":50, "right": 50 }}>{"Autoplay"}</Button>
    var customplaybtn=<Button onClick={(e)=>{navigate("/player")}} style={{ position: "fixed", zIndex: "9", "bottom":50, "right": 150 }}>{"Load game from file"}</Button>
    return (<>
        <Table striped bordered hover>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Winner</th>
                    <th>Scoreboard</th>
                    <th>Round 1</th>
                    <th>Round 2</th>
                    <th>Round 3</th>
                    <th>Round 4</th>
                    <th>Round final</th>
                </tr>
            </thead>
            <tbody>
                {list}
            </tbody>
        </Table>
        {customplaybtn}{autoplaybtn}</>
    );
}

export default GamesTable;