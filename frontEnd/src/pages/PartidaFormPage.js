import React from "react";
import PartidaForm from "../components/PartidaForm.js";
import Button from "@mui/material/Button";

function PartidaFormPage() {
  return (
    <div>
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