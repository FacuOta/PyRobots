import { API } from "../api";
import React, { useEffect, useState } from "react";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import RefreshIcon from '@mui/icons-material/Refresh';
import LockIcon from '@mui/icons-material/Lock';
import AddIcon from '@mui/icons-material/Add';
import CancelIcon from '@mui/icons-material/Cancel';
import TaskAltIcon from '@mui/icons-material/TaskAlt';
import PlayForWorkIcon from '@mui/icons-material/PlayForWorkTwoTone';
import { Box, Collapse, TextField, Alert, IconButton, Stack } from "@mui/material";
import axios from "axios";
import styles from "./MatchsList.module.css"
import RobotSelect from "./robotSelect.js"
import { useNavigate } from "react-router-dom";
import sleep from './sleep.js'
import FilterPartidas from './filterPartidas'

function MatchsList() {

  const [matchs, setMatchs] = React.useState([]);
  const [Open, setOpen] = React.useState("");
  const [SelectedRobot, SetSelectedRobot] = React.useState("");
  const [Password, setPassword] = useState("");
  const [alert, setAlert] = useState(false);
  const [alertContent, setAlertContent] = useState("");
  const [filter, setFilter] = useState("noTerminadas")
  
  let bodyFormData = new FormData()
  const navigate = useNavigate();

  const headersStyle = {fontWeight:'bold'}
  const urlUnirse = `${API}/partida/unirse/`
  var urlInfoPartida = `${API}/partida/`
  var urlResultado = '/results/';

  function handleCreate() {
    window.location.replace('/creategame')
  }

  const token = sessionStorage.getItem("access_token");

  function getMatchs() {
    axios({
      method: 'get',
      url: filter === "noTerminadas" ?
        `${API}/partida/list` :
        `${API}/partida/list_ended`
      ,
      headers: { 'Authorization': `Bearer ${token}` },
    })
      .then((response) => {
        let sortedMatchsByDate = response.data.partidas;
        sortedMatchsByDate.sort((a, b) => new Date(a.fecha_creacion) < new Date(b.fecha_creacion));
        setMatchs(sortedMatchsByDate);
      })
      .catch(() => {
        console.log('An error has ocurred')
      })
  }

  function handleRowClick(index){
    if (Open === index) {
      setOpen("")
    } else {
      setOpen(index)
    }
  }

  function handlePassword(e){
    setPassword(e.target.value)
  }

  function joinMatch(index){
    var match = matchs[index]

    bodyFormData.append("match_name", match.nombre_partida);
    bodyFormData.append("robot_name", SelectedRobot);
    if(match.es_privada){
      bodyFormData.append("password", Password);
    }

    axios({
      method: 'post',
      url: urlUnirse,
      headers: { 'Authorization': `Bearer ${token}` },
      data: bodyFormData
    })
    .then(response => {
      const webskt = response.data.websocket;
      const partida_id = match.id_partida;
      sessionStorage.setItem("websocket", webskt);
      sessionStorage.setItem("id_partida", partida_id);
      sleep(1000).then(navigate('/lobby'));
    })
    .catch((err) => {
      console.log(err)
      setAlertContent(err.response.data.detail);
      setAlert(true);
    })
  }

  function goToLobby(index){
    var match = matchs[index];
    var id_partida = match.id_partida;
    var ws = "";
    urlInfoPartida = urlInfoPartida + id_partida;
    var datos = new FormData();

    datos.append("match_id", id_partida);

    console.log(urlInfoPartida);

    axios({
      method: 'get',
      url: urlInfoPartida,
      headers: { 'Authorization': `Bearer ${token}` },
      data: datos
    })
    .then(response => {
      ws = response.data.websocket
      sessionStorage.setItem("websocket", ws);
      sessionStorage.setItem("id_partida", id_partida);
      sleep(1000).then(navigate('/lobby'));
    })
    .catch((err) =>{
      console.log(err)
      setAlertContent(err.response.data.detail);
      setAlert(true);
    })
  }

  useEffect(getMatchs, []);
  useEffect(() => {SetSelectedRobot("")} ,[Open]); // Cuando me muevo de un registro de partida a otro borro la seleccion de robot
  useEffect(getMatchs,[filter]); // Cuando se cambia el filtro se fetchea nuevas matches
  useEffect(() => {setOpen("")} , [filter]); // Cierra registro de partida en caso de cambio de filtro

  return (
    <div className={styles.list}>
      {alert ?
            <Alert
                sx={{ borderRadius: 2,
                     width: 1/4,
                     left: 5,
                     m:2,
                     position: "absolute",
                     top: "4px",
                     left: "4px" }}
                action={
                    <IconButton
                      aria-label="close"
                      color="inherit"
                      size="small"
                      onClick={() => {setAlert(false);}}
                    >
                <CloseIcon fontSize="inherit" />
                </IconButton> }
                severity = "error"
                >
            {alertContent}
            </Alert> : <></>
      }
      <Stack direction="row">
        <Button
          variant="contained"
          sx = {{mb: 1, right: 0}}
          endIcon={<RefreshIcon />}
          onClick={getMatchs}
        >
          Actualizar
        </Button>
        <Button
          variant="contained"
          sx={{mb: 1, ml:3}}
          endIcon={<AddIcon />}
          onClick={handleCreate}
        >
          Crear Partida
        </Button>
        <FilterPartidas setFiltro={setFilter} filtro={filter} />
      </Stack>

      <TableContainer className={styles.table} component={Paper}>
        <Table sx={{ minWidth: 650 }} size="small" aria-label="a dense table">
          <TableHead className= {styles.tableHead}>
            <TableRow>
              <TableCell padding="checkbox"><LockIcon fontSize="small" /></TableCell>
              <TableCell sx={headersStyle}>Partida</TableCell>
              <TableCell align="right" sx={headersStyle}> Jugadores</TableCell>
              <TableCell align="right" sx={headersStyle}> Juegos(Rondas)</TableCell>
              <TableCell align="right" sx={headersStyle}> Estado</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {matchs.length === 0 &&
              <TableRow
              sx={{ '&:last-child td, &:last-child th': { border: 0 }}}
            ><TableCell></TableCell>
            <TableCell className={styles.missingText}>No se encontraron partidas iniciadas</TableCell>
            </TableRow>
            }
            {
            matchs.length > 0 && matchs.map((match, index) => (
              <React.Fragment>
                <TableRow
                  key={index}
                  sx={{ borderBottom: 0, bgcolor:  index === Open ? 'rgb(240, 240, 240)': "" }}
                  onClick = {() => {handleRowClick(index)}}
                >
                  <TableCell>{match.es_privada ? <LockIcon /> : ""}</TableCell>
                  <TableCell component="th" scope="match">
                    {match.nombre_partida}
                  </TableCell>
                  <TableCell align="right" >{match.jugadores_participando} / {match.numero_maximo_jugadores}</TableCell>
                  <TableCell align="right">{match.numero_juegos} ({match.numero_rondas})</TableCell>
                  <TableCell align="right">
                    {match.participa ? <TaskAltIcon color="success"/> : 
                          match.jugadores_participando === match.numero_maximo_jugadores ? <CancelIcon color="error"/> : <PlayForWorkIcon color="#FFFF"/>}
                  </TableCell>
                </TableRow>
                
                 <TableRow sx={{ padding: 0, boxShadow: 0, border: 0 , borderRadius: 1, bgcolor: index === Open? 'rgb(240, 240, 240)': ''}} >
                  <TableCell colSpan={5} sx={{padding: 0, boxShadow: 2}}>
                    <Collapse in={index === Open} timeout = "auto" unmountOnExit>
                      { filter === "noTerminadas" ?
                      <Box sx={{margin:2, borderRadius: 1 }}>
                        <RobotSelect inputValue={SelectedRobot} SetValue={SetSelectedRobot}/>
                        {match.es_privada? <TextField
                            label = "Contraseña"
                            name = 'password'
                            value={Password}
                            id="outlined-basic"
                            variant="outlined"
                            type= "Password"
                            color= "secondary"
                            required
                            onChange={handlePassword}
                            fullWidth
                            sx ={{marginBottom: 1, bgcolor: "white"}}
                        />: <></>}
                        <Button key={match.nombre_partida} onClick={() => {joinMatch(index)}} disabled={SelectedRobot === "" || match.es_privada? Password === "" : false } variant="contained" >Unirse a partida</Button>
                        <Button onClick={() => {goToLobby(index)}} sx={{m:1}} disabled = { !match.participa }>Ir al lobby</Button>
                      </Box>
                      :
                      <Box sx={{margin:2, borderRadius: 1 }}>
                        <Button onClick={() => {navigate((urlResultado + match.id_partida))}} sx={{m:1}} variant= "contained">Ver resultado</Button>
                      </Box>}
                    </Collapse>
                  </TableCell>
                </TableRow>
              </React.Fragment>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  )
}

export default MatchsList;