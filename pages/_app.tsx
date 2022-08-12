import type { AppProps } from "next/app";
import { ChakraProvider, extendTheme } from "@chakra-ui/react";
import { withProse } from "@nikolovlazar/chakra-ui-prose";
import Layout from "../components/Layout";
import { DefaultSeo } from "next-seo";

const theme = extendTheme(withProse());

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <>
      <DefaultSeo
        titleTemplate="%s | Purée"
        defaultTitle="Purée"
        description="A quick and easy way to find regions that have been tagged."
        openGraph={{
          type: "website",
          locale: "en_US",
          url: "https://esfalsa.github.io/puree",
          site_name: "Purée",
        }}
        twitter={{
          handle: "@handle",
          site: "@site",
          cardType: "summary_large_image",
        }}
      />

      <ChakraProvider theme={theme}>
        <Layout>
          <Component {...pageProps} />
        </Layout>
      </ChakraProvider>
    </>
  );
}

export default MyApp;
