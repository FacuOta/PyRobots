import React from "react";
import ListRobots from "../components/ListRobots";
import Button from "@mui/material/Button"
import ArrowBackIcon from '@mui/icons-material/ArrowBack';

import styles from "./ListRobotsPage.module.css";

function ListRobotsPage() {
    return (
        <div className={styles.listPage}>
            <div className={styles.divlist}>
                <ListRobots className={styles.listPage}/>
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

export default ListRobotsPage