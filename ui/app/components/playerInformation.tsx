"use client";

import Image from "next/image";
import profilePhoto from "../../public/photo.png";
import teamPhoto from "../../public/chelsea.png";
import flagPhoto from "../../public/germany.png";

import React from "react";

interface ButtonComponentProps {
  title: string;
  child2?: React.ReactNode;
  child3?: React.ReactNode;
  child4?: React.ReactNode;
}

function PlayerInformation({ title, child3, child4, selectedPlayer, hoveredPlayer }: ButtonComponentProps) {
  return (
    <div className="flex flex-col justify-center items-center uppercase w-30 h-full">
      <h1 className="uppercase text-dream11FontColor font-bold text-3xl mb-8 ">{title}</h1>
      <div className="rounded-full border-dream11FontColor border-2 profilePhoto w-44 h-44 mb-8 flex items-center justify-center">
        <Image src={profilePhoto} alt="player" height={50} width={50} className="" />
      </div>
      <div className="flex align-center justify-center">
        <table className="text-dream11FontColor text-left">
          <tbody>
            <tr>
              <th>Team:</th>
              <th>Nationality:</th>
            </tr>
            <tr>
              <td>
                <Image src={teamPhoto} alt="player" width={50} height={50} />
              </td>

              <td>
                <Image src={flagPhoto} alt="player" width={50} height={50} />
              </td>
            </tr>
            <tr>
              <th>Name:</th>
              <th>Position:</th>
            </tr>
            <tr>
              <td>{selectedPlayer.name}</td>
              <td>19</td>
            </tr>
            <tr>
              <th>Overall Rating:</th>
              <th>Bowling Rating:</th>
            </tr>
            <tr>
              <td>
                {selectedPlayer.fitnessRating}{" "}
                <span>
                  {hoveredPlayer ? (
                    selectedPlayer.fitnessRating - hoveredPlayer.fitnessRating >= 0 ? (
                      <span className="text-green-500">
                        {"+ "}
                        {selectedPlayer.fitnessRating - hoveredPlayer.fitnessRating}
                      </span>
                    ) : (
                      <span className="text-red-500">
                        {"- "}
                        {hoveredPlayer.fitnessRating - selectedPlayer.fitnessRating}
                      </span>
                    )
                  ) : null}
                </span>
              </td>
              <td>
                {selectedPlayer.bowlingRating}{" "}
                <span>
                  {hoveredPlayer ? (
                    selectedPlayer.bowlingRating - hoveredPlayer.bowlingRating >= 0 ? (
                      <span className="text-green-500">
                        {"+ "}
                        {selectedPlayer.bowlingRating - hoveredPlayer.bowlingRating}
                      </span>
                    ) : (
                      <span className="text-red-500">
                        {"- "}
                        {hoveredPlayer.bowlingRating - selectedPlayer.bowlingRating}
                      </span>
                    )
                  ) : null}
                </span>
              </td>
            </tr>
            <tr>
              <th>Fielding Rating:</th>
              <th>Batting Rating:</th>
            </tr>
            <tr>
              <td>
                {selectedPlayer.fieldingRating}{" "}
                <span>
                  {hoveredPlayer ? (
                    selectedPlayer.fieldingRating - hoveredPlayer.fieldingRating >= 0 ? (
                      <span className="text-green-500">
                        {"+ "}
                        {selectedPlayer.fieldingRating - hoveredPlayer.fieldingRating}
                      </span>
                    ) : (
                      <span className="text-red-500">
                        {"- "}
                        {hoveredPlayer.fieldingRating - selectedPlayer.fieldingRating}
                      </span>
                    )
                  ) : null}
                </span>
              </td>
              <td>
                {selectedPlayer.battingRating}{" "}
                <span>
                  {hoveredPlayer ? (
                    selectedPlayer.battingRating - hoveredPlayer.battingRating >= 0 ? (
                      <span className="text-green-500">
                        {"+ "}
                        {selectedPlayer.battingRating - hoveredPlayer.battingRating}
                      </span>
                    ) : (
                      <span className="text-red-500">
                        {"- "}
                        {hoveredPlayer.battingRating - selectedPlayer.battingRating}
                      </span>
                    )
                  ) : null}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
export default PlayerInformation;
