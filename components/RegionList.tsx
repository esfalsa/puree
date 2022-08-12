import {
  TableContainer,
  Table,
  Thead,
  Tr,
  Th,
  Tbody,
  Td,
  Tfoot,
  Link,
} from "@chakra-ui/react";
import Detags from "../public/detags.json";

export default function RegionList() {
  return (
    <TableContainer>
      <Table size="sm">
        <Thead>
          <Tr>
            <Th>Region</Th>
            <Th>Issues</Th>
            <Th>Minor</Th>
            <Th>Major</Th>
          </Tr>
        </Thead>
        <Tbody>
          {Detags.map((region) => (
            <Tr key={region.Region} _hover={{ bg: "blue.50" }}>
              <Td>
                <Link
                  href={region.Link}
                  color="blue.500"
                  isExternal
                  onClick={async (e) => {
                    e.preventDefault();
                    await navigator.clipboard.writeText(region.Link);
                    window.open(region.Link, "_blank", "noopener");
                  }}
                >
                  {region.Region}
                </Link>
              </Td>
              <Td>{region.Issues}</Td>
              <Td>+{region.MinorTimestamp}</Td>
              <Td>+{region.MajorTimestamp}</Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </TableContainer>
  );
}
