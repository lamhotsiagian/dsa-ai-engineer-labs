'use client';

import React, { useState } from 'react';
import { Problem, ExecutionResponse } from '@/lib/types';
import { BookOpen, FileText, CheckCircle2, ExternalLink, Copy, Check, Sparkles, Building, Layers } from 'lucide-react';

interface ProblemDescriptionProps {
  problem: Problem;
  lastResult: ExecutionResponse | null;
  activeTab?: 'description' | 'editorial' | 'submissions';
  onTabChange?: (tab: 'description' | 'editorial' | 'submissions') => void;
}

export default function ProblemDescription({
  problem,
  lastResult,
  activeTab: externalTab,
  onTabChange,
}: ProblemDescriptionProps) {
  const [internalTab, setInternalTab] = useState<'description' | 'editorial' | 'submissions'>('description');
  const activeTab = externalTab !== undefined ? externalTab : internalTab;
  const setActiveTab = (tab: 'description' | 'editorial' | 'submissions') => {
    if (onTabChange) onTabChange(tab);
    setInternalTab(tab);
  };
  const [copiedCode, setCopiedCode] = useState(false);

  const getDifficultyBadge = (diff: string) => {
    switch (diff) {
      case 'Easy':
        return 'text-[#00b8a3] bg-[#00b8a3]/10 border-[#00b8a3]/30';
      case 'Medium':
        return 'text-[#ffc01e] bg-[#ffc01e]/10 border-[#ffc01e]/30';
      case 'Hard':
        return 'text-[#ff375f] bg-[#ff375f]/10 border-[#ff375f]/30';
      default:
        return 'text-[#ffc01e] bg-[#ffc01e]/10 border-[#ffc01e]/30';
    }
  };

  const handleCopyEditorialCode = () => {
    if (!problem.editorial?.solutionCode) return;
    navigator.clipboard.writeText(problem.editorial.solutionCode);
    setCopiedCode(true);
    setTimeout(() => setCopiedCode(false), 2000);
  };

  return (
    <div className="flex flex-col h-full bg-[#1e1e1e] text-[#eff1f6] select-text overflow-hidden border-r border-[#3e3e3e]">
      {/* Tab Navigation */}
      <div className="flex items-center gap-1 px-3 pt-2 bg-[#282828] border-b border-[#3e3e3e] select-none">
        <button
          onClick={() => setActiveTab('description')}
          className={`flex items-center gap-1.5 px-3 py-2 text-xs font-medium rounded-t transition border-b-2 ${
            activeTab === 'description'
              ? 'border-[#ffa116] text-white bg-[#1e1e1e]'
              : 'border-transparent text-[#8a8a8a] hover:text-[#cccccc]'
          }`}
        >
          <FileText className="w-3.5 h-3.5 text-[#3b82f6]" />
          <span>Description</span>
        </button>

        <button
          onClick={() => setActiveTab('editorial')}
          className={`flex items-center gap-1.5 px-3 py-2 text-xs font-medium rounded-t transition border-b-2 ${
            activeTab === 'editorial'
              ? 'border-[#ffa116] text-white bg-[#1e1e1e]'
              : 'border-transparent text-[#8a8a8a] hover:text-[#cccccc]'
          }`}
        >
          <Sparkles className="w-3.5 h-3.5 text-[#ffa116]" />
          <span>Editorial & 5-Step Solution</span>
        </button>

        <button
          onClick={() => setActiveTab('submissions')}
          className={`flex items-center gap-1.5 px-3 py-2 text-xs font-medium rounded-t transition border-b-2 ${
            activeTab === 'submissions'
              ? 'border-[#ffa116] text-white bg-[#1e1e1e]'
              : 'border-transparent text-[#8a8a8a] hover:text-[#cccccc]'
          }`}
        >
          <CheckCircle2 className="w-3.5 h-3.5 text-[#2cbb5d]" />
          <span>Submissions</span>
        </button>
      </div>

      {/* Tab Body */}
      <div className="flex-1 overflow-y-auto p-5 scrollbar-thin scrollbar-thumb-[#3e3e3e] scrollbar-track-transparent">
        {activeTab === 'description' && (
          <div className="space-y-6">
            {/* Title Header */}
            <div>
              <div className="flex items-center justify-between gap-2">
                <h1 className="text-xl font-bold text-white tracking-tight">
                  {problem.lcNumber}. {problem.title}
                </h1>
                <a
                  href={`https://leetcode.com/problems/${problem.slug}/`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-1 text-xs text-[#8a8a8a] hover:text-[#ffa116] transition"
                  title="View on LeetCode"
                >
                  <span>LeetCode #{problem.lcNumber}</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              </div>

              {/* Badges & Meta */}
              <div className="flex flex-wrap items-center gap-2 mt-3 text-xs">
                <span className={`px-2.5 py-0.5 rounded-full border font-semibold ${getDifficultyBadge(problem.difficulty)}`}>
                  {problem.difficulty}
                </span>

                <span className="flex items-center gap-1 bg-[#2d2d2d] text-[#bfbfbf] border border-[#444] px-2.5 py-0.5 rounded-full">
                  <Layers className="w-3 h-3 text-[#ffa116]" />
                  <span>{problem.category}</span>
                </span>

                <span className="bg-[#2d2d2d] text-[#a0a0a0] border border-[#444] px-2.5 py-0.5 rounded-full">
                  Pattern: <span className="text-[#eff1f6] font-medium">{problem.pattern}</span>
                </span>

                {problem.companies && (
                  <span className="flex items-center gap-1 bg-[#2d2d2d] text-[#a0a0a0] border border-[#444] px-2.5 py-0.5 rounded-full">
                    <Building className="w-3 h-3 text-[#3b82f6]" />
                    <span className="text-[#eff1f6]">{problem.companies}</span>
                  </span>
                )}
              </div>
            </div>

            {/* Description Text */}
            <div className="text-sm leading-relaxed text-[#d4d4d4] whitespace-pre-line space-y-3 font-normal">
              {problem.description}
            </div>

            {/* Examples */}
            {problem.examples && problem.examples.length > 0 && (
              <div className="space-y-4 pt-2">
                <h2 className="text-sm font-semibold text-white tracking-wide uppercase text-opacity-80">
                  Examples
                </h2>
                {problem.examples.map((ex, idx) => (
                  <div key={idx} className="bg-[#262626] border border-[#3e3e3e] rounded-lg p-3.5 space-y-2 text-xs">
                    <div className="font-semibold text-white">Example {idx + 1}:</div>
                    <div className="font-mono space-y-1 text-[#eff1f6]">
                      <div>
                        <span className="text-[#8a8a8a]">Input: </span>
                        <span>{ex.input}</span>
                      </div>
                      <div>
                        <span className="text-[#8a8a8a]">Output: </span>
                        <span className="text-[#2cbb5d] font-semibold">{ex.output}</span>
                      </div>
                      {ex.explanation && (
                        <div>
                          <span className="text-[#8a8a8a]">Explanation: </span>
                          <span className="text-[#a0a0a0] font-sans">{ex.explanation}</span>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Constraints */}
            {problem.constraints && problem.constraints.length > 0 && (
              <div className="space-y-2 pt-2">
                <h2 className="text-sm font-semibold text-white tracking-wide uppercase text-opacity-80">
                  Constraints
                </h2>
                <ul className="list-disc list-inside space-y-1.5 text-xs text-[#a0a0a0] font-mono">
                  {problem.constraints.map((c, i) => (
                    <li key={i} className="leading-relaxed">
                      <span className="text-[#eff1f6] bg-[#2a2a2a] px-1 py-0.5 rounded">{c}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {activeTab === 'editorial' && (
          <div className="space-y-6 text-xs text-[#d4d4d4]">
            <div className="flex items-center justify-between pb-3 border-b border-[#3e3e3e]">
              <div>
                <h2 className="text-base font-bold text-white">5-Step DSA Framework Guide</h2>
                <p className="text-[#8a8a8a] text-xs mt-0.5">Structured systematic engineering analysis</p>
              </div>
              <button
                onClick={handleCopyEditorialCode}
                className="flex items-center gap-1.5 bg-[#2d2d2d] hover:bg-[#3d3d3d] text-white px-2.5 py-1.5 rounded transition font-medium"
              >
                {copiedCode ? <Check className="w-3.5 h-3.5 text-[#2cbb5d]" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copiedCode ? 'Copied' : 'Copy Solution'}</span>
              </button>
            </div>

            {/* Step 1 */}
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <span className="w-5 h-5 rounded-full bg-[#ffa116] text-black font-bold flex items-center justify-center text-[10px]">
                  1
                </span>
                <h3 className="font-semibold text-white text-sm">Step 1: Clarify Requirements & Constraints</h3>
              </div>
              <p className="bg-[#262626] border border-[#3e3e3e] p-3 rounded-lg leading-relaxed text-[#c0c0c0]">
                {problem.editorial?.step1 || 'Clarify data bounds, edge cases (empty input, negatives), and space requirements.'}
              </p>
            </div>

            {/* Step 2 */}
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <span className="w-5 h-5 rounded-full bg-[#3a3a3a] text-white font-bold flex items-center justify-center text-[10px]">
                  2
                </span>
                <h3 className="font-semibold text-white text-sm">Step 2: Brute Force Baseline</h3>
              </div>
              <p className="bg-[#262626] border border-[#3e3e3e] p-3 rounded-lg leading-relaxed text-[#c0c0c0]">
                {problem.editorial?.step2 || 'Exhaustive search approach to establish problem baseline.'}
              </p>
            </div>

            {/* Step 3 */}
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <span className="w-5 h-5 rounded-full bg-[#2cbb5d] text-white font-bold flex items-center justify-center text-[10px]">
                  3
                </span>
                <h3 className="font-semibold text-white text-sm">Step 3: Optimal Strategy & Algorithm</h3>
              </div>
              <p className="bg-[#262626] border border-[#3e3e3e] p-3 rounded-lg leading-relaxed text-[#c0c0c0]">
                {problem.editorial?.step3 || 'Optimized time-space algorithm leveraging data structure properties.'}
              </p>
            </div>

            {/* Step 5 */}
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <span className="w-5 h-5 rounded-full bg-[#3b82f6] text-white font-bold flex items-center justify-center text-[10px]">
                  4
                </span>
                <h3 className="font-semibold text-white text-sm">Complexity Analysis</h3>
              </div>
              <p className="bg-[#262626] border border-[#3e3e3e] p-3 rounded-lg font-mono text-[#a5b4fc]">
                {problem.editorial?.step5 || 'Time: O(N) | Space: O(1)'}
              </p>
            </div>

            {/* Reference Solution Code */}
            {problem.editorial?.solutionCode && (
              <div className="space-y-2">
                <h3 className="font-semibold text-white text-sm">Python Reference Implementation</h3>
                <pre className="bg-[#141414] border border-[#333] p-3.5 rounded-lg font-mono text-xs overflow-x-auto text-[#e0e0e0] leading-relaxed">
                  {problem.editorial.solutionCode}
                </pre>
              </div>
            )}
          </div>
        )}

        {activeTab === 'submissions' && (
          <div className="space-y-4 text-xs">
            <h2 className="text-sm font-bold text-white">Recent Session Submissions</h2>
            {lastResult ? (
              <div className="bg-[#262626] border border-[#3e3e3e] rounded-lg p-4 space-y-3">
                <div className="flex items-center justify-between">
                  <span
                    className={`font-bold text-sm ${
                      lastResult.status === 'Accepted'
                        ? 'text-[#2cbb5d]'
                        : lastResult.status === 'Wrong Answer'
                        ? 'text-[#ef4444]'
                        : 'text-[#f59e0b]'
                    }`}
                  >
                    {lastResult.status}
                  </span>
                  <span className="text-[#8a8a8a] font-mono">{lastResult.runtimeMs} ms</span>
                </div>
                <div className="text-[#a0a0a0]">
                  Passed: <span className="text-white font-semibold">{lastResult.passedCount} / {lastResult.totalCount}</span> test cases
                </div>
                {lastResult.error && (
                  <pre className="bg-[#141414] border border-[#ef4444]/40 text-[#ef4444] p-2.5 rounded font-mono text-[11px] overflow-x-auto">
                    {lastResult.error}
                  </pre>
                )}
              </div>
            ) : (
              <div className="text-center py-12 text-[#8a8a8a]">
                <BookOpen className="w-8 h-8 mx-auto mb-2 opacity-40" />
                <p>No submission in this session yet.</p>
                <p className="text-[11px] text-[#666] mt-1">Click "Submit" to test your solution across all test cases.</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
