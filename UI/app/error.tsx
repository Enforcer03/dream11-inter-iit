"use client";

import { useEffect } from "react";
import PageTemplateWithoutTop from "./components/pageTemplateNoTop";
import ButtonComponent from "./components/buttonComp";

export default function Error({ error, reset }: { error: Error & { digest?: string }; reset: () => void }) {
  useEffect(() => {
    // Optionally log the error to an error reporting service
    console.error(error);
  }, [error]);

  return (
    <PageTemplateWithoutTop>
      <div className="flex w-full h-full flex-col justify-center items-center">
        <p className="text-center uppercase text-4xl text-dream11FontColor">OOPS! Something went wrong!</p>
        <div className="mt-10">
          <ButtonComponent nextPage="/">Back to home</ButtonComponent>
        </div>
      </div>
    </PageTemplateWithoutTop>
  );
}
