"use client";

import { useRouter } from 'next/navigation';
import html2canvas from 'html2canvas';

interface ButtonProps {
  children: React.ReactNode;
  nextPage?: string;
  downloadScreenshot?: boolean;
}

const ButtonComponent = ({ children, nextPage, downloadScreenshot }: ButtonProps) => {
  const router = useRouter();

  const downloadScreenshotImage = async () => {
    try {
      const canvas = await html2canvas(document.body, {
        useCORS: true,
        allowTaint: true,
      });

      const dataUrl = canvas.toDataURL('image/png');

      const link = document.createElement('a');
      link.href = dataUrl;
      link.download = 'screenshot.png';
      link.click();
    } catch (error) {
      console.error('Error capturing screenshot:', error);
    }
  };

  const handleClick = () => {
    if (downloadScreenshot) {
      downloadScreenshotImage();
    } else {
      router.push(nextPage)
    }
  };

  return (
    <button onClick={handleClick} className="buttonComp backdrop-blur uppercase">
      {children}
    </button>
  );
};

export default ButtonComponent;
