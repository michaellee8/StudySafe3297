import React, { useState } from "react";
import logo from "./logo.svg";
import "./App.css";
import { AxiosInstance } from "axios";
import { AxiosContext, getAxiosInstance } from "./AxiosContext";

function App() {
  const [axiosInstance, setAxiosInstance] = useState<AxiosInstance>(
    getAxiosInstance(),
  );
  return (
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
  );
}

export default App;
