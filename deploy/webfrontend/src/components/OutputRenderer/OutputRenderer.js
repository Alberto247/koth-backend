import { useNavigate, useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { apiGetGameRoundOutput } from '../../api.js'
import {decode as base64_decode} from 'base-64';
import "./OutputRenderer.css"

function OutputRenterer(props) {
    let { round, game } = useParams();
    const navigate = useNavigate();
    const [dockerOutput, setDockerOutput] = useState("");
    props.setTopText("");
    useEffect(() => {
        async function loadDockerOutput(){
            let txt=await apiGetGameRoundOutput(game, round);
            if(txt.length<=0){
                navigate("/");
            }
            setDockerOutput(base64_decode(txt.slice(1, -1)));
        }
        loadDockerOutput();
    }, [])
    const output = dockerOutput.split("\n").map((x)=><>{x}<br></br></>)
    console.log(output)
    console.log(dockerOutput)
    return <pre style={{marginLeft:"100px", maxWidth:"90vw", overflowY:"scroll", overflowX:"scroll", paddingLeft:"10px", marginRight:"100px", marginTop:"50px", maxHeight:"70vh", height:"70vh", border: "solid", backgroundColor: "lightgray", display:"flex"}}><div style={{display:"inline-block", alignSelf:"flex-end"}}>{output}</div></pre>
}

export default OutputRenterer;