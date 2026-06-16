import React from "react";
import "@testing-library/jest-dom/extend-expect";
import { render, screen } from "@testing-library/react";
import userEvent from '@testing-library/user-event';

import RegisterPage from "../pages/RegisterPage";

const mockedUsedNavigate = jest.fn();

jest.mock('react-router-dom', () => ({
   ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockedUsedNavigate,
}));

test("La pagina se renderiza por completo", () => {
  render(<RegisterPage />);

  const title = screen.getByText("Registrar usuario");
  expect(title).toBeInTheDocument();

  const avatar = screen.getByRole("img");
  expect(avatar).toBeInTheDocument();

  const user = screen.getByText("Nombre de usuario");
  expect(user).toBeInTheDocument();

  const email = screen.getByText("Email");
  expect(email).toBeInTheDocument();

  const pass = screen.getByText("Contraseña");
  expect(pass).toBeInTheDocument();

  const passValidate = screen.getByText("Confirmar Contraseña");
  expect(passValidate).toBeInTheDocument();

  const registerBtn = screen.getByText(/registrarse/i);
  expect(registerBtn).toBeInTheDocument();

  const loginRedirect = screen.getByText(/Inicie Sesión ahora/i);
  expect(loginRedirect).toBeInTheDocument();

  const passRequirements = screen.getAllByText(/La contraseña debe contener/i);
  expect(passRequirements).toHaveLength(4);
});

test("Todos los campos son requeridos (menos el avatar)",()=>{
  render(<RegisterPage />);

  const user = screen.getByText("Nombre de usuario");
  expect(user).toHaveClass("Mui-required");

  const email = screen.getByText("Email");
  expect(email).toHaveClass("Mui-required");

  const pass = screen.getByText("Contraseña");
  expect(pass).toHaveClass("Mui-required");

  const passValidate = screen.getByText("Confirmar Contraseña");
  expect(passValidate).toHaveClass("Mui-required");
});