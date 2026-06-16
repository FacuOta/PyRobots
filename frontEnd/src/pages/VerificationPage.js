import Button from "@mui/material/Button";
import React from "react";
import VerificationForm from '../components/FormUserVerification.js'

function VerificationPage() {
    return(
        <div>
            <VerificationForm />
            <br />
            <a href="/register">
                <Button
                    color = "error"
                    variant= "containted"
                    style={{ borderRadius: "100px",
                             position:"absolute",
                             bottom: 15,
                             left: 15,
                             color: "white",
                             background: 'red' }}
                >
                 Registrarse
                </Button>
            </a>
            <a href="/">
                <Button
                    color = "error"
                    variant= "containted"
                    style={{ borderRadius: "100px",
                             position: "absolute",
                             bottom: 15,
                             right: 15,
                             color: "white",
                             background: 'red'}}
                >
                 Login
                </Button>
            </a>
        </div>
    )
}

export default VerificationPage;