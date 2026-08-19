import React from "react";
import PartidaForm from "../components/PartidaForm.js";
import Button from "@mui/material/Button";
import SimForm from "../components/SimForm.jsx";
import centrado from "./PantallaCentrada.module.css";

function CreateSimPage() {
  return (
    <div className={centrado.pantalla}>
      <SimForm />
      <br />
      <a href="/home">
        <Button
          variant="contained"
          color="error"
          style={{ borderRadius: "100px",
                   position:"absolute",
                   bottom: 15,
                   left: 15 }}
        >
          Menu
        </Button>
      </a>
    </div>
  );
}

export default CreateSimPage;