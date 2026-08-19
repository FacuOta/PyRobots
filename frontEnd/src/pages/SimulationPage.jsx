import { API } from "../api";
import Board from "../components/Board";
import React, { useReducer, useState } from "react";
import useInterval from "../components/hooks/useInterval.js";
import styles from "../components/Board.module.css";
import { BOT_ONE, BOT_TWO, BOT_THREE, BOT_FOUR } from "../components/const";
import Button from "@mui/material/Button";
import qs from "qs";
import axios from "axios";

const SimulationPage = () => {
  const token = sessionStorage.getItem("access_token"); // Permiso para mirar la pagina
  const simData = JSON.parse(sessionStorage.getItem("dataSim")); // Datos de la simulacion

  // Arreglo que almacena los valores por turno de cada bot
  const initialBots = [BOT_ONE, BOT_TWO, BOT_THREE, BOT_FOUR];

  // Auxiliares
  const [index, setIndex] = useState(0);
  const [finalizada, setFinalizada] = useState(false);
  const [ganador, setGanador] = useState("");
  const [cargada, setCargada] = useState(false);
  const [simulacion, setSimulacion] = useState({});

  // Crear la simulacion
  function getSimulationdata() {
    axios({
      method: "post",
      url: `${API}/simulacion/`,
      headers: {
        Authorization: `Bearer ${token}`,
        "Access-Control-Allow-Origin": "*",
      },
      params: simData,
      paramsSerializer: {
        serialize: (params) => qs.stringify(params, { arrayFormat: "repeat" }),
      },
    })
      .then((response) => {
        // Obtener JSON de datos de la simulacion
        setSimulacion(response.data);
        setCargada(true);
      })
      .catch(() => {
        console.log("Error al obtener la simulacion");
      });
  }

  function updateGame(bots, action) {
    switch (action.type) {
      case "move": {
        if (cargada) {
          let allturns = simulacion.rondas_robots[simulacion.robots[0]].length;
          if (index < allturns) {
            let newBots = [];
            let cantRobots = simulacion.robots.length;
            for (let player = 0; player < cantRobots; player++) {
              // Actualizacion de campos de cada robot
              let namebot = simulacion.robots[player];
              let newx =
                simulacion.rondas_robots[namebot][index].datos_robot.pos_x;
              let newy =
                simulacion.rondas_robots[namebot][index].datos_robot.pos_y;
              let newdamage =
                simulacion.rondas_robots[namebot][index].datos_robot.damage;

              // Actualizacion de estado de misiles de cada robot
              let newMisiles = [];
              let refMisiles = simulacion.rondas_robots[namebot][index].misiles;
              let cantMisiles = refMisiles.length;
              for (let misil = 0; misil < cantMisiles; misil++) {
                let newexploto = refMisiles[misil].exploto;
                let newmisilx = refMisiles[misil].pos_x;
                let newmisily = refMisiles[misil].pos_y;
                let actualMisil = {
                  exploto: newexploto,
                  x: newmisilx,
                  y: newmisily,
                };
                newMisiles.push(actualMisil);
              }

              // Registro de cambios
              let actualBot = {
                name: namebot,
                color: bots[player].color,
                position: { x: newx, y: newy },
                damage: newdamage,
                misiles: newMisiles,
              };
              newBots.push(actualBot);
            }
            setIndex(index + 1);
            // newBots cambia SOLAMENTE el valor de la posicion del bot
            return newBots;
          } else {
            setGanador(simulacion.robotGanador);
            setFinalizada(true);
            return bots;
          }
        } else {
          return bots;
        }
      }
      default: {
        return bots;
      }
    }
  }

  const [bots, gameDispatch] = useReducer(updateGame, initialBots);

  useInterval(() => {
    gameDispatch({ type: "move" });
  }, 1000 / 15);

  useState(getSimulationdata, []);

  // Se renderiza la pagina
  return (
    <div>
      <div className={styles.total}>
        {token && <Board bots={bots} />}
        {token && (
          <div className={styles.statuses}>
            <h1 style={{ color: "orange" }}>Ronda: {index}</h1>
            <div className="robot-1">
              <h1 style={{ color: bots[0].color }}>
                {bots[0].name ? (bots[0].name).split('-')[0] : "No participa"}
              </h1>
              <h2 style={{ color: bots[0].color }}>
                Daño recibido: {bots[0].damage}%
              </h2>
            </div>
            <div className="robot-2">
              <h1 style={{ color: bots[1].color }}>
                {bots[1].name ? (bots[1].name).split('-')[0] : "No participa"}
              </h1>
              <h2 style={{ color: bots[1].color }}>
                Daño recibido: {bots[1].damage}%
              </h2>
            </div>
            {!(bots[2] === undefined) && (
              <div className="robot-3">
                <h1 style={{ color: bots[2].color }}>
                  {bots[2].name ? (bots[2].name).split('-')[0] : "No participa"}
                </h1>
                <h2 style={{ color: bots[2].color }}>
                  Daño recibido: {bots[2].damage}%
                </h2>
              </div>
            )}
            {!(bots[3] === undefined) && (
              <div className="robot-4">
                <h1 style={{ color: bots[3].color }}>
                  {bots[3].name !== "" ? (bots[3].name).split('-')[0] : "No participa"}
                </h1>
                <h2 style={{ color: bots[3].color }}>
                  Daño recibido: {bots[3].damage}%
                </h2>
              </div>
            )}
            {finalizada && (
              <h2 style={{ color: "white" }}>
                Resultado: {ganador !== "" ? "Ganador: " + ganador : "Empate"}
              </h2>
            )}
          </div>
        )}
      </div>
      <a href="/home" style={{ textDecoration: "none" }}>
        <Button
          variant="contained"
          color="secondary"
          style={{
            width: "100%",
            borderRadius: "15px",
            border: "3px solid white",
            position: "absolute",
            bottom: "1px",
          }}
        >
          Volver a la pagina de inicio
        </Button>
      </a>
    </div>
  );
};

export default SimulationPage;