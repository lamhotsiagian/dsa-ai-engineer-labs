'use client';

import React from 'react';
import { Play, Check, ChevronLeft, ChevronRight, List } from 'lucide-react';
import { Problem } from '@/lib/types';
import CountdownTimer from './CountdownTimer';

interface NavbarProps {
  currentProblem: Problem;
  onOpenProblemList: () => void;
  onPrevProblem: () => void;
  onNextProblem: () => void;
  onRun: () => void;
  onSubmit: () => void;
  isRunning: boolean;
  onTimeExpired?: () => void;
}

export default function Navbar({
  currentProblem,
  onOpenProblemList,
  onPrevProblem,
  onNextProblem,
  onRun,
  onSubmit,
  isRunning,
  onTimeExpired,
}: NavbarProps) {
  const getDifficultyBadge = (diff: string) => {
    switch (diff) {
      case 'Easy':
        return 'text-[#00b8a3] bg-[#00b8a3]/10 border-[#00b8a3]/20';
      case 'Medium':
        return 'text-[#ffc01e] bg-[#ffc01e]/10 border-[#ffc01e]/20';
      case 'Hard':
        return 'text-[#ff375f] bg-[#ff375f]/10 border-[#ff375f]/20';
      default:
        return 'text-[#ffc01e] bg-[#ffc01e]/10 border-[#ffc01e]/20';
    }
  };

  return (
    <header className="h-12 bg-[#282828] border-b border-[#3e3e3e] px-4 flex items-center justify-between select-none text-sm text-[#eff1f6]">
      {/* Left: Logo & Problem Navigator */}
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 font-bold tracking-tight text-white cursor-pointer mr-2">
          <span className="bg-[#ffa116] text-black text-xs font-black px-1.5 py-0.5 rounded">DSA</span>
          <span className="hidden sm:inline font-semibold text-[#eff1f6]">AI Labs</span>
        </div>

        <button
          onClick={onOpenProblemList}
          className="flex items-center gap-1.5 bg-[#3a3a3a] hover:bg-[#4a4a4a] text-[#eff1f6] px-2.5 py-1 rounded transition text-xs font-medium"
          title="Browse all 150 problems"
        >
          <List className="w-3.5 h-3.5" />
          <span>Problem List</span>
        </button>

        <div className="flex items-center gap-1 text-[#8a8a8a]">
          <button
            onClick={onPrevProblem}
            className="p-1 hover:text-white hover:bg-[#3a3a3a] rounded transition"
            title="Previous Problem"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          <button
            onClick={onNextProblem}
            className="p-1 hover:text-white hover:bg-[#3a3a3a] rounded transition"
            title="Next Problem"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>

        {/* Current Problem Name & Badge */}
        <div className="flex items-center gap-1.5 sm:gap-2 ml-1">
          <span className="text-[#a0a0a0] font-mono text-xs">#{currentProblem.lcNumber}</span>
          <span className="font-semibold text-white max-w-[130px] sm:max-w-[200px] truncate">{currentProblem.title}</span>
          <span className={`text-[10px] px-2 py-0.5 rounded-full border font-medium ${getDifficultyBadge(currentProblem.difficulty)}`}>
            {currentProblem.difficulty}
          </span>
        </div>
      </div>

      {/* Center: Run & Submit Action Buttons */}
      <div className="flex items-center gap-2">
        <button
          onClick={onRun}
          disabled={isRunning}
          className="flex items-center gap-1.5 bg-[#3a3a3a] hover:bg-[#4a4a4a] active:scale-95 text-white px-3.5 py-1.5 rounded transition text-xs font-medium disabled:opacity-50"
          title="Run code against sample test cases (Cmd/Ctrl + Enter)"
        >
          <Play className="w-3.5 h-3.5 text-[#2cbb5d] fill-[#2cbb5d]" />
          <span>{isRunning ? 'Running...' : 'Run'}</span>
        </button>

        <button
          onClick={onSubmit}
          disabled={isRunning}
          className="flex items-center gap-1.5 bg-[#2cbb5d] hover:bg-[#28a745] active:scale-95 text-white px-4 py-1.5 rounded transition text-xs font-semibold shadow disabled:opacity-50"
          title="Submit solution for full validation"
        >
          <Check className="w-3.5 h-3.5" />
          <span>Submit</span>
        </button>
      </div>

      {/* Right: Countdown Challenge Timer */}
      <div className="flex items-center gap-3">
        <CountdownTimer
          difficulty={currentProblem.difficulty}
          problemId={currentProblem.id}
          onTimeExpired={onTimeExpired}
        />
      </div>
    </header>
  );
}
