import { Select, InputLabel, FormControl, MenuItem } from "@mui/material";
import axios from "axios";
import React, { useEffect, useState } from "react";

const RobotSelect = (props) => {

    const urlListRobots =  "http://127.0.0.1:8000/get_robots/"
    var creador = sessionStorage.getItem('access_token');
    
    const [Robots, SetRobots] = useState([]);

        function getRobots(){
        axios({
            method: 'get',
            url: urlListRobots,
            headers: { 'Authorization': `Bearer ${creador}` }
        })
        .then(function(response){
            SetRobots(response.data.robotNames)
            console.log("cambiando robots");
        })
        .catch(() => {
            console.log('Ocurrio un error consiguiendo la lista de robots')
        });
    }

    useEffect(getRobots,[]);
    
    return(
            <FormControl fullWidth margin="normal" sx={{ boxShadow: 1 }}>
                    <InputLabel id="title">Robots</InputLabel>
                    <Select
                        labelId="title"
                        label= "Robots"
                        defaultValue=""
                        value = {props.inputValue}
                        onChange={(event) => props.SetValue(event.target.value)}
                        sx ={{ bgcolor: 'white'}}
                    >
                    {(Robots === []) ? <MenuItem key={99999} value={"None"}>No hay robots disponibles</MenuItem> : Robots.map((name, index) => <MenuItem key={index} value={name}>{name}</MenuItem>)}
                    </Select>
            </FormControl>
    );
}

export default RobotSelect;
