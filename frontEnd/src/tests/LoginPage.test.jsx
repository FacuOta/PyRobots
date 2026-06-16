import React from "react";
import "@testing-library/jest-dom/extend-expect";
import { render, screen } from "@testing-library/react";

import LoginPage from "../pages/LoginPage";

const mockedUsedNavigate = jest.fn();

jest.mock('react-router-dom', () => ({
   ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockedUsedNavigate,
}));


test("El titulo se muestra correctamente", ()=>{
  render(<LoginPage />);
  const title = screen.getByText("PyRobots");
  expect(title).toBeInTheDocument();
});

test("El form se muestra correctamente", ()=>{
  render(<LoginPage />);
  const user = screen.getByText("Usuario");
  expect(user).toBeInTheDocument();

  const pass = screen.getByText("Contraseña");
  expect(pass).toBeInTheDocument();

  const loginButton = screen.getByText(/iniciar sesion/i);
  expect(loginButton).toBeInTheDocument();
});

test("Los campos del form son obligatorios",()=>{
  render(<LoginPage />);
  const user = screen.getByText('Usuario');
  expect(user).toHaveClass("Mui-required");

  const pass = screen.getByText('Contraseña');
  expect(pass).toHaveClass("Mui-required");
});

test("Se muestra mensaje para crear nueva cuenta",()=>{
  render(<LoginPage />);
  const registerMsg = screen.getByText("No tienes Cuenta?");
  expect(registerMsg).toBeInTheDocument();
});

  test("El mensaje de user/pass incorrecto esta oculto por defecto",()=> {
  render(<LoginPage />);
  const errMsg = screen.getByText("El usuario y/o la contraseña son incorrectos o la cuenta no esta verificada");
  expect(errMsg).not.toBeVisible();
});
