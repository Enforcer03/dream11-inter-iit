import React from 'react';

interface ButtonComponentProps {
  child1: React.ReactNode;
  child2: React.ReactNode;
}

function ButtonComponent({ child1, child2 }: ButtonComponentProps) {
  return (
    <div className="flex flex-col items-center justify-center">
      <div className='my-1 bgSelectedPlayer'>{child1}</div>

      <div className="my-1 anonymousPlayerText">{child2}</div>
    </div>
  );
}

export default ButtonComponent;
