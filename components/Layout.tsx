import { Container } from "@chakra-ui/react";
import React from "react";
import Navbar from "./Navbar";

export default function Layout({ children }: React.PropsWithChildren<{}>) {
  return (
    <>
      <Navbar />
      <Container maxW={"5xl"} pt={24}>
        {children}
      </Container>
    </>
  );
}
