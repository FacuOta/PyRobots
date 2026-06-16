import React from "react";
import "@testing-library/jest-dom/extend-expect";
import { render, screen } from "@testing-library/react";
import userEvent from '@testing-library/user-event';

import {HomePage} from "../pages/HomePage";

const mockedUsedNavigate = jest.fn();

jest.mock('react-router-dom', () => ({
   ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockedUsedNavigate,
}));

test("La pagina se renderiza por completo",()=>{
    render(<HomePage />);

    //test de si se muestran el avatar y las otras 4 imagenes.
    const images = screen.getAllByRole("img");
    expect(images).toHaveLength(5);

    const logoutBtn = screen.getByText(/cerrar sesion/i);
    expect(logoutBtn).toBeInTheDocument();

    const matchBtn = screen.getByText("Partida");
    expect(matchBtn).toBeInTheDocument();

    const simulationBtn = screen.getByText(/simulacion/i);
    expect(simulationBtn).toBeInTheDocument();

    const robotBtn = screen.getByText("Robots");
    expect(robotBtn).toBeInTheDocument();

    const matchListBtn = screen.getByText(/lista de partidas/i);
    expect(matchListBtn).toBeInTheDocument();

    const title = screen.getByText(/pyrobots/i);
    expect(title).toBeInTheDocument();

    //Como agarrar a los integrantes?
    const integrantes = ["Francisco Cortez", "Lucas Cordoba",
                         "Agustin Ardizzone", "Facundo Granado",
                         "Francisco Ferrante", "Juan Cortez", "Facundo Otamendi"]
    
    const devs = integrantes.map((integrante)=>{
        screen.getByText(integrante);
    });
    expect(devs).toHaveLength(7);

});