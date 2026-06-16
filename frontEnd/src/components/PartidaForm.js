import React from "react";
import { useState } from "react";
import axios from "axios";
import {
    TextField,
    Button,
  } from "@mui/material";
  import sleep from './sleep.js'
  import { useNavigate } from "react-router-dom";
  import styles from "./PartidaForm.module.css";

  const PartidaForm = () => {

    var creador = sessionStorage.getItem('access_token');

    const [partida, setNPartida] = useState({
        nombre_partida: "",
        cant_max_players: "",
        cant_juegos: "",
        cant_rondas: "",
        creador: creador,
        password: ""
    });
    
    const navigate = useNavigate();

    const url = "http://127.0.0.1:8000/crear_partida/";
    var bodyFormData = new FormData();

    bodyFormData.append("nombre_partida", partida.nombre_partida);
    bodyFormData.append("cant_max_players", partida.cant_max_players);
    bodyFormData.append("cant_juegos", partida.cant_juegos);
    bodyFormData.append("cant_rondas", partida.cant_rondas);
    if (partida.password !== '') {
        bodyFormData.append("password", partida.password);
    }
    
    const handleChange = (e) => {
        setNPartida({...partida, [e.target.name]: e.target.value})
    }

    const handleSubmit = (e) => {
        e.preventDefault(e);
        console.log(partida);

        axios({
            method: 'post',
            url: url,
            headers: {'Authorization': `Bearer ${creador}`},
            data: bodyFormData
          })
          .then(function (response){
            alert("Se creo la partida con exito");
            console.log(response);
            sleep(1500).then(() => {navigate('/listgame')}) //TODO: redireccionar al lobby
          })
          .catch(function(response){
            alert("No se puedo crear la partida, intentelo de nuevo mas tarde");
            console.log(response)
          });

    }    
    return(
        <form onSubmit={handleSubmit} className={styles.PartidaForm}>
            <h1 className={styles.titulo}>Crear Partida</h1>
            <span className={styles.breaks}></span>

            <TextField
                label= "Nombre de partida"
                name = 'nombre_partida'
                value = {partida.nombre_partida}
                variant="outlined"
                required
                fullWidth
                type = "Text"
                id="outlined-basic"
                onChange={handleChange}
            />
            <span className={styles.breaks}></span>

            <TextField
                label= "Cantidad maxima de jugadores"
                name = 'cant_max_players'
                value = {partida.cant_max_players}
                variant="outlined"
                required
                fullWidth
                type="Number"
                id="outlined-basic"
                InputProps={{ inputProps: { min: 2, max: 4 } }}
                onChange={handleChange}
            />
            <span className={styles.breaks}></span>

            <TextField
                variant="outlined"
                required
                fullWidth
                label ="Cantidad de juegos"
                name = 'cant_juegos'
                value = {partida.cant_juegos}
                id="outlined-basic"
                type="Number"
                InputProps={{ inputProps: { min: 1, max: 200 } }}
                onChange={handleChange}
            />
            <span className={styles.breaks}></span>

            <TextField
                variant="outlined"
                required
                fullWidth
                label = "Cantidad de rondas"
                name = 'cant_rondas'
                value = {partida.cant_rondas}
                id="outlined-basic"
                type="Number"
                InputProps={{ inputProps: { min: 1, max: 10000 } }}
                onChange={handleChange}
            />
            <span className={styles.breaks}></span>

            <TextField
                label = "Contraseña"
                name = 'password'
                value = {partida.password}
                id="outlined-basic"
                variant="outlined"
                type= "Password"
                color= "secondary"
                fullWidth
                onChange={handleChange}
            >

            </TextField>
            <span className={styles.breaks}></span>

            <Button variant="contained" type="submit"> Crear Partida </Button>
        </form>
    );
}

export default PartidaForm;
