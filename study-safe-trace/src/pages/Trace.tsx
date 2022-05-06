import Container from "@mui/material/Container";
import React, { useContext } from "react";
import { AxiosContext } from "../AxiosContext";

export default function Trace() {
  const axiosInstance = useContext(AxiosContext);
  return <Container></Container>;
}
