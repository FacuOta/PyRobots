import React from "react";
import PartidaForm from "../components/PartidaForm.js";
import Button from "@mui/material/Button";
import centrado from "./PantallaCentrada.module.css";

function PartidaFormPage() {
  return (
    <div className={centrado.pantalla}>
      <PartidaForm />
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

export default PartidaFormPage;