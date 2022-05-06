import React, { useState } from "react";
import "./App.css";
import { AxiosInstance } from "axios";
import { AxiosContext, getAxiosInstance } from "./AxiosContext";
import { CssBaseline, ThemeProvider } from "@mui/material";
import { theme } from "./theme";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import IndexPage from "./pages/Index";
import SignIn from "./pages/SignIn";
import Trace from "./pages/Trace";

function App() {
  const [authToken, setAuthToken] = useState<string | undefined>(undefined);
  const [axiosInstance, setAxiosInstance] = useState<AxiosInstance>(() =>
    getAxiosInstance(authToken),
  );
  const loginWithToken = (token?: string) => {
    setAuthToken(token);
    setAxiosInstance(() => getAxiosInstance(token));
  };
  const logout = () => {
    setAuthToken(undefined);
    setAxiosInstance(() => getAxiosInstance());
  };
  return (
    <AxiosContext.Provider value={axiosInstance}>
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
              <Route path="/trace" element={<Trace logout={logout}/>} />
              <Route path="*" element={<IndexPage authToken={authToken} />} />
            </Routes>
          </BrowserRouter>
        </ThemeProvider>
      </React.Fragment>
    </AxiosContext.Provider>
  );
}

export default App;
