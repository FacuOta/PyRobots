import React, {useEffect, useRef} from "react";
import styles from "./Board.module.css";
import { UNIT, BOARDSIZE } from "./const.js"

const Board = ({bots}) => {
  const canvasRef = useRef();

  // Dibujo los cambios de posicion
  useEffect(() => {
    const ctx = canvasRef.current.getContext('2d');
    ctx.clearRect(0,0,BOARDSIZE,BOARDSIZE);
    ctx.fillStyle = "black";
    ctx.fillRect(0,0,BOARDSIZE,BOARDSIZE);
    bots.forEach(bot => {
      if (bot.damage < 100 && bot.name !== '') { // Cada robot existente y vivo se dibuja
        ctx.fillStyle = bot.color;
        ctx.fillRect(bot.position.x, bot.position.y, UNIT, UNIT*2);
      }
      if (bot.misiles !== undefined && bot.misiles.length > 0) { // Confirmacion de existencia de misiles
        bot.misiles.forEach(misil => {
          ctx.fillStyle = "white";
          if (misil.exploto) {
            ctx.fillRect(misil.x, misil.y, UNIT*3, UNIT*3);
          } else {
            ctx.fillRect(misil.x, misil.y, UNIT, UNIT);
          }
        })
      }
    });
  }, [bots]);

  // Renderizo el tablero
  return (
    <canvas ref={canvasRef} id="board" className={styles.board} width={BOARDSIZE} height={BOARDSIZE}></canvas>
  )
};

export default Board;