import { FormRobot } from "../components/FormCreateRobot";
import Button from "@mui/material/Button";
import centrado from "./PantallaCentrada.module.css";

export function CreateRobot() {
  return (
    <div className={centrado.pantalla}>
      <FormRobot></FormRobot>
      <a href="/home">
        {" "}
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
      <Button
        variant="contained"
        color="error"
        style={{ borderRadius: "100px", float: "right", position: "absolute", bottom: 15, right: 15 }}
        href="/listrobots"
      >
        Lista De Robots
      </Button>
    </div>
  );
}
