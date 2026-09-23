'use client';

import React, { useState, useEffect, useCallback } from 'react';
import Navbar from '@/components/Navbar';
import ProblemDescription from '@/components/ProblemDescription';
import CodeEditor from '@/components/CodeEditor';
import ConsoleTabs from '@/components/ConsoleTabs';
import ProblemModal from '@/components/ProblemModal';
import { ALL_PROBLEMS, DEFAULT_PROBLEM } from '@/lib/problems';
import { Problem, ExecutionResponse } from '@/lib/types';
import { Sparkles, X } from 'lucide-react';

export default function Home() {
  const [problems] = useState<Problem[]>(ALL_PROBLEMS);
  const [currentProblem, setCurrentProblem] = useState<Problem>(DEFAULT_PROBLEM);
  const [code, setCode] = useState<string>('');
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [result, setResult] = useState<ExecutionResponse | null>(null);
  const [activeConsoleTab, setActiveConsoleTab] = useState<'testcase' | 'result'>('testcase');
  const [activeDescTab, setActiveDescTab] = useState<'description' | 'editorial' | 'submissions'>('description');
  const [isProblemModalOpen, setIsProblemModalOpen] = useState<boolean>(false);
  const [solvedIds, setSolvedIds] = useState<Set<string>>(new Set());
  const [showTimeExpiredBanner, setShowTimeExpiredBanner] = useState<boolean>(false);

  // Load solved problems from localStorage on mount
  useEffect(() => {
    try {
      const savedSolved = localStorage.getItem('dsa_solved_problems');
      if (savedSolved) {
        setSolvedIds(new Set(JSON.parse(savedSolved)));
      }
      const lastProbId = localStorage.getItem('dsa_last_problem_id');
      if (lastProbId) {
        const found = ALL_PROBLEMS.find((p) => p.id === lastProbId);
        if (found) {
          setCurrentProblem(found);
        }
      }
    } catch (e) {
      console.error('Error loading saved state:', e);
    }
  }, []);

  // Update code when problem changes (loading from localStorage if previously edited)
  useEffect(() => {
    if (!currentProblem || !currentProblem.id) return;
    try {
      const savedCode = localStorage.getItem(`dsa_code_${currentProblem.id}`);
      if (savedCode !== null && savedCode.trim() !== '') {
        setCode(savedCode);
      } else {
        setCode(currentProblem.starterCode || '');
      }
      localStorage.setItem('dsa_last_problem_id', currentProblem.id);
    } catch {
      setCode(currentProblem.starterCode || '');
    }
    setResult(null);
    setActiveConsoleTab('testcase');
    setActiveDescTab('description');
    setShowTimeExpiredBanner(false);
  }, [currentProblem]);

  // Save code changes to localStorage
  const handleCodeChange = (newCode: string) => {
    setCode(newCode);
    if (currentProblem && currentProblem.id) {
      try {
        localStorage.setItem(`dsa_code_${currentProblem.id}`, newCode);
      } catch (e) {
        console.error('Error saving code:', e);
      }
    }
  };

  // Reset code to starter template
  const handleResetCode = () => {
    if (!currentProblem) return;
    setCode(currentProblem.starterCode);
    try {
      localStorage.removeItem(`dsa_code_${currentProblem.id}`);
    } catch (e) {
      console.error(e);
    }
  };

  // Run code against sample test cases
  const handleRun = useCallback(async () => {
    if (isRunning || !currentProblem) return;
    setIsRunning(true);
    setActiveConsoleTab('result');

    try {
      const res = await fetch('/api/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          code,
          testCases: currentProblem.testCases.slice(0, 3), // sample test cases
          entryFunction: currentProblem.entryFunction,
          slug: currentProblem.slug,
        }),
      });

      const data: ExecutionResponse = await res.json();
      setResult(data);

      if (data.status === 'Accepted') {
        setSolvedIds((prev) => {
          const next = new Set(prev);
          next.add(currentProblem.id);
          try {
            localStorage.setItem('dsa_solved_problems', JSON.stringify(Array.from(next)));
          } catch {}
          return next;
        });
      }
    } catch (err: any) {
      setResult({
        status: 'Runtime Error',
        runtimeMs: 0,
        passedCount: 0,
        totalCount: currentProblem.testCases.length,
        results: [],
        error: err.message || 'Network or execution failure',
      });
    } finally {
      setIsRunning(false);
    }
  }, [isRunning, currentProblem, code]);

  // Submit code against all test cases
  const handleSubmit = useCallback(async () => {
    if (isRunning || !currentProblem) return;
    setIsRunning(true);
    setActiveConsoleTab('result');

    try {
      const res = await fetch('/api/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          code,
          testCases: currentProblem.testCases, // all test cases
          entryFunction: currentProblem.entryFunction,
          slug: currentProblem.slug,
        }),
      });

      const data: ExecutionResponse = await res.json();
      setResult(data);

      if (data.status === 'Accepted') {
        setSolvedIds((prev) => {
          const next = new Set(prev);
          next.add(currentProblem.id);
          try {
            localStorage.setItem('dsa_solved_problems', JSON.stringify(Array.from(next)));
          } catch {}
          return next;
        });
      }
    } catch (err: any) {
      setResult({
        status: 'Runtime Error',
        runtimeMs: 0,
        passedCount: 0,
        totalCount: currentProblem.testCases.length,
        results: [],
        error: err.message || 'Submission failure',
      });
    } finally {
      setIsRunning(false);
    }
  }, [isRunning, currentProblem, code]);

  // Keyboard shortcut listener: Cmd/Ctrl + Enter to Run
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
        e.preventDefault();
        handleRun();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleRun]);

  // Navigation handlers
  const currentIndex = problems.findIndex((p) => p.id === currentProblem.id);

  const handlePrevProblem = () => {
    if (currentIndex > 0) {
      setCurrentProblem(problems[currentIndex - 1]);
    } else {
      setCurrentProblem(problems[problems.length - 1]);
    }
  };

  const handleNextProblem = () => {
    if (currentIndex < problems.length - 1) {
      setCurrentProblem(problems[currentIndex + 1]);
    } else {
      setCurrentProblem(problems[0]);
    }
  };

  const handleSelectProblem = (prob: Problem) => {
    setCurrentProblem(prob);
  };

  if (!currentProblem || !currentProblem.id) {
    return (
      <div className="flex items-center justify-center h-screen bg-[#1a1a1a] text-white">
        Loading problem set...
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen w-screen overflow-hidden bg-[#1a1a1a]">
      {/* Top Navbar with Countdown Timer */}
      <Navbar
        currentProblem={currentProblem}
        onOpenProblemList={() => setIsProblemModalOpen(true)}
        onPrevProblem={handlePrevProblem}
        onNextProblem={handleNextProblem}
        onRun={handleRun}
        onSubmit={handleSubmit}
        isRunning={isRunning}
        onTimeExpired={() => setShowTimeExpiredBanner(true)}
      />

      {/* Time Expired Challenge Alert Banner */}
      {showTimeExpiredBanner && (
        <div className="bg-[#38161c] border-b border-[#ff375f]/50 px-4 py-2 flex items-center justify-between text-xs text-[#eff1f6] animate-in slide-in-from-top-2">
          <div className="flex items-center gap-2">
            <span className="bg-[#ff375f] text-white px-2 py-0.5 rounded font-bold text-[10px] tracking-wide">
              TIME'S UP!
            </span>
            <span className="text-[#fca5a5]">
              Target time limit reached for this problem. Don't worry — review the 5-Step Editorial & Solution to solidify the pattern!
            </span>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => {
                setActiveDescTab('editorial');
                setShowTimeExpiredBanner(false);
              }}
              className="flex items-center gap-1 bg-[#ffa116] hover:bg-[#ff9000] text-black font-semibold px-2.5 py-1 rounded transition text-xs"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>View 5-Step Editorial</span>
            </button>
            <button
              onClick={() => setShowTimeExpiredBanner(false)}
              className="text-[#999] hover:text-white p-1 rounded transition"
              title="Dismiss"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* Main Workspace Split Layout */}
      <div className="flex-1 flex flex-col md:flex-row overflow-hidden">
        {/* Left Column: Problem Description & Editorial */}
        <div className="w-full md:w-[46%] h-1/2 md:h-full flex flex-col min-w-[320px]">
          <ProblemDescription
            problem={currentProblem}
            lastResult={result}
            activeTab={activeDescTab}
            onTabChange={setActiveDescTab}
          />
        </div>

        {/* Right Column: Code Editor & Console Output */}
        <div className="w-full md:w-[54%] h-1/2 md:h-full flex flex-col">
          {/* Top Half: Code Editor */}
          <div className="h-[60%] flex flex-col min-h-[220px]">
            <CodeEditor
              code={code}
              onChange={handleCodeChange}
              onReset={handleResetCode}
            />
          </div>

          {/* Bottom Half: Interactive Console & Test Results */}
          <div className="h-[40%] flex flex-col min-h-[160px]">
            <ConsoleTabs
              testCases={currentProblem.testCases || []}
              result={result}
              isRunning={isRunning}
              activeMainTab={activeConsoleTab}
              setActiveMainTab={setActiveConsoleTab}
            />
          </div>
        </div>
      </div>

      {/* Problem Browser Modal */}
      <ProblemModal
        isOpen={isProblemModalOpen}
        onClose={() => setIsProblemModalOpen(false)}
        problems={problems}
        currentProblemId={currentProblem.id}
        onSelectProblem={handleSelectProblem}
        solvedIds={solvedIds}
      />
    </div>
  );
}
