import axios, { AxiosInstance } from "axios";
import React from "react";

export const API_URL = "https://studysafe3297-michaellee8.herokuapp.com/";

export const AxiosContext = React.createContext<AxiosInstance>(
  getAxiosInstance(),
);

export function getAxiosInstance(token?: string): AxiosInstance {
  return axios.create({
    baseURL: API_URL,
    timeout: 1000,
    headers: token
      ? {
          Authorization: `Token ${token}`,
        }
      : {},
  });
}
