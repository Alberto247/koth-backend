import { useNavigate, useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { apiGetGameRoundOutput } from '../../api.js'
import { decode as base64_decode } from 'base-64';
import { LazyLog } from 'react-lazylog';

function OutputRenterer(props) {
    let { round, game } = useParams();
    const navigate = useNavigate();
    const [dockerOutput, setDockerOutput] = useState("");
    props.setTopText("");
    useEffect(() => {
        async function loadDockerOutput() {
            let txt = await apiGetGameRoundOutput(game, round);
            if (txt.length <= 0) {
                navigate("/");
            }
            setDockerOutput(base64_decode(txt.slice(1, -1)));
        }
        loadDockerOutput();
    }, [])
    let output = dockerOutput.split("\n")
    if(dockerOutput.length==0){
        return <></>;
    }
    return <div style={{width:"100%", height: "90vh", padding: "100px"}}><LazyLog text={output.join("\n")} scrollToLine={dockerOutput.length+1} /></div>
}

export default OutputRenterer;