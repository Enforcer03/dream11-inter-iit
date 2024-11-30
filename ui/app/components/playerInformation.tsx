"use client";

import Image from "next/image";
import React from "react";

interface ButtonComponentProps {
  title: string;
  child2?: React.ReactNode;
  child3?: React.ReactNode;
  child4?: React.ReactNode;
}

function PlayerInformation({ title, child2, child3, child4 }: ButtonComponentProps) {
  const formatName = (name: string) => {
    if (name.length > 13) {
      const words = name.split(' ');
      if (words.length > 1) {
        const initial = words[0][0] + '.';
        return initial + ' ' + words.slice(1).join(' ');
      }
    }
    return name;
  };

  const formattedChild2 = typeof child2 === 'string' ? formatName(child2) : child2;

  return (
    <div className="flex flex-col justify-center items-center uppercase w-[21rem] h-full">
      <h1 className="uppercase text-dream11FontColor font-bold text-3xl mb-4 ">{title}</h1>
      <div className="rounded-full border-2 profilePhoto w-44 h-44 mb-8 flex items-center justify-center">
        <Image src={child3} alt="player" height={180} width={180} />
      </div>
      <div className="flex align-center justify-center">
        <div className="text-left flex flex-col">
          <div className="flex justify-center mb-4">
              <Image src={child4} alt="player" width={60} height={50} />
          </div>
          <div className="flex flex-col w-[21rem] ml-24">
            <div className="flex text-dream11FontColor">
            <div className="font-bold w-1/2">Name:</div>
            <div className="font-bold">Role:</div>
          </div>
          <div className="flex mb-2 text-white">
            <div className="w-1/2">{formattedChild2}</div>
            <div className="w-1/2">19</div>
          </div>
          <div className="flex text-dream11FontColor">
            <div className="font-bold w-1/2">Batting S/R:</div>
            <div className="font-bold w-1/2">Runs:</div>
          </div>
          <div className="flex mb-2 text-white">
            <div className="w-1/2">88</div>
            <div className="w-1/2">25</div>
          </div>
          <div className="flex text-dream11FontColor">
            <div className="font-bold w-1/2">Batting Avg.:</div>
            <div className="font-bold w-1/2">Wickets:</div>
          </div>
          <div className="flex mb-2 text-white">
            <div className="w-1/2">88</div>
            <div className="w-1/2">25</div>
          </div>
          <div className="flex text-dream11FontColor">
            <div className="font-bold w-1/2">Economy Rate:</div>
            <div className="font-bold w-1/2">Bowling S/R:</div>
          </div>
          <div className="flex text-white">
            <div className="w-1/2">88</div>
            <div className="w-1/2">25</div>
        </div>
          </div>
      </div>
      </div>
    </div>
  );
}

export default PlayerInformation;