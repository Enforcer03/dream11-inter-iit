import React from "react";

interface SelectedPlayerProps {
  child1: React.ReactNode;
  child2: React.ReactNode;
}

function SelectedPlayer({ child1, child2 }: SelectedPlayerProps) {
  return (
    <div className="flex flex-col flex-wrap w-20">
      <div className="my-1 bgInfoReportPlayer">{child1}</div>

      <div className="my-1 anonymousPlayerText">{child2}</div>
    </div>
  );
}

export default SelectedPlayer;
