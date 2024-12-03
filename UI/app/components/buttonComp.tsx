"use client";

import { useRouter } from "next/navigation";
import html2canvas from "html2canvas";

interface ButtonProps {
  children: React.ReactNode;
  nextPage?: string;
  onClick?: () => void;
  disabled?: boolean;
  downloadScreenshot?: boolean;
}

const ButtonComponent = ({ children, nextPage, onClick, disabled, downloadScreenshot }: ButtonProps) => {
  const router = useRouter();

  const downloadScreenshotImage = async () => {
    try {
      const canvas = await html2canvas(document.body, {
        useCORS: true,
        allowTaint: true,
      });

      const dataUrl = canvas.toDataURL("image/png");

      const link = document.createElement("a");
      link.href = dataUrl;
      link.download = "screenshot.png";
      link.click();
    } catch (error) {
      console.error("Error capturing screenshot:", error);
    }
  };

  const handleClick = () => {
    if (disabled) return;

    if (downloadScreenshot) {
      downloadScreenshotImage();
    } else if (onClick) {
      onClick();
    } else if (nextPage) {
      router.push(nextPage);
    }
  };

  return (
    <button
      onClick={handleClick}
      disabled={disabled}
      className={`buttonComp backdrop-blur uppercase ${disabled ? "opacity-50 cursor-not-allowed" : ""}`}
    >
      {children}
    </button>
  );
};

export default ButtonComponent;
