import React, { useState } from "react";
import logo from "./logo.svg";
import "./App.css";
import { AxiosInstance } from "axios";
import { AxiosContext, getAxiosInstance } from "./AxiosContext";
import { CssBaseline, ThemeProvider } from "@mui/material";
import { theme } from "./theme";
import { BrowserRouter } from "react-router-dom";

function App() {
  const [axiosInstance, setAxiosInstance] = useState<AxiosInstance>(
    getAxiosInstance(),
  );
  const setToken = (token?: string) => {
    setAxiosInstance(getAxiosInstance(token));
  };
  return (
    <React.Fragment>
      <CssBaseline />
      <ThemeProvider theme={theme}>
        <BrowserRouter>
          <div className="App">
            <AxiosContext.Provider value={axiosInstance}>
              <header className="App-header">
                <img src={logo} className="App-logo" alt="logo" />
                <p>
                  Edit <code>src/App.tsx</code> and save to reload.
                </p>
                <a
                  className="App-link"
                  href="https://reactjs.org"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Learn React
                </a>
              </header>
            </AxiosContext.Provider>
          </div>
        </BrowserRouter>
      </ThemeProvider>
    </React.Fragment>
  );
}

export default App;
