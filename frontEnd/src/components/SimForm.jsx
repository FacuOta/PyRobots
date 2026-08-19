import { API } from "../api";
import React from "react";
import { useState } from "react";
import axios from "axios";
import {
    TextField,
    Button,
    MenuItem,
    FormControl,
    InputLabel,
    Select
  } from "@mui/material";
import styles from "./PartidaForm.module.css";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

  const SimForm = () => {

    const token = sessionStorage.getItem('access_token');
    const navigate = useNavigate();

    const [robotsPlayer, setRobotsPlayer] = useState([]); 

    const [simulacion, setSimulacion] = useState({
        cant_rondas: "",
        robots: { 
                    robot1: "",
                    robot2: "",
                    robot3: "",    
                    robot4: "",
                }
    });

    function dataSim(){
        let data = {"cant_rondas": simulacion.cant_rondas};
        
        let robots = []
        Object.keys(simulacion.robots).forEach((key)=>{
            if(simulacion.robots[key] != ""){
                robots.push(simulacion.robots[key])
            }
        })
        data["robots"] = robots;
        return data;
    }
    
    const url = `${API}/simulacion/`;

    function getRobots(){
        axios({
            method: 'get',
            url: `${API}/get_robots/`,
            headers: { 'Authorization': `Bearer ${token}` },
          }
        )
        .then((response)=> {
            setRobotsPlayer(response.data.robotNames);
        })
    }; 

    const handleSubmit = (e) => {
        e.preventDefault(e);
        
        if(dataSim().robots.length < 2){
            alert("Se requieren al menos 2 bots");
        }else{    
            sessionStorage.setItem("dataSim",JSON.stringify(dataSim()))
            navigate("/simulation");
        }
    }

    useEffect(getRobots,[]);


    const addRobot = (e)=> {
        const newRobots = {...simulacion.robots, [e.target.name]: e.target.value};
        setSimulacion(prevSimulacion => ({...prevSimulacion, robots: newRobots}))
    };

    const changeRounds= (e)=> {
        setSimulacion(prevSimulacion =>({...prevSimulacion, cant_rondas: e.target.value}))
    }

    return(
        <form onSubmit={handleSubmit} className={styles.PartidaForm}>
            <h1 className={styles.titulo}>Crear Simulacion</h1>
            <span className={styles.breaks}></span>


            <FormControl variant="standard" fullWidth>
                <InputLabel id="robot1">Robot 1 </InputLabel>
                <Select
                    name="robot1"
                    id="demo-simple-select"
                    value={simulacion.robots.robot1}
                    label = "Robot 1"
                    onChange={addRobot}
                >
                    <MenuItem value="">
                        <em>None</em>
                    </MenuItem>
                    {robotsPlayer.map((robot)=> (
                        <MenuItem key={robot} value={robot}>{robot}</MenuItem>
                    ))}
                </Select>
            </FormControl>

            <FormControl variant="standard" fullWidth>
                <InputLabel id="robot2">Robot 2 </InputLabel>
                <Select
                    name="robot2"
                    id="demo-simple-select"
                    value={simulacion.robots.robot2}
                    label = "Robot 2"
                    onChange={addRobot}
                >
                    <MenuItem value="">
                        <em>None</em>
                    </MenuItem>
                    {robotsPlayer.map((robot)=> (
                        <MenuItem key={robot} value={robot}>{robot}</MenuItem>
                    ))}
                </Select>
            </FormControl>

            <FormControl variant="standard" fullWidth>
                <InputLabel id="robot3">Robot 3 </InputLabel>
                <Select
                    name="robot3"
                    id="demo-simple-select"
                    value={simulacion.robots.robot3}
                    label = "Robot 3"
                    onChange={addRobot}
                >
                    <MenuItem value="">
                        <em>None</em>
                    </MenuItem>
                    {robotsPlayer.map((robot)=> (
                        <MenuItem key={robot} value={robot}>{robot}</MenuItem>
                    ))}
                </Select>
            </FormControl>

            <FormControl variant="standard" fullWidth>
                <InputLabel id="robot4">Robot 4 </InputLabel>
                <Select
                    name="robot4"
                    id="demo-simple-select"
                    value={simulacion.robots.robot4}
                    label = "Robot 4"
                    onChange={addRobot}
                >
                    <MenuItem value="">
                        <em>None</em>
                    </MenuItem>
                    {robotsPlayer.map((robot)=> (
                        <MenuItem key={robot} value={robot}>{robot}</MenuItem>
                    ))}
                </Select>
            </FormControl>

            
            <TextField
                variant="outlined"
                required
                fullWidth
                label = "Cantidad de rondas"
                name = 'cant_rondas'
                value = {simulacion.cant_rondas}
                id="outlined-basic"
                type="Number"
                InputProps={{ inputProps: { min: 200, max: 10000 } }}
                 onChange={changeRounds}
            />
            <span className={styles.breaks}></span>

            <Button variant="contained" type="submit"> Crear Simulacion </Button>
        </form>
    );
}

export default SimForm;
