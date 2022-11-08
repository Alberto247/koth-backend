import { useNavigate, useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { Button } from "react-bootstrap";
import Form from 'react-bootstrap/Form'
import Table from 'react-bootstrap/Table';
import { FaRegFlag, FaMountain, FaFortAwesome } from 'react-icons/fa';
import {GiCrystalGrowth}from 'react-icons/gi';

import { HexGrid, Layout, Hexagon, Text, GridGenerator } from 'react-hexgrid';
import { apiGetGameRoundHistory, apiGetGameRoundScoreboard } from '../../api';
import { teams as ID_map, SIDE } from '../../config.js';

const POINT_TYPES = {
    UNKNOWN_OBJECT: -2,
    UNKNOWN_EMPTY: -1,
    GRASS: 0,
    WALL: 1,
    FORT: 2,
    CRYPTO_CRYSTAL: 3,
    WEB_CRYSTAL: 4,
    REV_CRYSTAL: 5,
    PWN_CRYSTAL: 6,
    MISC_CRYSTAL: 7,
    FLAG: 100,
}



const PLAYER_COLORS = { "-1": "white", null: "none", 1: "#008000", 2: "#0000FF", 3: "#FF0000", 4: "#00FFFF", 5: "#FF00FF", 6: "#FFFF00", 7: "salmon", 8: "darkorange", 9: "lime", 10: "violet", 11: "pink", 12: "grey", 13: "royalblue", 14: "palegreen", 15: "peru", 16: "orangered" }
let colors = { null: "none" }
let tmp_ID_map = { null: "none" }
let crystal_tiles_seens = {}
let crystal_handled = {}
let deaths = []
let intervalid = undefined;
let tick = 0;


function getTextColor(tile, pov, hex_map) {
    const [q, r, s] = tile["tuple"]
    const point_type = tile["point_type"]
    const owner_ID = tile["owner_ID"]
    const current_value = tile["current_value"]
    let text = undefined
    let color = 'none'
    let icon = null

    if (point_type === POINT_TYPES.FLAG) {
        text = `${current_value}`
        color = colors[owner_ID]
        icon = <FaRegFlag x="-0.5em" y="-0.9em" fontSize="0.1em"/>
    } else if (point_type === POINT_TYPES.GRASS) {
        if (current_value !== 0) {
            text = `${current_value}`
        }
        color = colors[owner_ID]
    } else if (point_type === POINT_TYPES.WALL) {
        // color = 'black'
        icon= <FaMountain x="-0.5em" y="-0.5em" fontSize="0.16em"/>
    } else if (point_type === POINT_TYPES.FORT) {
        text = `${current_value}`
        icon = <FaFortAwesome x="-0.5em" y="-1em" fontSize="0.1em"/>
        color = colors[owner_ID]
    } else if (point_type === POINT_TYPES.CRYPTO_CRYSTAL) {
        text = `${current_value}` 
        color = colors[owner_ID]
        icon = <GiCrystalGrowth style={{ fill: 'green' }} x="-0.5em" y="-1em" fontSize="0.1em"/>
    } else if (point_type === POINT_TYPES.WEB_CRYSTAL) {
        text = `${current_value}`
        color = colors[owner_ID]
        icon = <GiCrystalGrowth style={{ fill: 'yellow' }} x="-0.5em" y="-1em" fontSize="0.1em"/>
    } else if (point_type === POINT_TYPES.REV_CRYSTAL) {
        text = `${current_value}`
        color = colors[owner_ID]
        icon = <GiCrystalGrowth style={{ fill: 'blue' }} x="-0.5em" y="-1em" fontSize="0.1em"/>
    } else if (point_type === POINT_TYPES.PWN_CRYSTAL) {
        text = `${current_value}`
        color = colors[owner_ID]
        icon = <GiCrystalGrowth style={{ fill: 'purple' }} x="-0.5em" y="-1em" fontSize="0.1em"/>
    } else if (point_type === POINT_TYPES.MISC_CRYSTAL) {
        text = `${current_value}`
        color = colors[owner_ID]
        icon = <GiCrystalGrowth style={{ fill: 'brown' }} x="-0.5em" y="-1em" fontSize="0.1em"/>
    } else if (point_type === POINT_TYPES.UNKNOWN_EMPTY) {
        color = 'grey'
        icon = null
    } else if (point_type === POINT_TYPES.UNKNOWN_OBJECT) {
        color = 'purple'
        icon = null
    }

    if ([POINT_TYPES.CRYPTO_CRYSTAL, POINT_TYPES.WEB_CRYSTAL, POINT_TYPES.REV_CRYSTAL, POINT_TYPES.PWN_CRYSTAL, POINT_TYPES.MISC_CRYSTAL].includes(point_type) && owner_ID != null) {
        if (!(owner_ID in crystal_handled)) {
            crystal_handled[owner_ID] = [point_type];
            crystal_tiles_seens[owner_ID] = [];
            crystal_tiles_seens[owner_ID].push([q + 1, r - 1, s].toString());
            crystal_tiles_seens[owner_ID].push([q - 1, r + 1, s].toString());
            crystal_tiles_seens[owner_ID].push([q + 1, r, s - 1].toString());
            crystal_tiles_seens[owner_ID].push([q - 1, r, s + 1].toString());
            crystal_tiles_seens[owner_ID].push([q, r + 1, s - 1].toString());
            crystal_tiles_seens[owner_ID].push([q, r - 1, s + 1].toString());
            crystal_tiles_seens[owner_ID].push([q + 2, r, s - 2].toString());
            crystal_tiles_seens[owner_ID].push([q - 2, r, s + 2].toString());
            crystal_tiles_seens[owner_ID].push([q + 2, r - 2, s].toString());
            crystal_tiles_seens[owner_ID].push([q - 2, r + 2, s].toString());
            crystal_tiles_seens[owner_ID].push([q + 2, r - 1, s - 1].toString());
            crystal_tiles_seens[owner_ID].push([q - 2, r + 1, s + 1].toString());
            crystal_tiles_seens[owner_ID].push([q, r + 2, s - 2].toString());
            crystal_tiles_seens[owner_ID].push([q, r - 2, s + 2].toString());
            crystal_tiles_seens[owner_ID].push([q - 1, r + 2, s - 1].toString());
            crystal_tiles_seens[owner_ID].push([q + 1, r - 2, s + 1].toString());
            crystal_tiles_seens[owner_ID].push([q - 1, r - 1, s + 2].toString());
            crystal_tiles_seens[owner_ID].push([q + 1, r + 1, s - 2].toString());
            crystal_tiles_seens[owner_ID].push([q, r, s].toString());
        }
        if (!(crystal_handled[owner_ID].includes(point_type))) {
            crystal_handled[owner_ID].push(point_type);
            crystal_tiles_seens[owner_ID].push([q + 1, r - 1, s].toString());
            crystal_tiles_seens[owner_ID].push([q - 1, r + 1, s].toString());
            crystal_tiles_seens[owner_ID].push([q + 1, r, s - 1].toString());
            crystal_tiles_seens[owner_ID].push([q - 1, r, s + 1].toString());
            crystal_tiles_seens[owner_ID].push([q, r + 1, s - 1].toString());
            crystal_tiles_seens[owner_ID].push([q, r - 1, s + 1].toString());
            crystal_tiles_seens[owner_ID].push([q + 2, r, s - 2].toString());
            crystal_tiles_seens[owner_ID].push([q - 2, r, s + 2].toString());
            crystal_tiles_seens[owner_ID].push([q + 2, r - 2, s].toString());
            crystal_tiles_seens[owner_ID].push([q - 2, r + 2, s].toString());
            crystal_tiles_seens[owner_ID].push([q + 2, r - 1, s - 1].toString());
            crystal_tiles_seens[owner_ID].push([q - 2, r + 1, s + 1].toString());
            crystal_tiles_seens[owner_ID].push([q, r + 2, s - 2].toString());
            crystal_tiles_seens[owner_ID].push([q, r - 2, s + 2].toString());
            crystal_tiles_seens[owner_ID].push([q - 1, r + 2, s - 1].toString());
            crystal_tiles_seens[owner_ID].push([q + 1, r - 2, s + 1].toString());
            crystal_tiles_seens[owner_ID].push([q - 1, r - 1, s + 2].toString());
            crystal_tiles_seens[owner_ID].push([q + 1, r + 1, s - 2].toString());
            crystal_tiles_seens[owner_ID].push([q, r, s].toString());
        }
    }

    if (pov != -1) {
        if (
            owner_ID != pov &&
            !(
                hex_map[[q + 1, r - 1, s].toString()]?.owner_ID == pov ||
                hex_map[[q - 1, r + 1, s].toString()]?.owner_ID == pov ||
                hex_map[[q + 1, r, s - 1].toString()]?.owner_ID == pov ||
                hex_map[[q - 1, r, s + 1].toString()]?.owner_ID == pov ||
                hex_map[[q, r + 1, s - 1].toString()]?.owner_ID == pov ||
                hex_map[[q, r - 1, s + 1].toString()]?.owner_ID == pov
            ) && (!(parseInt(pov) in crystal_tiles_seens) || !(crystal_tiles_seens[parseInt(pov)].includes([q, r, s].toString())))
        ) {
            // hide_hexagon.show()
            text = ""
            color='grey'
            if (point_type === POINT_TYPES.GRASS || point_type === POINT_TYPES.FLAG) {
                color = 'grey'
                icon = null
            } else if(point_type==POINT_TYPES.FORT || point_type==POINT_TYPES.WALL) {
                color = 'purple'
                icon = null
            }
        } else {
            // hide_hexagon.hide()
        }
    } else {
        // hide_hexagon.hide()
    }


    return [text, color, icon]
}

function SingleHexagon(props) {
    const [text, color, icon] = getTextColor(props.tile, props.pov, props.mapStatus);
    return (
        <Hexagon style={{ fill: color }} stroke={"black"} strokeWidth={0.2} q={props.pos[0]} r={props.pos[1]} s={props.pos[2]} >{icon===null?<></>:icon}<Text style={{ fill: "black" }} strokeWidth={0} y="1em" fontSize="0.07em" fontWeight={"-1"}>{text}</Text></Hexagon>
    )
}

function HexagonalGrid(props) {
    let hexagons = []
    for (const [key, value] of Object.entries(props.mapStatus)) {
        hexagons.push(<SingleHexagon mapStatus={props.mapStatus} pov={props.pov} tile={value} pos={value["tuple"]} key={key} />)
    }

    return (<div>
        <HexGrid style={{ width: "100%", height: "100%" }} viewBox="0 -20 100 120">
            {/* Grid with manually inserted hexagons */}
            <Layout size={{ x: 2, y: 2 }} flat={false} spacing={1} origin={{ x: 50, y: 35 }}>
                {hexagons}
            </Layout>
        </HexGrid>
    </div>);
}

function game_tick(edits, setMapStatus) {
    setMapStatus((oldStatus) => {
        for (const edit of edits) {
            if (edit[1] == POINT_TYPES.FORT && oldStatus[edit[0]]["point_type"] == POINT_TYPES.FLAG) {
                deaths.push(oldStatus[edit[0]]["owner_ID"]);
            }
            oldStatus[edit[0]]["point_type"] = edit[1]
            oldStatus[edit[0]]["owner_ID"] = edit[2]
            oldStatus[edit[0]]["current_value"] = edit[3]
        }
        return oldStatus
    })
}



function LiveStats(props) {
    let players = {}
    function compare(a, b) {
        if (a["value"] < b["value"]) {
            return -1;
        } else if (a["value"] > b["value"]) {
            return 1
        }
        if (a["land"] < b["land"]) {
            return -1
        } else if (a["land"] > b["land"]) {
            return 1;
        }
        return 0;
    }
    for (const [key, hexagon] of Object.entries(props.mapStatus)) {
        if (hexagon["owner_ID"] != null) {
            if (!(hexagon["owner_ID"] in players)) {
                players[hexagon["owner_ID"]] = { "value": hexagon["current_value"], "land": 1, "ID": hexagon["owner_ID"] }
            } else {
                players[hexagon["owner_ID"]]["value"] += hexagon["current_value"]
                players[hexagon["owner_ID"]]["land"] += 1
            }
        }
    }
    let ordered_scoreboard = deaths.map((x) => { return { "ID": x, "value": 0, "land": 0, "name": ID_map[tmp_ID_map[x]] } })
    let tmp_arr = []
    for (const [key, value] of Object.entries(players)) {
        tmp_arr.push(value);
    }
    tmp_arr.sort(compare);
    for (const entry of tmp_arr) {
        ordered_scoreboard.push({ "ID": entry["ID"], "value": entry["value"], "land": entry["land"], "name": ID_map[tmp_ID_map[entry["ID"]]] })
    }
    ordered_scoreboard.reverse()
    let rows = ordered_scoreboard.map((row, i) => <tr key={props.ID + row["ID"].toString()} style={{ backgroundColor: colors[row["ID"]] }}><td>{i + 1}</td><td>{row["name"]}</td><td>{row["value"]}</td><td>{row["land"]}</td></tr>)
    
    return <div style={{ position: "absolute", float: "right", zIndex: "9", "top": 100, "right": 0 }}><Table striped bordered hover>
        <thead>
            <tr style={{ backgroundColor: "grey" }}>
                <th>#</th>
                <th>Name</th>
                <th>Power</th>
                <th>Land</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </Table></div>
}


function GameRenderer(props) {
    let { round, game } = useParams();
    const navigate = useNavigate();
    const [speed, setSpeed] = useState(50);
    const [disabled, setDisabled] = useState(false);
    const hexagons = GridGenerator.hexagon(SIDE);
    const [shownTick, setShownTick] = useState(0);
    const [pov, setPov] = useState(-1);

    window.onpopstate = () => {
        setShownTick(0);
        clearInterval(intervalid);
        tick=0;
        intervalid=undefined;
        crystal_tiles_seens = {}
        crystal_handled = {}
        deaths = []
        
    }

    useEffect(() => {
        async function loadGameData(){
            let round_scoreboard=await apiGetGameRoundScoreboard(game, round);
            let gameHistory = await apiGetGameRoundHistory(game, round);
            if(gameHistory.length<=0){
                navigate("/");
            }
            let hexagonMap = {};
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
        }
        if(!props.externalLoad){
            loadGameData();
        }
    }, [])


    function start_ticking(speed_tick) {
        if (intervalid == undefined) {
            const tick_timeout = Math.floor((10000 / speed_tick))
            intervalid = setInterval(() => {
                tick = tick + 1
                setShownTick(tick)
                if (tick >= props.gameHistory.length) {
                    clearInterval(intervalid);
                    intervalid=undefined;
                    setDisabled(true);
                } else {
                    game_tick(props.gameHistory[tick], props.setMapStatus);
                }
            }, tick_timeout)
        }
    }

    function stop_ticking(event) {

        if (intervalid !== undefined) {
            clearInterval(intervalid)
            intervalid = undefined
        }
    }

    function restart(event) {

        stop_ticking()
        tick = 0;
        setShownTick(tick)
        crystal_handled = [];
        crystal_tiles_seens = [];
        deaths=[];
        game_tick(props.gameHistory[0], props.setMapStatus);
        setDisabled(false);
    }

    function btn_tick(event) {

        tick = tick + 1;
        setShownTick(tick)
        game_tick(props.gameHistory[tick], props.setMapStatus);
        if (tick >= props.gameHistory.length) {
            setDisabled(true);
        }
    }

    function changeSlide(event) {
        setSpeed(event.target.value);
        
        if (intervalid != undefined) {
            stop_ticking();
            start_ticking(event.target.value);
        }
    }

    colors = { null: "none" }
    for (const entry of props.gameScoreboard) {
        colors[entry["ID"]] = PLAYER_COLORS[entry["real_ID"]];
        tmp_ID_map[entry["ID"]] = entry["real_ID"];
    }
    let players = props.gameScoreboard.map((x) => x["ID"])
    players.sort()

    const options = players.map((x) => <option key={"player"+x} value={x} style={{ backgroundColor: colors[x] }}>{ID_map[tmp_ID_map[x]]}</option>)
    const changePov = <select style={{ backgroundColor: colors[pov] }}
        value={pov}
        onChange={(e) => { setPov(e.target.value) }}
    >
        <option value={-1} style={{ backgroundColor: "white" }}>All</option>
        {options}
    </select>

    const buttonRow = <div style={{ height: "5%", width: "100%", alignContent: "center" }}>Current Tick: {shownTick} <Button disabled={disabled} onClick={(e) => { btn_tick(e) }}>Tick</Button> <Button disabled={disabled} onClick={(e) => { start_ticking(speed) }}>Start</Button> <Button disabled={disabled} onClick={(e) => { stop_ticking(e) }}>Stop</Button> <Button onClick={(e) => { restart(e) }}>Restart</Button>{changePov}Speed:<Form.Range style={{ maxWidth: "20%", paddingTop: "15px" }} min={5} max={100} value={speed} onChange={(x) => { changeSlide(x) }} /></div>



    return (<>{buttonRow}<HexagonalGrid pov={pov} mapStatus={props.mapStatus} /><LiveStats mapStatus={props.mapStatus} /></>)
}





export default GameRenderer;