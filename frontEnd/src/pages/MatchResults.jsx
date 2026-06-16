import Button from '@mui/material/Button';
import axios from "axios";
import { useEffect } from 'react';
import { useParams } from "react-router-dom";
import { useState } from 'react';
import ConfettiGenerator from 'confetti-js';

import styles from "./MatchResults.module.css";


function MatchResults() {

    const token = sessionStorage.getItem("access_token");

    const {id} = useParams();

    const [screenMsg,setScreenMsg] = 
        useState(<p data-testid="error">No hay info para mostrar</p>);

    const [enableConfetti,setEnableConfetti] = useState(false);


    const getResults = () =>{
        axios({
            method: "get",
            url: `http://127.0.0.1:8000/partida/${id}/resultados`,
            headers: { 'Authorization': `Bearer ${token}` }
        })
            .then((response) => {
                if("winnerRobot" in response.data){
                    if (response.data.winnerRobot !== ""){
                        setScreenMsg(<div>
                                        <p> El ganador es el robot </p>
                                        <p className={styles.winner}> 
                                            {response.data.winnerRobot} 
                                        </p>
                                        <p>del usuario</p>
                                        <p className={styles.winner}> 
                                            {response.data.winnerUser} 
                                        </p>
                                    </div>
                                    )
                        setEnableConfetti(true);
                    } else{
                        setScreenMsg(
                            <div>
                                <p>Hubo un empate!</p>
                            </div>
                        );
                        setEnableConfetti(false);
                    }
                } else if ("detail" in response.data){
                    setScreenMsg(<p>{`${response.data.detail}`}</p>);
                    setEnableConfetti(false);
                }
            })
        }
    
    useEffect(getResults,[]);

    useEffect(()=>{
        if(enableConfetti){
            const confettiSettings = {"target":"confetti-holder","max":"200","size":"1","animate":true,
                                    "props":["circle","square","triangle","line"],
                                    "colors":[[165,104,246],[230,61,135],[0,199,228],[253,214,126]],
                                    "clock":"25","rotate":true,"width":"1366","height":"622",
                                    "start_from_edge":false,"respawn":true};
            const confetti = new ConfettiGenerator(confettiSettings);
            confetti.render();
            
            return () => confetti.clear();
        }
    }, [enableConfetti])

    

    return (
        <div className={styles.winnerPage} id="winnerPage">

            {enableConfetti && <canvas data-testid="canvas" className={styles.confettiholder} id='confetti-holder'></canvas>}
            <div className={styles.winnerDiv} id="winnerDiv">
                <div data-testid="msg" id="winnerMsg">{screenMsg}</div>
                <Button data-testid="btn" variant="contained">
                    <a className={styles.link} href="/listgame">Volver</a>
                </Button>
            </div>
        </div>
        
    );
}

export default MatchResults;
