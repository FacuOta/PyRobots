import {React, useState} from "react";
import styles from './FormUserVerification.module.css';
import axios from "axios";
import { TextField, Alert, Button, IconButton } from "@mui/material";
import CloseIcon from "@mui/icons-material/Close"
import { useNavigate } from "react-router-dom";
import sleep from './sleep.js'


const VerificationForm = () => {

    const [alert, setAlert] = useState(false);
    const [alertContent, setAlertContent] = useState();
    const [severity_, setSeverity_] = useState("");
    const [UCodigo, setUCodigo] = useState({
        NombreUsuario:"",
        codigo:""
    })

    const urlVerify = "http://127.0.0.1:8000/verify_user/"
    const urlSendMail = "http://127.0.0.1:8000/send_verif_email/"
    const navigate = useNavigate();

    var bodyFormData = new FormData();

    const handleChange = (e) => {
        setUCodigo({...UCodigo, [e.target.name]: e.target.value})
    }

    const handleSubmit = (e) => {
        e.preventDefault(e);
        console.log(UCodigo);
    }

    const verify = () => {
        if(UCodigo.codigo){
        console.log("verify");
        bodyFormData.append("username", UCodigo.NombreUsuario);
        bodyFormData.append("verification_code", UCodigo.codigo);

        axios.post(
            urlVerify,
            bodyFormData)
            .then(function(response){
                setAlertContent(response.data.detail);
                setAlert(true);
                setSeverity_("success");
                sleep(1500).then(() => {navigate('/')})
            })
            .catch(function(response){
                if(response.data.detail){
                    setAlertContent(response.data.detail);
                } else {
                    setAlertContent("Hubo un error en la red")
                }
                setAlert(true);
                setSeverity_("error");
            })
        } else {
            setAlertContent("No hay ningun codigo en el formulario");
            setAlert(true);
            setSeverity_("error")
        }
    }

    const sendMail = () => {
        if(UCodigo.NombreUsuario !== ""){
            bodyFormData.append("username", UCodigo.NombreUsuario);
            console.log("mail");

            axios.post(
                urlSendMail,
                bodyFormData)
            .then(function(response){
                setAlertContent(response.data.detail);
                setAlert(true);
                setSeverity_("info");
            })
            .catch(function(response){
                if(response.data.detail){
                    setAlertContent(response.data.detail);
                    setSeverity_("warning");
                } else {
                    setAlertContent("Hubo un error en la red");
                    setSeverity_("error");
                }
                setAlert(true);
            })
        }
    }

    return(
        <div>
            {alert ?
            <Alert
                sx={{borderRadius: 2,
                     width: 1/4,
                     left: 5,
                     m:2
                }}
                action={
                    <IconButton
                    aria-label="close"
                    color="inherit"
                    size="small"
                    onClick={() => {
                        setAlert(false);
                }}
                >
                <CloseIcon fontSize="inherit" />
                </IconButton>
                } severity = {severity_}
                >
            {alertContent}
            </Alert> : <></>}
            <form onSubmit={handleSubmit} className={styles.verifyForm}>
                <h1 className={styles.titleV}>Verificar Usuario</h1>
                <h3 className={styles.subTV}>Para enviar el mail solo es necesario que ingrese su nombre de usuario, luego cargue el codigo y verifique la cuenta</h3>

                <TextField 
                    label = "Usuario"
                    name= "NombreUsuario"
                    margin= "normal"
                    required
                    fullWidth
                    type = "Text"
                    id = "outlined-basic"
                    value = {UCodigo.NombreUsuario}
                    onChange = {handleChange}
                />
                <TextField 
                    label = "Codigo"
                    name= "codigo"
                    margin= "normal"
                    fullWidth
                    type = "Number"
                    id = "outlined-basic"
                    value = {UCodigo.codigo}
                    onChange = {handleChange}
                />

                <Button sx ={{m:1}} variant="contained" type="submit" onClick={sendMail}> Enviar mail </Button>
                <Button sx ={{m:1}} variant="contained" type="submit" onClick={verify} > Verificar </Button>
            </form>
        </div>
    )
}
// >
//
export default VerificationForm;