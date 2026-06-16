import React from "react";
import "@testing-library/jest-dom/extend-expect";
import { render, screen } from "@testing-library/react";

import MatchResults from "../pages/MatchResults";


test("La pagina se renderiza por completo",()=>{
    render(<MatchResults />);

    const confetti = screen.queryByTestId("canvas");
    expect(confetti).not.toBeInTheDocument();

    const msgDiv = screen.getByTestId("msg");
    expect(msgDiv).toBeInTheDocument();

    const error = screen.getByTestId("error");
    expect(error).toBeInTheDocument();

    const backBtn = screen.getByTestId("btn");
    expect(backBtn).toBeInTheDocument();
});