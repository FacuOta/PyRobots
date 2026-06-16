import React from "react";
import "@testing-library/jest-dom/extend-expect";
import { render, screen } from "@testing-library/react";
import userEvent from '@testing-library/user-event';

import ListRobotsPage from "../pages/ListRobotsPage";

const mockedUsedNavigate = jest.fn();

jest.mock('react-router-dom', () => ({
   ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockedUsedNavigate,
}));

test("La pagina se renderiza por completo",()=>{
    render(<ListRobotsPage />);
    const createButton = screen.getByText(/crear robot/i);
    expect(createButton).toBeInTheDocument();
    
    const backButton = screen.getByText(/volver a home/i);
    expect(backButton).toBeInTheDocument();
    
    const matchsTable = screen.getByRole("table");
    expect(matchsTable).toBeInTheDocument();
});

test("Se muestra mensaje de que no hay robots para mostrar cuando no se llama al back",()=>{
    render(<ListRobotsPage />);
    const noMatchesMsg = screen.getByText(/No hay robots para mostrar./i)
    expect(noMatchesMsg).toBeInTheDocument();
});