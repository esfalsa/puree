import {
  Box,
  Flex,
  Icon,
  Link,
  Stack,
  Text,
  useColorModeValue,
  useTheme,
  useToken,
} from "@chakra-ui/react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  defaults,
} from "chart.js";
import { Line } from "react-chartjs-2";
import { FaFileDownload } from "react-icons/fa";
import History from "../public/history.json";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip
);

export default function HistoryPage() {
  const lineColor = useToken("colors", "blue.500");
  const topMargin = useToken("space", 24);
  defaults.font.family = useToken("fonts", "body");

  return (
    <Flex
      direction={"column"}
      rowGap={4}
      as={"main"}
      minH={`calc(100vh - ${topMargin})`}
      pb={8}
    >
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

      <Box flexGrow={1}>
        <Line
          options={{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: false,
              },
              title: {
                display: true,
                text: "Tagged Regions Found by Day",
              },
            },
            interaction: {
              mode: "nearest",
              intersect: false,
              axis: "x",
            },
          }}
          data={{
            labels: History.map((day) => day.Date),
            datasets: [
              {
                label: "Tagged Regions",
                data: History.map((day) => day.Count),
                fill: false,
                borderColor: lineColor,
                pointBackgroundColor: lineColor,
                tension: 0.1,
              },
            ],
          }}
        />
      </Box>
    </Flex>
  );
}
