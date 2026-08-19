import MatchsPage from "./pages/MatchsPage";
import LoginPage from "./pages/LoginPage";
import { HomePage } from "./pages/HomePage";
import RegisterPage from "./pages/RegisterPage";
import { CreateRobot } from "./pages/CreateRobot";
import PartidaFormPage from "./pages/PartidaFormPage";
import SimulationPage from "./pages/SimulationPage";

import "./stylesPage.module.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ListRobotsPage from "./pages/ListRobotsPage";
import MatchResults from "./pages/MatchResults";
import SimulationFormPage from "./pages/CreateSimPage";
import LobbyPage from "./pages/LobbyPage";

const App = () => {
  return (
    <BrowserRouter basename={process.env.PUBLIC_URL}>
      <Routes>
        <Route path="/home" element={ <HomePage></HomePage> }></Route>
        <Route path="/" element={<LoginPage></LoginPage> }></Route>
        <Route path="/register" element={ <RegisterPage></RegisterPage> }></Route>
        <Route path="/createsim" element={ <SimulationFormPage></SimulationFormPage> }></Route>
        <Route path="/simulation" element={ <SimulationPage></SimulationPage> }></Route>
        <Route path="/listgame" element={ <MatchsPage></MatchsPage> }></Route>
        <Route path="/robot" element={ <CreateRobot></CreateRobot> }></Route>
        <Route path="/listrobots" element={ <ListRobotsPage></ListRobotsPage> }></Route>
        <Route path="/creategame" element={ <PartidaFormPage></PartidaFormPage> }></Route>

        <Route path="/results/:id" component={MatchResults} element={<MatchResults />}></Route>
        <Route path="/lobby" element={<LobbyPage />}> </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
