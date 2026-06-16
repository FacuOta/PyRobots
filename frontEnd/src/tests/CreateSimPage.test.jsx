import React from "react";
import "@testing-library/jest-dom/extend-expect";
import { render, screen } from "@testing-library/react";
import userEvent from '@testing-library/user-event';

import CreateSimPage from "../pages/CreateSimPage";


const mockedUsedNavigate = jest.fn();

jest.mock('react-router-dom', () => ({
   ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockedUsedNavigate,
}));


test("La pagina se renderiza por completo",()=>{
    render(<CreateSimPage/>);

    const title = screen.getByRole('heading',{level: 1});
    expect(title).toBeInTheDocument();
;

    const robot1 = screen.getByText("Robot 1");
    expect(robot1).toBeInTheDocument();

    const robot2 = screen.getByText("Robot 2");
    expect(robot2).toBeInTheDocument();

    const robot3 = screen.getByText("Robot 3");
    expect(robot3).toBeInTheDocument();

    const robot4 = screen.getByText("Robot 4");
    expect(robot4).toBeInTheDocument();

    const rounds = screen.getByText("Cantidad de rondas");
    expect(rounds).toBeInTheDocument();


    const createBtn = screen.getByRole("button", {name: "Crear Simulacion"});
    expect(createBtn).toBeInTheDocument();

    const homeLink = screen.getByRole("link");
    expect(homeLink).toBeInTheDocument(); 
});

test("El campo de cantidad de rondas es requerido",()=>{
    render(<CreateSimPage/>);

    const rounds = screen.getByText("Cantidad de rondas");
    expect(rounds).toHaveClass("Mui-required");
});
