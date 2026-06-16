import React from "react";
import PartidaForm from "../components/PartidaForm.js";
import Button from "@mui/material/Button";
import SimForm from "../components/SimForm.jsx";

function CreateSimPage() {
  return (
    <div>
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