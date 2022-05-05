import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import React, { useContext, useState } from "react";
import { AxiosContext } from "../AxiosContext";
import TextField from "@mui/material/TextField";
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
} from "@mui/material";
import { useNavigate } from "react-router";

interface SignInProps {
  setToken: (token?: string) => void;
}

function SignIn({ setToken }: SignInProps) {
  const axiosInstance = useContext(AxiosContext);
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [alertOpen, setAlertOpen] = useState(false);
  const [alertErrorMessage, setAlertErrorMessage] = useState("");
  const handleSignIn = async () => {
    try {
      const res = await axiosInstance.post("/api-token-auth/", {
        username,
        password,
      });
      console.debug(`Signed in with token ${res.data.token}`);
      setToken(res.data.token);
      navigate("/trace");
    } catch (err: any) {
      setAlertErrorMessage(`${err}`);
      setAlertOpen(true);
    }
  };
  const handleCloseDialog = () => {
    setAlertErrorMessage("");
    setAlertOpen(false);
  };
  return (
    <Container maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Typography component="h1" variant="h5">
          Sign in to proceed
        </Typography>
        <Box sx={{ mt: 1 }}>
          <TextField
            margin="normal"
            required
            fullWidth
            label="Username"
            autoComplete="username"
            autoFocus
            value={username}
            onChange={(event) => {
              setUsername(event.target.value);
            }}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            label="Password"
            type="password"
            autoComplete="current-password"
            value={password}
            onChange={(event) => {
              setPassword(event.target.value);
            }}
          />
          <Button fullWidth variant="contained" sx={{ mt: 3, mb: 2 }} />
        </Box>
      </Box>
      <Dialog open={alertOpen} onClose={handleCloseDialog}>
        <DialogTitle>{"SignIn failed"}</DialogTitle>
        <DialogContent>
          <DialogContentText>{alertErrorMessage}</DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog} autoFocus>
            Dismiss
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}
