import { useEffect, useState } from "react";
import ButtonComponent from "../components/buttonComp";
import PageTemplate from "../components/pageTemplate";
import PlayerInformation from "../components/playerInformation";

export default function SwapPlayer() {
  const [playerInfo, setPlayerInfo] = useState("");

  useEffect(() => {}, []);
  return (
    <>
      <PageTemplate title="Playing 11">
        <div className="flex w-full">
          <div className="basis-1/4">
            <PlayerInformation title="Player Information" />
          </div>
          <div className="flex flex-col w-16 basis-3/4 text-white font-semibold tracking-wider p-4 px-24  text-xl leading-relaxed">
            <p>
              1. Learn about our loan products. We offer a wide range of loan products to choose from, so make sure you
              find one that meets your needs. Pay particular attention to loans with low interest rates.
            </p>
            <p>
              2. Fill out a loan application. You can fill out an application online, at a bank branch, or by calling
              us. Make sure to indicate on the application that you need a low-interest loan.
            </p>
            <p>
              3. Wait for a decision. We will review your application and let you know our decision within a few days.
              If your application is approved, you will receive a low-interest loan.
            </p>
          </div>
        </div>
      </PageTemplate>
      <div className="buttonCompDiv">
        <ButtonComponent>BACK</ButtonComponent>
        <ButtonComponent>SWAP</ButtonComponent>
      </div>
    </>
  );
}
