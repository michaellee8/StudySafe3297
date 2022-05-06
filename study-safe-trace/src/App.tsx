import React, { useState } from "react";
import logo from "./logo.svg";
import "./App.css";
import { AxiosInstance } from "axios";
import { AxiosContext, getAxiosInstance } from "./AxiosContext";
import { CssBaseline, ThemeProvider } from "@mui/material";
import { theme } from "./theme";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import IndexPage from "./pages/Index";
import SignIn from "./pages/SignIn";

function App() {
  const [axiosInstance, setAxiosInstance] = useState<AxiosInstance>(
    getAxiosInstance(),
  );
  const [authToken, setAuthToken] = useState<string | undefined>(undefined);
  const loginWithToken = (token?: string) => {
    setAuthToken(token);
    setAxiosInstance(getAxiosInstance(token));
  };
  const logout = () => {
    setAuthToken(undefined);
    setAxiosInstance(getAxiosInstance());
  };
  return (
    <React.Fragment>
      <CssBaseline />
      <ThemeProvider theme={theme}>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<IndexPage authToken={authToken} />} />
            <Route
              path="/signin"
              element={<SignIn setToken={loginWithToken} />}
            />
            <Route path="*" element={<IndexPage authToken={authToken} />} />
          </Routes>
        </BrowserRouter>
      </ThemeProvider>
    </React.Fragment>
  );
}

export default App;
