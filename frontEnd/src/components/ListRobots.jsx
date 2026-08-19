import { API } from "../api";
import React, { useEffect } from "react";
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button"
import AddIcon from '@mui/icons-material/Add';
import axios from "axios";
import styles from "./ListRobots.module.css"



function ListRobots(){
    const [robots, setRobots] = React.useState([]);
    const [images, setImages] = React.useState([]);

    const token = sessionStorage.getItem("access_token");
  
    function getRobots() {
  
      axios({
        method: 'get',
        url: `${API}/get_robots/`,
        headers: { 'Authorization': `Bearer ${token}` },
      }
      )
        .then((response) => {
          setRobots(response.data.robotNames);
        })
        .catch((err) => {
          console.log('An error has ocurred images')
        })
    }

    function getImages() {
  
      axios({
        method: 'get',
        url: `${API}/images`,
        headers: { 'Authorization': `Bearer ${token}` },
      }
      )
        .then((response) => {
          setImages(response.data)
        })
        .catch((err) => {
          console.log('An error has ocurred')
        })
    }

    function getImgUrl(robotName){
      console.log(images.length);
      for (let i = 0; i < images.length; i++) {
        if (robotName === images[i].robotname){
          return (`${API}` + images[i].path);
        }
      }
    }
  
    useEffect(getRobots, []);
    useEffect(getImages, []);

  
    return (
      <div className={styles.list}>

        <Button
          variant="contained"
          style={{
            marginBottom: 5,
            float: "right",
            backgroundColor: "green",
          }}
          endIcon={<AddIcon />}
          href="/robot"
        >
          Crear Robot
        </Button>
  
        <TableContainer className={styles.table} component={Paper}>
          <Table sx={{ minWidth: 650 }} size="small" aria-label="a dense table">
            <TableHead className= {styles.tableHead}>
              <TableRow>
                <TableCell padding="checkbox">Avatar</TableCell>
                <TableCell>Nombre</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {robots.length === 0 &&
                <TableRow
                sx={{ '&:last-child td, &:last-child th': { border: 0 }}}
              ><TableCell className={styles.missingText}>No hay robots para mostrar.</TableCell>
              </TableRow>
              }
              {
              robots.length > 0 && robots.map((robot) => (
                <TableRow
                  key={robot}
                  sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                >
                  <TableCell>
                    {images.some(e=> e.robotname === robot) ? 
                    <Avatar style={{ width: "100px", height: "100px",backgroundColor:"#ffff"}}  src={getImgUrl(robot)}/> :
                    <Avatar style={{ width: "100px", height: "100px",backgroundColor:"#ffff"}}  src="https://robohash.org/66"/> 
                    } 
                  </TableCell>
                  <TableCell component="th" scope="robot">
                    {robot}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </div>
    )
}

export default ListRobots;