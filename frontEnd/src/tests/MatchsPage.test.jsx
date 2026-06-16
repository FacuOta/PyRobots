import React from "react";
import "@testing-library/jest-dom/extend-expect";
import { render, screen } from "@testing-library/react";
import userEvent from '@testing-library/user-event';

import MatchsPage from "../pages/MatchsPage";

const mockedUsedNavigate = jest.fn();

jest.mock('react-router-dom', () => ({
   ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockedUsedNavigate,
}));

test("La pagina se renderiza por completo",()=>{
    render(<MatchsPage />);
    const createButton = screen.getByText(/crear partida/i);
    expect(createButton).toBeInTheDocument();
    
    const updateButton = screen.getByText(/actualizar/i);
    expect(updateButton).toBeInTheDocument();
    
    const backButton = screen.getByText(/volver a home/i);
    expect(backButton).toBeInTheDocument();
    
    const matchsTable = screen.getByRole("table");
    expect(matchsTable).toBeInTheDocument();
});

test("Se muestra mensaje de que no hay partidas disponibles cuando no se llama al back",()=>{
    render(<MatchsPage />);
    const noMatchesMsg = screen.getByText(/No se encontraron partidas iniciadas/i)
    expect(noMatchesMsg).toBeInTheDocument();
});
