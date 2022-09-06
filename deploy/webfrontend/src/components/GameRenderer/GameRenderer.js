import { useNavigate } from 'react-router-dom';
import {useRef, useState, useEffect} from 'react';
import { Row, Button, Collapse, Card, OverlayTrigger, Popover } from "react-bootstrap";
import Form from 'react-bootstrap/Form'

import { HexGrid, Layout, Hexagon, Text, Pattern, Path, Hex, GridGenerator } from 'react-hexgrid';


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



const PLAYER_COLORS = { null: "none", 1: "#008000", 2: "#0000FF", 3: "#FF0000", 4: "#00FFFF", 5: "#FF00FF", 6: "#FFFF00", 7: "salmon", 8: "darkorange", 9: "lime", 10: "violet", 11: "pink", 12: "grey", 13: "royalblue", 14: "palegreen", 15: "peru", 16: "orangered" }
const ID_map = { 1: "team1", 2: "team2", 3: "team3", 4: "team4", 5: "team5", 6: "team6", 7: "team7", 8: "team8", 9: "team9", 10: "team10", 11: "team11", 12: "team12", 13: "team13", 14: "team14", 15: "team15", 16: "team16" }
let colors={null:"none"}
let hexagon_map = {}
let tick = 0;
let intervalid=undefined;

// function edit_hexagon(hex) {

//     const q = hex.q
//     const r = hex.r
//     const s = hex.s
//     const point_type = hex.point_type
//     const owner_ID = hex.owner_ID
//     const current_value = hex.current_value

//     let text = undefined
//     let color = 'none'

//     if (point_type === POINT_TYPES.FLAG) {
//         text = `S ${current_value}`
//         color = PLAYER_COLORS[owner_ID]
//     } else if (point_type === POINT_TYPES.GRASS) {
//         if (current_value !== 0) {
//             text = `${current_value}`
//         }
//         color = PLAYER_COLORS[owner_ID]
//     } else if (point_type === POINT_TYPES.WALL) {
//         color = 'black'
//     } else if (point_type === POINT_TYPES.FORT) {
//         text = `H ${current_value}`
//         color = PLAYER_COLORS[owner_ID]
//     } else if (point_type === POINT_TYPES.CRYPTO_CRYSTAL) {
//         text = `CC ${current_value}`
//         color = 'green'
//     } else if (point_type === POINT_TYPES.WEB_CRYSTAL) {
//         text = `WC ${current_value}`
//         color = 'yellow'
//     } else if (point_type === POINT_TYPES.REV_CRYSTAL) {
//         text = `RC ${current_value}`
//         color = 'blue'
//     } else if (point_type === POINT_TYPES.PWN_CRYSTAL) {
//         text = `PC ${current_value}`
//         color = 'purple'
//     } else if (point_type === POINT_TYPES.MISC_CRYSTAL) {
//         text = `MC ${current_value}`
//         color = 'brown'
//     } else if (point_type === POINT_TYPES.UNKNOWN_EMPTY) {
//         color = 'grey'
//     } else if (point_type === POINT_TYPES.UNKNOWN_OBJECT) {
//         color = 'purple'
//     }

//     // const hide_hexagon = hide_hexagon_map[[hex.q, hex.r, hex.s]]
//     if (player_pov !== undefined) {
//         if (
//             owner_ID !== player_pov &&
//             !(
//                 hex_map[[q + 1, r - 1, s]]?.owner_ID === player_pov ||
//                 hex_map[[q - 1, r + 1, s]]?.owner_ID === player_pov ||
//                 hex_map[[q + 1, r, s - 1]]?.owner_ID === player_pov ||
//                 hex_map[[q - 1, r, s + 1]]?.owner_ID === player_pov ||
//                 hex_map[[q, r + 1, s - 1]]?.owner_ID === player_pov ||
//                 hex_map[[q, r - 1, s + 1]]?.owner_ID === player_pov
//             )
//         ) {
//             // hide_hexagon.show()
//             text = undefined
//             if (point_type === POINT_TYPES.GRASS || point_type === POINT_TYPES.FLAG) {
//                 color = 'grey'
//             } else {
//                 color = 'purple'
//             }
//         } else {
//             // hide_hexagon.hide()
//         }
//     } else {
//         // hide_hexagon.hide()
//     }


