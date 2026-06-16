import React from "react";
import { Button, ButtonGroup } from "@mui/material";

const filterPartida = (props) => {

    return(
        <ButtonGroup variant="contained" aria-label="outlined primary button group" sx ={{ mb: 1, ml: 3 }}>
            <Button value={"noTerminadas"} sx={{ bgcolor: props.filtro === "noTerminadas" ? '#044485': ''}} onClick={() => {props.setFiltro("noTerminadas")}}>No iniciadas</Button>
            <Button value={"terminadas"} sx={{ bgcolor: props.filtro === "terminadas" ? '#044485': '' }} onClick={() => {props.setFiltro("terminadas")}}>Completadas</Button>
        </ButtonGroup>
    );
}

export default filterPartida;