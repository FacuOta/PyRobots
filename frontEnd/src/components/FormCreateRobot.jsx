import * as React from "react";
import TextField from "@mui/material/TextField";
import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import { useState } from "react";
import axios from "axios";
import "./stylesCreateRobot.module.css";
import roboticon from "../img/a.png";
import Snackbar from "@mui/material/Snackbar";
import { Alert } from "@mui/material";
import styles from "./FormCreateRobot.module.css"
import sleep from './sleep.js'
import { useNavigate } from "react-router-dom";


var creador = sessionStorage.getItem('access_token');
export function FormRobot() {
  const [ImageSelectedPrevious, setImageSelectedPrevious] = useState();
  const [ImageSelected, setImageSelected] = useState(null);
  const [FileSelectedPrevious, setFileSelectedPrevious] = useState(null);
  const [FileSelected, setFileSelected] = useState(null);
  const [UserSelected, setUserSelected] = useState(null);
  const [open, setOpen] = useState(false);
  const [open2, setOpen2] = useState(false);
  const [open3, setOpen3] = useState(false);

  const navigate = useNavigate();

  const changeImage = (e) => {
    if (e.target.files[0] !== undefined) {
      setImageSelected(e.target.files[0]);
      const reader = new FileReader();
      reader.readAsDataURL(e.target.files[0]);
      reader.onload = (e) => {
        e.preventDefault();
        setImageSelectedPrevious(e.target.result);
      };
    }
  };

  const captureFiles = (e) => {
    setFileSelectedPrevious(e.target.value);
    setFileSelected(e.target.files[0]);
  };

  const sendData = () => {
    var formData = new FormData();

    const url = "http://127.0.0.1:8000/robot/";
    formData.append("robotCode", FileSelected);
    formData.append("robotName", UserSelected);
    if (ImageSelected !== null) {
      formData.append("robotAvatar", ImageSelected);
    }

    axios
      .post(url, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
          "Authorization":"Bearer " + creador,
          "Access-Control-Allow-Origin": "*"
        },
      })
      .then((res) => {
        console.log(res.status);
        if (res.status === 201) {
          setOpen(true);
          sleep(1500).then(() => {navigate('/listrobots')})
        }
        
      }).catch(error => {console.log(error.response.status)
        if(error.response.status===422){
          setOpen2(true);
        }
        else if(error.response.status===400){
          setOpen3(true);
        }
      
      });
  };
  const handleClose = () => {
    setOpen(false);
  };
  const handleClose2 = () => {
    setOpen2(false);
  };
  const handleClose3 = () => {
    setOpen3(false);
  };

  return (
    <div>
      <form className= {styles.formRobot}>
        <IconButton
          color="primary"
          aria-label="upload picture"
          component="label"
        >
          <input
            hidden
            accept="image/*"
            type="file"
            onChange={(e) => {
              changeImage(e);
            }}
          />
          <Avatar
            alt="Remy Sharp"
            src={
              ImageSelectedPrevious == null ? roboticon : ImageSelectedPrevious
            }
            sx={{ width: 125, height: 125 }}
            className="icono"
          />
        </IconButton>
        <span className="separar"></span>
        <TextField
          id="outlined-basic"
          title="Nombre Robot"
          label="Nombre Robot"
          variant="outlined"
          className={styles.NombreRobot}
          sx={{margin: 3}}
          required
          fullWidth
          onChange={(e) => {
            setUserSelected(e.target.value);
          }}
        />
        <span className="separar"></span>
        <Button variant="contained" component="label" className="bbutton">
          Subir Archivo
          <input
            hidden
            accept=".py"
            type="file"
            required
            onChange={(e) => {
              captureFiles(e);
            }}
          />
        </Button>
        <span style={{ margin: "12px" }}>{FileSelectedPrevious}</span>

        <Button variant="contained" className="bbutton" onClick={sendData}>
          Crear Robot
        </Button>
      </form>
      <Snackbar
        open={open}
        autoHideDuration={6000}
        onClose={handleClose}
        style={{ marginLeft: "100px" }}
      >
        <Alert onClose={handleClose} severity="success" sx={{ width: "100%" }}>
          Robot Creado
        </Alert>
      </Snackbar>
      <Snackbar
        open={open2}
        autoHideDuration={6000}
        onClose={handleClose2}
        style={{ marginLeft: "100px" }}
      >
        <Alert onClose={handleClose2} severity="error" sx={{ width: "100%" }}>
          Suba un archivo o escriba un nombre correcto
        </Alert>
      </Snackbar>
      <Snackbar
        open={open3}
        autoHideDuration={6000}
        onClose={handleClose3}
        style={{ marginLeft: "100px" }}
      >
        <Alert onClose={handleClose3} severity="error" sx={{ width: "100%" }}>
          Nombre del robot existente
        </Alert>
      </Snackbar>
    </div>
  );
}
