import React from "react";
import { useState } from "react";
import {
  IconButton,
  Avatar,
  TextField,
  Button,
} from "@mui/material";
import axios from "axios";
import styles from "./Register.module.css";
import roboticon from "../img/a.png";
import { useNavigate } from "react-router-dom";
import sleep from './sleep.js'

const Register = () => {
  // Datos del formulario
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmationPassword, setConfirmationPassword] = useState("");
  // Auxiliar para la generacion de un mensaje de error
  const [errorMessage, setErrorMessage] = useState("");
  // Manipulacion de la imagen del avatar
  const [imageSelectedPrevious, setImageSelectedPrevious] = useState(null); // Para renderizar
  const [imageBD, setImageBD] = useState(null); // Usada para almacenar el avatar del usuario

  const navigate = useNavigate();

  const changeImage = (e) => {
    if (e.target.files[0] !== undefined) {
      // Avatar en base de datos
      setImageBD(e.target.files[0]);
      // Avatar en pagina
      const reader = new FileReader();
      reader.readAsDataURL(e.target.files[0]);
      reader.onload = (e) => {
        e.preventDefault();
        setImageSelectedPrevious(e.target.result);
      };
    }
  };

  // Envio la solicitud de registro
  const submitRegistration = async () => {
    // Preparo los datos para que su envio
    var formData = new FormData();
    formData.append("username", username);
    formData.append("email", email);
    formData.append("password", password);
    if (imageBD !== null) {
      formData.append("avatar", imageBD);
    }
    try {
      // Enviamos los datos a la API
      const res = await axios.post(
        "http://127.0.0.1:8000/register/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            accept: "application/json",
          },
        }
      );
      // Enviamos mensaje al usuario
      let mensaje = "";
        if (res.data.detail === "User created") {
          mensaje = "Los datos fueron confirmados, solo falta la confirmacion de email";
        } else if (res.data.detail === "Invalid image") {
          mensaje = "Avatar invalido";
        } else if (res.data.detail === "Invalid password") {
          mensaje = "Contraseña invalida";
        } else if (res.data.detail === "Non-unique email or username") {
          mensaje = "El nombre de usuario y/o el email ya estan en uso"
        } else if (res.data.detail === "Invalid email") {
          mensaje = "Email invalido";
        } else if (res.data.detail === "Invalid username") {
          mensaje = "Nombre de usuario invalido";
        } else {
          mensaje = "Creacion de perfil incorrecta";
        }
      setErrorMessage(mensaje);
      if (res.data.detail === 'User created') {
        sleep(1500).then(() => {navigate('/verification')});
      }
    } catch (e) {
      console.log(e);
      setErrorMessage(e.response.data.detail);
    }
  };

  // Reviso que se cumplan requerimientos basicos de datos
  const handleSubmit = (e) => {
    e.preventDefault();
    if (password !== confirmationPassword || password.length < 8 || password.length > 16) {
      setErrorMessage(
        "Asegurese que las contraseñas coincidan y tengan entre 8 y 16 caracteres"
      );
    } else if (username.length > 16) {
      setErrorMessage(
        "Asegurese que el nombre de usuario sea hasta 16 caracteres"
      );
    } else {
      submitRegistration();
    }
  };

  // Renderizado
  return (
    <div>
      <form className= {styles.form} onSubmit={handleSubmit}>
        <h1 style={{color: "black"}}>Registrar usuario</h1>
        <div>
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
              alt="Register Bot"
              src={
                imageSelectedPrevious == null
                  ? roboticon
                  : imageSelectedPrevious
              }
              sx={{ width: 105, height: 105 }}
            />
          </IconButton>
        </div>
        <div className= {styles.registerFields}>
          <TextField
            variant="outlined"
            type="name"
            label="Nombre de usuario"
            required
            fullWidth
            onChange={(e) => setUsername(e.target.value)}
          />
          <TextField
            variant="outlined"
            type="email"
            label="Email"
            required
            fullWidth
            onChange={(e) => setEmail(e.target.value)}
          />
          <TextField
            variant="outlined"
            type="password"
            label="Contraseña"
            required
            onChange={(e) => setPassword(e.target.value)}
          />
          <TextField
            variant="outlined"
            type="password"
            label="Confirmar Contraseña"
            required
            onChange={(e) => setConfirmationPassword(e.target.value)}
          />
        </div>
        <p>{errorMessage}</p>
        <Button type="submit" variant="contained">
          Registrarse
        </Button>
        <br></br>
          Si ya tiene una cuenta <a href="/">Inicie sesión ahora</a>
        <br />
          Si todavia no verifico su cuenta <a href="/verification"> Pulse aqui </a>
      </form>
    </div>
  );
};

export default Register;
