import React from "react";
import "@testing-library/jest-dom/extend-expect";
import { render ,screen} from "@testing-library/react";
import { CreateRobot } from "../pages/CreateRobot";
import userEvent from '@testing-library/user-event';
// import { prettyDOM } from "@testing-library/dom";

const mockedUsedNavigate = jest.fn();

jest.mock('react-router-dom', () => ({
   ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockedUsedNavigate,
}));

test("La pagina se renderiza por completo", ()=>{
  render(<CreateRobot />);
  
  const avatar = screen.getByRole("img");
  expect(avatar).toBeInTheDocument();

  const robotName = screen.getByText("Nombre Robot");
  expect(robotName).toBeInTheDocument();

  const uploadFileButton = screen.getByText(/subir archivo/i);
  expect(uploadFileButton).toBeInTheDocument();

  const createRobotButton = screen.getByText(/crear robot/i);
  expect(createRobotButton).toBeInTheDocument();

  const menuButton = screen.getByText(/menu/i);
  expect(menuButton).toBeInTheDocument();

  const robotListButton = screen.getByText(/lista de robots/i);
  expect(robotListButton).toBeInTheDocument();

});

test("Todos los campos son requeridos (menos el avatar)", ()=>{
  render(<CreateRobot />);
  
  const robotName = screen.getByText("Nombre Robot");
  expect(robotName).toHaveClass("Mui-required");

  const file = screen.getByLabelText(/subir archivo/i);
  expect(file).toBeRequired();
});
