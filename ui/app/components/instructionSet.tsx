"use client";

import React, { useEffect, useState } from 'react';

interface Instruction {
  id: number;
  text: string;
}

const Instructions: React.FC = () => {
  const [instructions, setInstructions] = useState<Instruction[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchInstructions = async () => {
      try {
        const response = await fetch('/instructions.txt');
        if (!response.ok) {
          throw new Error('Failed to load instructions');
        }

        const text = await response.text();
        const instructionsList = text.split('\n').map((line, index) => ({
          id: index + 1,
          text: line.trim(),
        }));

        setInstructions(instructionsList);
      } catch (error) {
        setError('There was an error fetching the instructions.');
      } finally {
        setLoading(false);
      }
    };

    fetchInstructions();
  }, []);

  if (loading) {
    return <p>Loading instructions...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <div className="instructions-container">
      <ul>
        {instructions.map((instruction) => (
          <li key={instruction.id}>{instruction.text}</li>
        ))}
      </ul>
    </div>
  );
};

export default Instructions;
