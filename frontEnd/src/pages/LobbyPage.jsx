import { API } from "../api";
import React, { useState, useEffect } from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import axios from "axios";

import { useNavigate } from "react-router-dom";

import RobotSelect from "../components/robotSelect.js";

const LobbyPage = () => {
  // Sin token no se puede ver la pagina
  const token = sessionStorage.getItem("access_token");
  const wsURL = sessionStorage.getItem("websocket");
  const match_id = sessionStorage.getItem("id_partida");

  // Para tener un registros de los usuarios
  const [cantusers, setCantusers] = useState(1);
  const [usernames, setUsernames] = useState([]);

  // Auxiliares
  const [creador, setCreador] = useState(false);
  const [nombrePartida, setNombrePartida] = useState("");
  const [robot, setRobot] = useState("");
  const [partidaIniciada, setPartidaIniciada] = useState(false);
  const [finalizada, setFinalizada] = useState(false);

  const navigate = useNavigate();

  // Creo el websocket y como funcionan sus callbacks
  function conexionWS() {
    try {
      const ws = new WebSocket(wsURL);
      // Inicia la conexion
      ws.onopen = (e) => {
        obtenerDatosGenerales();
      };
      // El servidor envia mensajes
      ws.onmessage = (e) => {
        try {
          var res = JSON.parse(e.data);
          if (res.event === "Union" && cantusers <= 4 && !partidaIniciada) {
            setUsernames([...usernames, res.nombre_usuario]);
            setCantusers(cantusers + 1);
          } else if (
            res.event === "Abandona" &&
            2 <= cantusers &&
            !partidaIniciada
          ) {
            var tmp = usernames.filter((user) => user !== res.nombre_usuario);
            setUsernames(tmp);
          } else if (res.event === "Inicio") {
            setPartidaIniciada(true);
          } else if (res.event === "Finalizado") {
            setFinalizada(true);
            mostrarResultados();
          } else {
            console.log(e);
          }
          obtenerDatosGenerales();
        } catch (error) {
          console.log("Error al unirse");
        }
      };
      // El servidor cerro la conexion
      ws.close = (e) => {
        onClose(e);
      };
      // Aviso de error del servidor
      ws.error = (e) => {
        console.log(e);
      };
    } catch (error) {
      console.log(error);
    }
  }

  // Datos de la partida para cada usuario
  function obtenerDatosGenerales() {
    let urlpartida = `${API}/partida/` + match_id;
    axios({
      method: "get",
      url: urlpartida,
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((response) => {
        setUsernames(response.data.participantes);
        setCreador(response.data.es_creador);
        setCantusers(response.data.jugadores_participando);
        setNombrePartida(response.data.nombre_partida);
        setPartidaIniciada(response.data.en_progreso);
        setFinalizada(response.data.termino);
      })
      .catch(() => {
        console.log("Error al obtener datos");
      });
  }

  // Abandonar la partida actual (No permitido para creador de la misma)
  function abandonarLobby() {
    try {
      if (!creador) {
        setCantusers(cantusers - 1); // Usuario abandona la partida
        // Creo el paquete a enviar
        let bodyFormData = new FormData();
        bodyFormData.append("match_name", nombrePartida);
        bodyFormData.append("current_user", token);
        axios({
          method: "put",
          url: `${API}/partida/abandonar/`,
          data: bodyFormData,
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data",
            "Access-Control-Allow-Origin": "*",
          },
        })
          .then((response) => {
            navigate("/listgame");
          })
          .catch(() => {
            console.log("Error al pasar datos para abandonar");
          });
      }
    } catch (error) {
      console.log("No se pudo abandonar");
    }
  }

  // El usuario creador puede iniciar su partida
  function iniciarPartida() {
    try {
      if (creador && cantusers >= 2 && robot) {
        let bodyFormData = new FormData();
        bodyFormData.append("current_user", token);
        bodyFormData.append("match_name", nombrePartida);
        bodyFormData.append("creator_robot", robot);
        axios({
          method: "put",
          url: `${API}/partida/iniciar_partida`,
          data: bodyFormData,
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data",
            "Access-Control-Allow-Origin": "*"
          },
        })
          .then((response) => {
            console.log(response);
          })
          .catch(() => {
            console.log("Error al pasar datos para iniciar la partida");
          });
      }
    } catch (error) {
      console.log("No se pudo iniciar la partida");
    }
  }

  // Ir a la pagina de ver resultados
  function mostrarResultados() {
    let urlresults = "/results/" + match_id;
    navigate(urlresults);
  }

  // Intentamos reconectarnos al servidor caido
  function onClose(e) {
    setTimeout(() => {
      conexionWS(wsURL);
    }, 5000);
  }

  useEffect(conexionWS, []);

  return (
    <div>
      <div style={{ textAlign: "center", marginBottom: "15px" }}>
        <h1 style={{ color: "white", fontSize: "50px", margin: "0" }}>
          {(!partidaIniciada && !finalizada) && "Esperando que se de inicio a la partida..."}
          {(partidaIniciada && !finalizada) && "Partida en progreso..."}
          {finalizada && "Partida finalizada"}
        </h1>
      </div>
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          marginBottom: "50px",
          "& > :not(style)": {
            m: 4,
            width: 345,
            height: 100,
          },
        }}
      >
        <div
          style={{
            background: "#2A9D8F",
            borderRadius: "20px",
            border: "4px solid white",
            textAlign: "center",
          }}
        >
          <h2 style={{ color: "white", margin: "0" }}>
            {usernames[0] !== undefined && usernames[0]}
            {usernames[0] === undefined && "Esperando jugador..."}
          </h2>
        </div>
        <div
          style={{
            background: "#8ecae6",
            borderRadius: "20px",
            border: "4px solid white",
            textAlign: "center",
          }}
        >
          <h2 style={{ color: "white", margin: "0" }}>
            {usernames[1] !== undefined && usernames[1]}
            {usernames[1] === undefined && "Esperando jugador..."}
          </h2>
        </div>
        <div
          style={{
            background: "#219ebc",
            borderRadius: "20px",
            border: "4px solid white",
            textAlign: "center",
          }}
        >
          <h2 style={{ color: "white", margin: "0" }}>
            {usernames[2] !== undefined && usernames[2]}
            {usernames[2] === undefined && "Esperando jugador..."}
          </h2>
        </div>
        <div
          style={{
            background: "#577590",
            borderRadius: "20px",
            border: "4px solid white",
            textAlign: "center",
          }}
        >
          <h2 style={{ color: "white", margin: "0" }}>
            {usernames[3] !== undefined && usernames[3]}
            {usernames[3] === undefined && "Esperando jugador..."}
          </h2>
        </div>
      </Box>
      {!partidaIniciada && !creador && !finalizada  && (
        <Button
          variant="contained"
          color="warning"
          style={{
            width: "100%",
            borderRadius: "15px",
            border: "3px solid white",
          }}
          onClick={abandonarLobby}
        >
          Abandonar partida
        </Button>
      )}
      {!partidaIniciada && creador && !finalizada && (
        <h2 style={{ color: "white", margin: "0" }}>
          Para iniciar la partida, seleccione su robot:
        </h2>
      )}
      {!partidaIniciada && creador && !finalizada && (
        <RobotSelect inputValue={robot} SetValue={setRobot} />
      )}
      {!partidaIniciada && creador && !finalizada && (
        <Button
          variant="contained"
          color="success"
          style={{
            width: "100%",
            borderRadius: "15px",
            border: "3px solid white",
          }}
          onClick={iniciarPartida}
        >
          Iniciar partida
        </Button>
      )}
      <a href="/listgame" style={{ textDecoration: "none" }}>
        <Button
          variant="contained"
          color="secondary"
          style={{
            width: "100%",
            borderRadius: "15px",
            border: "3px solid white",
          }}
        >
          Volver a lista de partidas
        </Button>
      </a>
    </div>
  );
};

export default LobbyPage;