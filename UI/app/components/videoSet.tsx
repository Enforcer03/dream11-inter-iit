"use client";

import { useRouter } from "next/navigation";

interface ButtonProps {
  children: React.ReactNode;
  nextPage: string;
}

function VideoComponent({ children, nextPage }: ButtonProps) {
  const router = useRouter();

  const handleClick = () => {
    router.push(nextPage);
  };

  return (
    <button onClick={handleClick} className="videoComp">
      <div className="videoCam"></div>
      {children}
    </button>
  );
}

export default VideoComponent;
