import {
  StatGroup,
  Stat,
  StatLabel,
  StatNumber,
  Box,
  Divider,
  Flex,
  Link,
  Icon,
  Stack,
  Text,
} from "@chakra-ui/react";
import type { NextPage } from "next";
import Head from "next/head";
import RegionList from "../components/RegionList";
import History from "../public/history.json";
import Detags from "../public/detags.json";
import { FaFileDownload } from "react-icons/fa";

const Home: NextPage = () => {
  return (
    <>
      <Head>
        <title>Purée</title>
        <meta
          name="description"
          content="A quick and easy way to find regions that have been tagged."
        />
      </Head>

      <Flex direction={"column"} rowGap={4} as={"main"}>
        <StatGroup>
          <Stat>
            <StatLabel>Daily Dump</StatLabel>
            <StatNumber>{History[History.length - 1].Date}</StatNumber>
          </Stat>

          <Stat>
            <StatLabel>Regions Found</StatLabel>
            <StatNumber>{Detags.length}</StatNumber>
          </Stat>
        </StatGroup>

        <Divider />

        <Stack direction={"row"} spacing={4}>
          <Text>Download:</Text>

          <Link color={"blue.500"} href="/puree/detags.csv" download>
            <Flex direction={"row"} align="center" columnGap={1}>
              <Icon as={FaFileDownload} /> CSV
            </Flex>
          </Link>

          <Link color={"blue.500"} href="/puree/detags.json" download>
            <Flex direction={"row"} align="center" columnGap={1}>
              <Icon as={FaFileDownload} /> JSON
            </Flex>
          </Link>

          <Link color={"blue.500"} href="/puree/detags.xlsx" download>
            <Flex direction={"row"} align="center" columnGap={1}>
              <Icon as={FaFileDownload} /> Excel Sheet
            </Flex>
          </Link>
        </Stack>

        <Box borderWidth="1px" borderRadius="lg" py={2}>
          <RegionList />
        </Box>
      </Flex>
    </>
  );
};

export default Home;
