import React from "react";
import MatchsList from "../components/MatchsList";
import Button from "@mui/material/Button"
import ArrowBackIcon from '@mui/icons-material/ArrowBack';

import styles from "./MatchsPage.module.css";


function MatchsPage() {
    return (
        <div className={styles.listPage}>
            <div className={styles.divlist}>
                <MatchsList className={styles.listPage}/>
            </div>
            <Button
                className={styles.backButton}
                variant="contained"
                startIcon={<ArrowBackIcon />}
            >
                <a className={styles.link} href="/home">Volver a Home</a>
            </Button>
        </div>
    )
}

export default MatchsPage