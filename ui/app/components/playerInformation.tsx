"use client";

import Image from "next/image";
import profilePhoto from "../../public/photo.png";
import teamPhoto from "../../public/chelsea.png";
import flagPhoto from "../../public/germany.png";

import React from 'react';

interface ButtonComponentProps {
  child1: React.ReactNode;
  child2: React.ReactNode;
  child3: React.ReactNode;
  child4: React.ReactNode;
}

function PlayerInformation({ child1, child2, child3, child4 }: ButtonComponentProps) {
  return (
    <div className="flex flex-col justify-center items-center uppercase w-30 h-full">
      <h1 className="uppercase text-dream11FontColor font-bold text-3xl tracking-widest mb-8">{child1}</h1>
      <div className="rounded-full border-dream11FontColor border-2 profilePhoto w-32 h-32 mb-8 flex items-center justify-center">
        <Image
          src={child3}
          alt="player"
          height={50}
          width={50}
          className=""
        />
      </div>
      <table className="text-dream11FontColor text-left">
        <tbody>
          <tr>
            <th>Team:</th>
            <th>Nationality:</th>
          </tr>
          <tr>
            <td>
              <Image src={child4} alt="player" width={50} height={50} />
            </td>

            <td>
              <Image src={child4} alt="player" width={50} height={50}/>
            </td>
          </tr>
          <tr>
            <th>Name:</th>
            <th>Position:</th>
          </tr>
          <tr>
            <td>{child2}</td>
            <td>19</td>
          </tr>
          <tr>
            <th>Overall Rating:</th>
            <th>Overall Rating:</th>
          </tr>
          <tr>
            <td>88</td>
            <td>25</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default PlayerInformation;
