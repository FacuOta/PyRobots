import {} from "./Board.module.css";

export const UNIT = 10;
export const BOARDSIZE = 1000;

export const BOT_ONE = {
  name: "",
  color: "yellow",
  position: {x: UNIT, y: UNIT},
  damage: 0,
  misiles: [{exploto: false, x: UNIT, y: UNIT}]
};

export const BOT_TWO = {
  name: "",
  color: "red",
  position: {x: UNIT, y: UNIT},
  damage: 0,
  misiles: [{exploto: false, x: UNIT, y: UNIT}]
};

export const BOT_THREE = {
  name: "",
  color: "Lawngreen",
  position: {x: UNIT, y: UNIT},
  damage: 0,
  misiles: [{exploto: false, x: UNIT, y: UNIT}]
};

export const BOT_FOUR = {
  name: "",
  color: "coral",
  position: {x: UNIT, y: UNIT},
  damage: 0,
  misiles: [{exploto: false, x: UNIT, y: UNIT}]
};