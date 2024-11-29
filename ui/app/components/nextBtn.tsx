"use client"

import { useRouter } from 'next/navigation';

interface ButtonProps {
  children: React.ReactNode;
  nextPage: string;
}

const NextButton = ({ children, nextPage }: ButtonProps) => {
  const router = useRouter();

  const handleClick = () => {
    router.push(nextPage);
  };

  return (
    <button onClick={handleClick} className="nextButton backdrop-blur uppercase ">
      {children}
    </button>
  );
};

export default NextButton;
