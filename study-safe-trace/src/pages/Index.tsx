import React from "react";
import { Navigate } from "react-router";

interface IndexPageProps {
  authToken?: string;
}

export default function IndexPage({ authToken }: IndexPageProps) {
  return authToken ? (
    <Navigate to={"/trace"} replace={true} />
  ) : (
    <Navigate to={"/signin"} replace={true} />
  );
}
