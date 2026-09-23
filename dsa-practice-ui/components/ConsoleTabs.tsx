'use client';

import React, { useState, useEffect } from 'react';
import { TestCase, ExecutionResponse, CaseResult } from '@/lib/types';
import { CheckCircle2, XCircle, AlertTriangle, Terminal, Clock, Check, X } from 'lucide-react';

interface ConsoleTabsProps {
  testCases: TestCase[];
  result: ExecutionResponse | null;
  isRunning: boolean;
  activeMainTab: 'testcase' | 'result';
  setActiveMainTab: (tab: 'testcase' | 'result') => void;
}

export default function ConsoleTabs({
  testCases,
  result,
  isRunning,
  activeMainTab,
  setActiveMainTab,
}: ConsoleTabsProps) {
  const [selectedCaseIdx, setSelectedCaseIdx] = useState(0);

  // When a new result comes in, switch automatically to the result tab and select the first failed case (if any)
  useEffect(() => {
    if (result) {
      setActiveMainTab('result');
      if (result.results && result.results.length > 0) {
        const firstFailed = result.results.findIndex((r) => !r.passed);
        setSelectedCaseIdx(firstFailed !== -1 ? firstFailed : 0);
      }
    }
  }, [result, setActiveMainTab]);

  return (
    <div className="flex flex-col h-full bg-[#1e1e1e] text-[#eff1f6] select-text">
      {/* Console Top Tab Header */}
      <div className="flex items-center justify-between px-3 bg-[#282828] border-b border-[#3e3e3e] select-none h-9">
        <div className="flex items-center gap-1">
          <button
            onClick={() => setActiveMainTab('testcase')}
            className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-t transition border-b-2 ${
              activeMainTab === 'testcase'
                ? 'border-[#ffa116] text-white bg-[#1e1e1e]'
                : 'border-transparent text-[#8a8a8a] hover:text-[#cccccc]'
            }`}
          >
            <CheckCircle2 className="w-3.5 h-3.5 text-[#8a8a8a]" />
            <span>Testcase</span>
          </button>

          <button
            onClick={() => setActiveMainTab('result')}
            className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-t transition border-b-2 ${
              activeMainTab === 'result'
                ? 'border-[#ffa116] text-white bg-[#1e1e1e]'
                : 'border-transparent text-[#8a8a8a] hover:text-[#cccccc]'
            }`}
          >
            <Terminal className="w-3.5 h-3.5 text-[#3b82f6]" />
            <span>Test Result</span>
            {result && (
              <span
                className={`w-2 h-2 rounded-full ${
                  result.status === 'Accepted' ? 'bg-[#2cbb5d]' : 'bg-[#ef4444]'
                }`}
              />
            )}
          </button>
        </div>

        {isRunning && (
          <div className="flex items-center gap-1.5 text-xs text-[#ffa116] animate-pulse">
            <Clock className="w-3.5 h-3.5 animate-spin" />
            <span>Evaluating code...</span>
          </div>
        )}
      </div>

      {/* Console Content Body */}
      <div className="flex-1 overflow-y-auto p-4 scrollbar-thin scrollbar-thumb-[#3e3e3e]">
        {/* TESTCASE TAB */}
        {activeMainTab === 'testcase' && (
          <div className="space-y-4">
            {/* Case selector pills */}
            <div className="flex items-center gap-2">
              {testCases.map((tc, idx) => (
                <button
                  key={tc.id}
                  onClick={() => setSelectedCaseIdx(idx)}
                  className={`px-3 py-1 rounded text-xs font-medium transition ${
                    selectedCaseIdx === idx
                      ? 'bg-[#3a3a3a] text-white font-semibold'
                      : 'bg-[#262626] text-[#8a8a8a] hover:text-white'
                  }`}
                >
                  Case {idx + 1}
                </button>
              ))}
            </div>

            {/* Selected Case Inputs */}
            {testCases[selectedCaseIdx] && (
              <div className="space-y-3 font-mono text-xs">
                <div>
                  <div className="text-[#8a8a8a] text-[11px] mb-1">Input:</div>
                  <pre className="bg-[#262626] border border-[#3a3a3a] p-2.5 rounded text-[#eff1f6] whitespace-pre-wrap">
                    {testCases[selectedCaseIdx].inputDisplay}
                  </pre>
                </div>
                <div>
                  <div className="text-[#8a8a8a] text-[11px] mb-1">Expected Output:</div>
                  <pre className="bg-[#262626] border border-[#3a3a3a] p-2.5 rounded text-[#2cbb5d] whitespace-pre-wrap">
                    {testCases[selectedCaseIdx].expectedDisplay}
                  </pre>
                </div>
              </div>
            )}
          </div>
        )}

        {/* TEST RESULT TAB */}
        {activeMainTab === 'result' && (
          <div>
            {!result && !isRunning && (
              <div className="text-center py-8 text-[#8a8a8a] text-xs">
                <Terminal className="w-6 h-6 mx-auto mb-2 opacity-40" />
                <p>Run your code to see evaluation and test results.</p>
              </div>
            )}

            {isRunning && (
              <div className="text-center py-8 text-[#8a8a8a] text-xs">
                <Clock className="w-6 h-6 mx-auto mb-2 animate-spin text-[#ffa116]" />
                <p>Running test suite against sample test cases...</p>
              </div>
            )}

            {result && !isRunning && (
              <div className="space-y-4">
                {/* Result Status Banner */}
                <div className="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-[#333]">
                  <div className="flex items-center gap-2">
                    <span
                      className={`text-lg font-bold ${
                        result.status === 'Accepted'
                          ? 'text-[#2cbb5d]'
                          : result.status === 'Wrong Answer'
                          ? 'text-[#ef4444]'
                          : 'text-[#f59e0b]'
                      }`}
                    >
                      {result.status}
                    </span>
                    <span className="text-[#8a8a8a] text-xs font-mono ml-1">
                      Runtime: {result.runtimeMs} ms
                    </span>
                  </div>

                  <div className="text-xs text-[#8a8a8a]">
                    Passed: <span className="font-semibold text-white">{result.passedCount}</span> / {result.totalCount} Cases
                  </div>
                </div>

                {/* Global Error Banner (Compile Error / Syntax Error / Runtime Error) */}
                {result.error && (
                  <div className="space-y-1">
                    <div className="flex items-center gap-1.5 text-xs text-[#ef4444] font-semibold">
                      <AlertTriangle className="w-3.5 h-3.5" />
                      <span>Execution Traceback / Error:</span>
                    </div>
                    <pre className="bg-[#241414] border border-[#ef4444]/40 text-[#fca5a5] p-3 rounded font-mono text-xs overflow-x-auto whitespace-pre-wrap leading-relaxed">
                      {result.error}
                    </pre>
                  </div>
                )}

                {/* Case Selector Tabs */}
                {result.results && result.results.length > 0 && (
                  <div className="space-y-3">
                    <div className="flex items-center gap-2">
                      {result.results.map((c, idx) => (
                        <button
                          key={idx}
                          onClick={() => setSelectedCaseIdx(idx)}
                          className={`flex items-center gap-1.5 px-3 py-1 rounded text-xs font-medium transition ${
                            selectedCaseIdx === idx
                              ? 'bg-[#3a3a3a] text-white font-semibold'
                              : 'bg-[#262626] text-[#8a8a8a] hover:text-white'
                          }`}
                        >
                          {c.passed ? (
                            <Check className="w-3 h-3 text-[#2cbb5d]" />
                          ) : (
                            <X className="w-3 h-3 text-[#ef4444]" />
                          )}
                          <span>Case {idx + 1}</span>
                        </button>
                      ))}
                    </div>

                    {/* Case Detail comparison */}
                    {result.results[selectedCaseIdx] && (
                      <div className="space-y-3 font-mono text-xs">
                        <div>
                          <div className="text-[#8a8a8a] text-[11px] mb-1">Input:</div>
                          <pre className="bg-[#262626] border border-[#3a3a3a] p-2.5 rounded text-[#eff1f6] whitespace-pre-wrap">
                            {result.results[selectedCaseIdx].inputDisplay}
                          </pre>
                        </div>

                        <div>
                          <div className="text-[#8a8a8a] text-[11px] mb-1">Your Output:</div>
                          <pre
                            className={`p-2.5 rounded border whitespace-pre-wrap ${
                              result.results[selectedCaseIdx].passed
                                ? 'bg-[#262626] border-[#3a3a3a] text-[#2cbb5d]'
                                : 'bg-[#2a1717] border-[#ef4444]/40 text-[#fca5a5]'
                            }`}
                          >
                            {result.results[selectedCaseIdx].actualDisplay}
                          </pre>
                        </div>

                        <div>
                          <div className="text-[#8a8a8a] text-[11px] mb-1">Expected Output:</div>
                          <pre className="bg-[#262626] border border-[#3a3a3a] p-2.5 rounded text-[#2cbb5d] whitespace-pre-wrap">
                            {result.results[selectedCaseIdx].expectedDisplay}
                          </pre>
                        </div>

                        {/* Case stdout if any */}
                        {result.results[selectedCaseIdx].stdout && (
                          <div>
                            <div className="text-[#8a8a8a] text-[11px] mb-1">Stdout:</div>
                            <pre className="bg-[#181818] border border-[#333] p-2.5 rounded text-[#a0a0a0] whitespace-pre-wrap">
                              {result.results[selectedCaseIdx].stdout}
                            </pre>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                )}

                {/* Overall stdout if not captured per case */}
                {result.stdout && (
                  <div className="pt-2">
                    <div className="text-[#8a8a8a] text-[11px] mb-1 flex items-center gap-1">
                      <Terminal className="w-3 h-3" />
                      <span>Console Stdout:</span>
                    </div>
                    <pre className="bg-[#181818] border border-[#333] p-2.5 rounded font-mono text-xs text-[#a0a0a0] whitespace-pre-wrap">
                      {result.stdout}
                    </pre>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
