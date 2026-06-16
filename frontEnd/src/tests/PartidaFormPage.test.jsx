import React from "react";
import "@testing-library/jest-dom/extend-expect";
import { render, screen } from "@testing-library/react";
import userEvent from '@testing-library/user-event';

import PartidaForm from "../pages/PartidaFormPage";

const mockedUsedNavigate = jest.fn();

jest.mock('react-router-dom', () => ({
   ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockedUsedNavigate,
}));

test("La pagina se renderiza por completo",()=>{
    render(<PartidaForm/>);

    const title = screen.getByRole('heading',{level: 1});
    expect(title).toBeInTheDocument();

    const matchName = screen.getByText("Nombre de partida");
    expect(matchName).toBeInTheDocument();

    const maxPlayers = screen.getByText("Cantidad maxima de jugadores");
    expect(maxPlayers).toBeInTheDocument();

    const games = screen.getByText("Cantidad de juegos");
    expect(games).toBeInTheDocument();

    const rounds = screen.getByText("Cantidad de rondas");
    expect(rounds).toBeInTheDocument();


    /* 
    * aplicado asi porque las dos cosas que agarra son del mismo componente. 
    ? mala practica?
    */
    const pass = screen.getAllByText("Contraseña");
    pass.map((elem)=>expect(elem).toBeInTheDocument());

    const createBtn = screen.getByRole("button", {name: "Crear Partida"});
    expect(createBtn).toBeInTheDocument();

    const homeLink = screen.getByRole("link");
    expect(homeLink).toBeInTheDocument(); 
});

test("Todos los campos son requeridos (menos contraseña)",()=>{
    render(<PartidaForm/>);

    const matchName = screen.getByText("Nombre de partida");
    expect(matchName).toHaveClass("Mui-required");

    const maxPlayers = screen.getByText("Cantidad maxima de jugadores");
    expect(maxPlayers).toHaveClass("Mui-required");

    const games = screen.getByText("Cantidad de juegos");
    expect(games).toHaveClass("Mui-required");

    const rounds = screen.getByText("Cantidad de rondas");
    expect(rounds).toHaveClass("Mui-required");
});

