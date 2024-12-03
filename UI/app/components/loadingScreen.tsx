import Image from "next/image";
import PageTemplate from "./pageTemplate";

export default function LoadingScreen() {
  return (
    <div>
      <PageTemplate title="Playing 11" />
      <div className="loader-container">
        <Image src="/loading.gif" alt="Loading..." width={100} height={100} priority />
      </div>
    </div>
  );
}
