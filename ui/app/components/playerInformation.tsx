"use client";
import Image from "next/image";
import ButtonComponent from "./buttonComp";
import profilePhoto from "../../public/photo.png";
import teamPhoto from "../../public/chelsea.png";
import flagPhoto from "../../public/germany.png";

export default function PlayerInformation({ title }: { title: string }) {
  return (
    <div className="flex flex-col justify-center items-center backdrop-blur-md uppercase w-full h-full">
      <h1 className="uppercase text-dream11FontColor font-bold text-5xl tracking-widest">{title}</h1>
      <Image
        src={profilePhoto}
        alt="player"
        width={300}
        className="rounded-full border-dream11FontColor border-2 profilePhoto"
      />
      <table className="text-dream11FontColor text-left">
        <tbody>
          <tr>
            <th>Team:</th>
            <th>Nationality:</th>
          </tr>
          <tr>
            <td>
              <Image src={teamPhoto} alt="player" width={100} />
            </td>

            <td>
              <Image src={flagPhoto} alt="player" width={100} />
            </td>
          </tr>
          <tr>
            <th>Name:</th>
            <th>Position:</th>
          </tr>
          <tr>
            <td>Anom</td>
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
      <ButtonComponent>Finalize</ButtonComponent>
      <ButtonComponent>Back</ButtonComponent>
    </div>
  );
}
