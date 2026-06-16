import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import { HeaderHome } from "../components/HeaderHome";
import img1 from "../img/2.png";
import img2 from "../img/21.png";
import img3 from "../img/22.png";
import img4 from "../img/23.png";

export function HomePage() {
  return (
    <div>
      <HeaderHome></HeaderHome>
      <Box
        sx={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "space-between",
          marginBottom: "50px",
          "& > :not(style)": {
            m: 4,
            width: 250,
            height: 290,
          },
        }}
      >
        <div
          style={{
            background: "#2A9D8F",
            borderRadius: "20px",
            border: "4px solid white",
          }}
        >
          <img src={img1} width="245"></img>
          <a href="/creategame" style={{ textDecoration: "none" }}>
            <Button
              variant="contained"
              color="warning"
              style={{
                width: "100%",
                borderRadius: "15px",
                border: "3px solid white",
              }}
            >
              Partida
            </Button>
          </a>
        </div>
        <div
          style={{
            background: "#8ecae6",
            borderRadius: "20px",
            border: "4px solid white",
          }}
        >
          <img src={img3} width="245"></img>
          <a href="/createsim" style={{ textDecoration: "none" }}>
            <Button
              variant="contained"
              color="error"
              style={{
                width: "100%",
                borderRadius: "15px",
                border: "3px solid white",
              }}
            >
              Simulacion
            </Button>
          </a>
        </div>
        <div
          style={{
            background: "#219ebc",
            borderRadius: "20px",
            border: "4px solid white",
          }}
        >
          <img src={img2} width="245"></img>
          <a href="/listrobots" style={{ textDecoration: "none" }}>
            <Button
              variant="contained"
              color="success"
              style={{
                width: "100%",
                borderRadius: "15px",
                border: "3px solid white",
              }}
            >
              Robots
            </Button>
          </a>
        </div>
        <div
          style={{
            background: "#577590",
            borderRadius: "20px",
            border: "4px solid white",
          }}
        >
          <img src={img4} width="245"></img>
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
              Lista de partidas
            </Button>
          </a>
        </div>
      </Box>
      <div style={{ textAlign: "center", marginBottom: "15px" }}>
        <h1 style={{ color: "white", fontSize: "50px", margin: "0" }}>
          PYROBOTS
        </h1>
      </div>
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "space-between",
          marginTop: "50px",
          color: "#ffff",
        }}
      >
        <span>Francisco Cortez</span>
        <span>Lucas Cordoba</span>
        <span>Agustin Ardizzone</span>
        <span>Facundo Granado</span>
        <span>Francisco Ferrante</span>
        <span>Juan Cortez</span>
        <span>Facundo Otamendi</span>
      </div>
    </div>
  );
}