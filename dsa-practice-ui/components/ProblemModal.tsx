'use client';

import React, { useState, useMemo } from 'react';
import { Problem, Difficulty } from '@/lib/types';
import { X, Search, CheckCircle2, Circle, Filter } from 'lucide-react';

interface ProblemModalProps {
  isOpen: boolean;
  onClose: () => void;
  problems: Problem[];
  currentProblemId: string;
  onSelectProblem: (problem: Problem) => void;
  solvedIds: Set<string>;
}

export default function ProblemModal({
  isOpen,
  onClose,
  problems,
  currentProblemId,
  onSelectProblem,
  solvedIds,
}: ProblemModalProps) {
  const [search, setSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('All');

  // Extract unique categories
  const categories = useMemo(() => {
    const cats = Array.from(new Set(problems.map((p) => p.category))).sort();
    return ['All', ...cats];
  }, [problems]);

  // Filter problems
  const filteredProblems = useMemo(() => {
    return problems.filter((p) => {
      const matchesSearch =
        search.trim() === '' ||
        p.title.toLowerCase().includes(search.toLowerCase()) ||
        p.lcNumber.toString().includes(search.trim()) ||
        p.pattern.toLowerCase().includes(search.toLowerCase()) ||
        p.category.toLowerCase().includes(search.toLowerCase());

      const matchesCategory =
        selectedCategory === 'All' || p.category === selectedCategory;

      const matchesDifficulty =
        selectedDifficulty === 'All' || p.difficulty === selectedDifficulty;

      return matchesSearch && matchesCategory && matchesDifficulty;
    });
  }, [problems, search, selectedCategory, selectedDifficulty]);

  if (!isOpen) return null;

  const getDifficultyBadge = (diff: Difficulty) => {
    switch (diff) {
      case 'Easy':
        return 'text-[#00b8a3] bg-[#00b8a3]/10 border-[#00b8a3]/30';
      case 'Medium':
        return 'text-[#ffc01e] bg-[#ffc01e]/10 border-[#ffc01e]/30';
      case 'Hard':
        return 'text-[#ff375f] bg-[#ff375f]/10 border-[#ff375f]/30';
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4 animate-in fade-in duration-200">
      <div className="bg-[#1e1e1e] border border-[#3e3e3e] rounded-xl w-full max-w-4xl h-[85vh] flex flex-col shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-[#3e3e3e] bg-[#282828]">
          <div className="flex items-center gap-3">
            <h2 className="text-base font-bold text-white">DSA Practice Problems</h2>
            <span className="text-xs bg-[#3a3a3a] text-[#eff1f6] px-2.5 py-0.5 rounded-full font-mono">
              {solvedIds.size} / {problems.length} Solved
            </span>
          </div>
          <button
            onClick={onClose}
            className="p-1 text-[#8a8a8a] hover:text-white hover:bg-[#3a3a3a] rounded-lg transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Filter Toolbar */}
        <div className="p-4 bg-[#232323] border-b border-[#3e3e3e] flex flex-col sm:flex-row gap-3">
          {/* Search Box */}
          <div className="relative flex-1">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-[#8a8a8a]" />
            <input
              type="text"
              placeholder="Search by title, LC #, or pattern..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-[#181818] border border-[#3e3e3e] rounded-lg pl-9 pr-3 py-1.5 text-xs text-white placeholder-[#666] focus:outline-none focus:border-[#ffa116]"
            />
          </div>

          {/* Category Dropdown */}
          <div className="flex items-center gap-2">
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="bg-[#181818] border border-[#3e3e3e] text-xs text-white rounded-lg px-3 py-1.5 focus:outline-none focus:border-[#ffa116]"
            >
              {categories.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>

            {/* Difficulty Filter */}
            <div className="flex items-center gap-1 bg-[#181818] border border-[#3e3e3e] rounded-lg p-0.5 text-xs">
              {(['All', 'Easy', 'Medium', 'Hard'] as const).map((diff) => (
                <button
                  key={diff}
                  onClick={() => setSelectedDifficulty(diff)}
                  className={`px-2.5 py-1 rounded text-[11px] font-medium transition ${
                    selectedDifficulty === diff
                      ? 'bg-[#3a3a3a] text-white'
                      : 'text-[#8a8a8a] hover:text-white'
                  }`}
                >
                  {diff}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Problem List Table */}
        <div className="flex-1 overflow-y-auto scrollbar-thin scrollbar-thumb-[#3e3e3e]">
          <table className="w-full text-left text-xs border-collapse">
            <thead className="sticky top-0 bg-[#282828] text-[#8a8a8a] border-b border-[#3e3e3e] select-none font-medium">
              <tr>
                <th className="py-2.5 px-4 w-12 text-center">Status</th>
                <th className="py-2.5 px-3 w-16">#</th>
                <th className="py-2.5 px-4">Title</th>
                <th className="py-2.5 px-4 hidden md:table-cell">Category</th>
                <th className="py-2.5 px-4 hidden sm:table-cell">Pattern</th>
                <th className="py-2.5 px-4 w-24 text-right">Difficulty</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#2e2e2e]">
              {filteredProblems.length === 0 ? (
                <tr>
                  <td colSpan={6} className="text-center py-12 text-[#8a8a8a]">
                    No problems match your filters.
                  </td>
                </tr>
              ) : (
                filteredProblems.map((prob) => {
                  const isCurrent = prob.id === currentProblemId;
                  const isSolved = solvedIds.has(prob.id);

                  return (
                    <tr
                      key={prob.id}
                      onClick={() => {
                        onSelectProblem(prob);
                        onClose();
                      }}
                      className={`cursor-pointer transition hover:bg-[#2a2a2a] ${
                        isCurrent ? 'bg-[#333]/50' : ''
                      }`}
                    >
                      <td className="py-3 px-4 text-center">
                        {isSolved ? (
                          <CheckCircle2 className="w-4 h-4 text-[#2cbb5d] mx-auto" />
                        ) : (
                          <Circle className="w-4 h-4 text-[#444] mx-auto" />
                        )}
                      </td>
                      <td className="py-3 px-3 font-mono text-[#8a8a8a]">
                        {prob.lcNumber}
                      </td>
                      <td className="py-3 px-4">
                        <span
                          className={`font-semibold transition ${
                            isCurrent
                              ? 'text-[#ffa116]'
                              : 'text-white hover:text-[#ffa116]'
                          }`}
                        >
                          {prob.title}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-[#a0a0a0] hidden md:table-cell">
                        {prob.category}
                      </td>
                      <td className="py-3 px-4 text-[#8a8a8a] hidden sm:table-cell">
                        {prob.pattern}
                      </td>
                      <td className="py-3 px-4 text-right">
                        <span
                          className={`inline-block px-2 py-0.5 rounded-full border text-[10px] font-semibold ${getDifficultyBadge(
                            prob.difficulty
                          )}`}
                        >
                          {prob.difficulty}
                        </span>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>

        {/* Footer */}
        <div className="px-6 py-3 bg-[#232323] border-t border-[#3e3e3e] flex items-center justify-between text-xs text-[#8a8a8a]">
          <span>Showing {filteredProblems.length} of {problems.length} problems</span>
          <span>Click any row to open problem</span>
        </div>
      </div>
    </div>
  );
}
