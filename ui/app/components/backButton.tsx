"use client";

import { useRouter } from "next/navigation";

function BackButtonComponent({ children }: { children: React.ReactNode }) {
  const router = useRouter();

  function handleClick() {
    router.back();
  }

  return (
    <button onClick={handleClick} className={"buttonComp backdrop-blur uppercase"}>
      {children}
    </button>
  );
}

export default BackButtonComponent;
