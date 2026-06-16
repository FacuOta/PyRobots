import Button from "@mui/material/Button";
import Avatar from "@mui/material/Avatar";
export function HeaderHome() {
  
  const handleLogOut = (()=> sessionStorage.removeItem("access_token"))
  
  return (
    <div
      style={{
        height: "93px",
        display: "flex",
        justifyContent: "space-between",
        marginBottom: "20px",
        flexWrap: "wrap",
      }}
    >
      <Avatar style={{ width: "100px", height: "100px", marginLeft: "30px",backgroundColor:"#ffff"}} 
              src="https://robohash.org/66"
      />
      <div>
        <h2 style={{ color: "white" }}></h2>
      </div>
      <a href="/" style={{ textDecoration: "none" }}>
        <Button
          variant="contained"
          onClick={handleLogOut}
          style={{
            height: "50px",
            margin: "20px 30px 0 0",
            border: "3px solid white",
            borderRadius: "15px",
          }}
        >
          Cerrar Sesion
        </Button>
      </a>
    </div>
  );
}