//     const hexagon = hexagon_map[[hex.q, hex.r, hex.s]]

//     if (hexagon.fill() !== color) {
//         hexagon.fill(color)
//     }


//     if (text) {
//         const label = text_labels[[hex.q, hex.r, hex.s]]
//         const { cx, cy } = hexagon.rbox()
//         const p = DRAW.point(cx, cy)
//         if (label) {
//             label.show()
//             if (label.text() !== text) {
//                 label.text(text).center(p.x, p.y)
//             }
//         } else {
//             let t = TEXT_GROUP.text(text).font({ size: 40 }).center(p.x, p.y)
//             text_labels[[hex.q, hex.r, hex.s]] = t
//         }
//     } else {
//         const label = text_labels[[hex.q, hex.r, hex.s]]
//         if (label) {
//             label.hide()
//         }
//     }
// }

function getTextColor(tile){
    const point_type = tile["point_type"]
    const owner_ID = tile["owner_ID"]
    const current_value = tile["current_value"]
    let text = undefined
    let color = 'none'

    if (point_type === POINT_TYPES.FLAG) {
        text = `S ${current_value}`
        color = colors[owner_ID]
    } else if (point_type === POINT_TYPES.GRASS) {
        if (current_value !== 0) {
            text = `${current_value}`
        }
        color = colors[owner_ID]
    } else if (point_type === POINT_TYPES.WALL) {
        color = 'black'
    } else if (point_type === POINT_TYPES.FORT) {
        text = `H ${current_value}`
        color = colors[owner_ID]
    } else if (point_type === POINT_TYPES.CRYPTO_CRYSTAL) {
        text = `CC ${current_value}`
        color = 'green'
    } else if (point_type === POINT_TYPES.WEB_CRYSTAL) {
        text = `WC ${current_value}`
        color = 'yellow'
    } else if (point_type === POINT_TYPES.REV_CRYSTAL) {
        text = `RC ${current_value}`
        color = 'blue'
    } else if (point_type === POINT_TYPES.PWN_CRYSTAL) {
        text = `PC ${current_value}`
        color = 'purple'
    } else if (point_type === POINT_TYPES.MISC_CRYSTAL) {
        text = `MC ${current_value}`
        color = 'brown'
    } else if (point_type === POINT_TYPES.UNKNOWN_EMPTY) {
        color = 'grey'
    } else if (point_type === POINT_TYPES.UNKNOWN_OBJECT) {
        color = 'purple'
    }
    return [text, color]
}

function SingleHexagon(props){
    const [text, color]=getTextColor(props.tile);
    return (
        <Hexagon style={{fill:color}} stroke={"black"} strokeWidth={0.2} q={props.pos[0]} r={props.pos[1]} s={props.pos[2]} ><Text style={{fill:"black"}} strokeWidth={0} fontSize="0.07em" fontWeight={"-1"}>{text}</Text></Hexagon>
    )
}

function HexagonalGrid(props){
    let hexagons=[]
    for (const [key, value] of Object.entries(props.mapStatus)) {
        hexagons.push(<SingleHexagon tile={value} pos={value["tuple"]} key={key}/>)
    }

    return (<div>
        <HexGrid style={{width:"100%", height:"100%"}} viewBox="0 0 100 100">
          {/* Grid with manually inserted hexagons */}
          <Layout size={{ x: 2, y:2 }} flat={false} spacing={1} origin={{ x: 50, y: 35 }}>
            {hexagons}
          </Layout>
        </HexGrid>
      </div>);
}

