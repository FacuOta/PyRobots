import { API } from "../api";
import styles from "./Login.module.css"
import React from "react";
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import axios from "axios";
import sleep from './sleep.js'
import { useNavigate } from "react-router-dom";

const Login = () => {

  const [user, setUser] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [error, setError] = React.useState(false);

  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault()

    let bodyFormData = new FormData();
    bodyFormData.append('username', user);
    bodyFormData.append('password', password);

    axios({
      method: "post",
      url: `${API}/login`,
      data: bodyFormData,
      headers: { "Content-Type": "multipart/form-data" }
    })
      .then((response) => {
        const token = response.data.access_token;
        sessionStorage.setItem("access_token", token);
        sleep(1000).then(() => {navigate("/home")})
      })
      .catch(() => {
        setError(true);
      })
  }

  return (
    <div className={styles.login}>
      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.loginFields}>
          <TextField
            className={styles.loginUser}
            error={error}
            required
            id="outlined-basic"
            label="Usuario"
            variant="outlined"
            fullWidth
            onChange={(e) => setUser(e.target.value)} />

          <TextField
            className={styles.loginPassword}
            required
            error={error}
            type="password"
            id="outlined-basic"
            label="Contraseña"
            variant="outlined"
            fullWidth
            onChange={(e) => setPassword(e.target.value)} />
        </div>
        <p hidden={!error} className={styles.loginError}>
        El usuario y/o la contraseña son incorrectos
        </p>
        <Button className={styles.loginButton} type="submit" variant="contained">Iniciar Sesion</Button>
      </form>
      <hr></hr>
      <p className={styles.registerText}>No tienes Cuenta? <a href="/register">Registrate</a></p>
    </div>
  )
}

export default Login;
