"use client";

import { useEffect } from "react";
import { useSearchParams } from 'next/navigation';
import ButtonComponent from "../components/buttonComp";
import PageTemplate from "../components/pageTemplate";
import PlayerInformation from "../components/playerInformation";
import playersData from "../../public/players.json";
import countryImages from "../../public/countryImages.json";

export default function SwapPlayer() {
    const searchParams = useSearchParams();
    const id = searchParams.get('id');
    const image = searchParams.get('image');

    const prevPage = "/playing11";
    const nextPage = "/swap-player";

  useEffect(() => {}, []);
  return (
    <>
      <PageTemplate title="Playing 11">
        <div className="flex">
          <div className="playerShortDetails -ml-10 mt-12">
            <PlayerInformation 
              title="Player Information" 
              child2={playersData.players[id-1].name}
              child3={image}
              child4={countryImages.data[0].image_path}
            />
          </div>
          <div className="flex flex-col text-slate-300 w-[50rem] tracking-wider text-lg ml-[24rem] mb-[18rem] leading-relaxed overflow-scroll">
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
        <ButtonComponent nextPage={prevPage}>BACK</ButtonComponent>
        <ButtonComponent nextPage={nextPage}>SWAP</ButtonComponent>
      </div>
    </>
  );
}