function game_tick(edits, setMapStatus){
    setMapStatus((oldStatus)=>{
        for(const edit of edits){
            oldStatus[edit[0]]["point_type"]=edit[1]
            oldStatus[edit[0]]["owner_ID"]=edit[2]
            oldStatus[edit[0]]["current_value"]=edit[3]
        }
        return oldStatus
    })
}

function LiveStats(props){
    let players={}
    for(const hexagon of props.mapStatus){
        if(hexagon["owner_ID"!=null]){
            if(!(hexagon["owner_ID"] in players)){
                players[hexagon["owner_ID"]]={"value":hexagon["current_value"], "land":1}
            }else{
                players[hexagon["owner_ID"]]["value"]+=hexagon["current_value"]
                players[hexagon["owner_ID"]]["land"]+=1
            }
        }
    }
    let ordered_scoreboard=[]
    for (const [key, value] of Object.entries(players)) {
        
    }
}


function GameRenderer(props){
    const navigate = useNavigate();
    const [speed, setSpeed] = useState(5);
    const [disabled, setDisabled] = useState(false);
    const hexagons=GridGenerator.hexagon(10);
    const [shownTick, setShownTick] = useState(0)
    let hexagonMap={};
    for(const hexagon of hexagons){
        hexagonMap[[hexagon.q, hexagon.r, hexagon.s]]={"hex":hexagon}
    }
    for(const hexagon of props.gameHistory[0]){
        let tile=hexagonMap[hexagon[0]]
        tile["point_type"]=hexagon[1]
        tile["owner_ID"]=hexagon[2]
        tile["current_value"]=hexagon[3]
        tile["tuple"]=hexagon[0]
        hexagonMap[hexagon[0]]=tile
    }

    const [mapStatus, setMapStatus] = useState(hexagonMap);
    

    let player_pov = undefined
    

    useEffect(()=>{
        if(props.gameHistory.length===0){
            navigate("/");
        }
    }, [])
    

    function start_ticking(){
        if(intervalid==undefined){
            const tick_timeout = Math.floor((10000 / speed))
            intervalid = setInterval(() => {
                console.log("ticking "+tick)
                tick=tick+1
                setShownTick(tick)
                if (tick >= props.gameHistory.length) {
                    clearInterval(intervalid);
                } else {
                    game_tick(props.gameHistory[tick], setMapStatus);
                }
            }, tick_timeout)
        }
    }

    function stop_ticking(event){

        if (intervalid !== undefined) {
            clearInterval(intervalid)
            intervalid = undefined
        }
    }

    function restart(event){

        stop_ticking()
        tick=0;
        setShownTick(tick)
        game_tick(props.gameHistory[0], setMapStatus);
    }

    function btn_tick(event){

        tick=tick+1;
        setShownTick(tick)
        game_tick(props.gameHistory[tick], setMapStatus);
    }
    
    colors={null:"none"}
    for(const entry of props.currentGameScoreboard){
        colors[entry["ID"]]=PLAYER_COLORS[entry["real_ID"]];
    }

    const buttonRow=<div style={{height:"5%", width:"100%", alignContent:"center"}}>Current Tick: {tick} <Button disabled={disabled} onClick={(e)=>{btn_tick(e)}}>Tick</Button> <Button disabled={disabled} onClick={(e)=>{start_ticking(e)}}>Start</Button> <Button disabled={disabled} onClick={(e)=>{stop_ticking(e)}}>Stop</Button> <Button disabled={disabled} onClick={(e)=>{restart(e)}}>Restart</Button>Speed:<Form.Range style={{maxWidth:"20%", paddingTop:"15px"}} min={5} max={100} value={speed} onChange={(x)=>{setSpeed(x.target.value)}} /></div>

    


    
    return (<>{buttonRow}<HexagonalGrid mapStatus={mapStatus}/></>)
}





export default GameRenderer;