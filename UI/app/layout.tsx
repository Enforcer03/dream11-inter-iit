import type { Metadata } from "next";
import "./globals.css";

import { Quantico } from "next/font/google";
import { MatchDataProvider } from "./contexts/matchDataContext";

const quantico = Quantico({ weight: "400", subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Dream11 AI Team Predictor",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${quantico.className} antialiased`}>
        <MatchDataProvider>{children}</MatchDataProvider>
      </body>
    </html>
  );
}
