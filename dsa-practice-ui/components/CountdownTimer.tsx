'use client';

import React, { useState, useEffect, useRef } from 'react';
import { Difficulty } from '@/lib/types';
import {
  Timer,
  Pause,
  Play,
  RotateCcw,
  Plus,
  ChevronDown,
  Volume2,
  VolumeX,
  AlertCircle,
  Zap,
  GraduationCap,
  Trophy,
} from 'lucide-react';

export type ChallengeTier = 'beginner' | 'intermediate' | 'advanced' | 'stopwatch';

export const TIER_CONFIG: Record<
  Exclude<ChallengeTier, 'stopwatch'>,
  {
    name: string;
    label: string;
    sublabel: string;
    icon: any;
    times: Record<Difficulty, number>; // in seconds
  }
> = {
  beginner: {
    name: 'Beginner',
    label: 'Beginner (Just Starting Out)',
    sublabel: 'Easy: 30m · Medium: 45m · Hard: 1h',
    icon: GraduationCap,
    times: {
      Easy: 30 * 60,   // 30 mins
      Medium: 45 * 60, // 45 mins
      Hard: 60 * 60,   // 60 mins
    },
  },
  intermediate: {
    name: 'Intermediate',
    label: 'Intermediate (Pattern Mastery)',
    sublabel: 'Easy: 20m · Medium: 35m · Hard: 50m',
    icon: Zap,
    times: {
      Easy: 20 * 60,   // 20 mins
      Medium: 35 * 60, // 35 mins
      Hard: 50 * 60,   // 50 mins
    },
  },
  advanced: {
    name: 'Interview Ready',
    label: 'Advanced (Interview Simulation)',
    sublabel: 'Easy: 15m · Medium: 25m · Hard: 45m',
    icon: Trophy,
    times: {
      Easy: 15 * 60,   // 15 mins
      Medium: 25 * 60, // 25 mins
      Hard: 45 * 60,   // 45 mins
    },
  },
};

interface CountdownTimerProps {
  difficulty: Difficulty;
  problemId: string;
  onTimeExpired?: () => void;
}

export default function CountdownTimer({
  difficulty,
  problemId,
  onTimeExpired,
}: CountdownTimerProps) {
  const [tier, setTier] = useState<ChallengeTier>('intermediate');
  const [seconds, setSeconds] = useState<number>(20 * 60);
  const [totalSeconds, setTotalSeconds] = useState<number>(20 * 60);
  const [isRunning, setIsRunning] = useState<boolean>(true);
  const [isExpired, setIsExpired] = useState<boolean>(false);
  const [soundEnabled, setSoundEnabled] = useState<boolean>(true);
  const [isOpenMenu, setIsOpenMenu] = useState<boolean>(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const hasChimedRef = useRef<boolean>(false);

  // Load user's preferred challenge tier from localStorage
  useEffect(() => {
    try {
      const savedTier = localStorage.getItem('dsa_timer_tier') as ChallengeTier;
      if (savedTier && (savedTier in TIER_CONFIG || savedTier === 'stopwatch')) {
        setTier(savedTier);
      }
      const savedSound = localStorage.getItem('dsa_timer_sound');
      if (savedSound !== null) {
        setSoundEnabled(savedSound === 'true');
      }
    } catch {}
  }, []);

  // Web Audio chime generator
  const playSoundChime = (type: 'warning' | 'expired') => {
    if (!soundEnabled || typeof window === 'undefined') return;
    try {
      const AudioCtx = window.AudioContext || (window as any).webkitAudioContext;
      if (!AudioCtx) return;
      const ctx = new AudioCtx();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.connect(gain);
      gain.connect(ctx.destination);

      if (type === 'expired') {
        // Double pulse chime
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(440, ctx.currentTime);
        osc.frequency.setValueAtTime(349.23, ctx.currentTime + 0.2);
        gain.gain.setValueAtTime(0.2, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.7);
        osc.start();
        osc.stop(ctx.currentTime + 0.7);
      } else {
        // Warning chime
        osc.type = 'sine';
        osc.frequency.setValueAtTime(587.33, ctx.currentTime);
        gain.gain.setValueAtTime(0.15, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.5);
        osc.start();
        osc.stop(ctx.currentTime + 0.5);
      }
    } catch {}
  };

  // Reset timer whenever problem or tier changes
  useEffect(() => {
    hasChimedRef.current = false;
    setIsExpired(false);
    setIsRunning(true);

    if (tier === 'stopwatch') {
      setSeconds(0);
      setTotalSeconds(0);
    } else {
      const config = TIER_CONFIG[tier];
      const alloc = config.times[difficulty] || 20 * 60;
      setSeconds(alloc);
      setTotalSeconds(alloc);
    }
  }, [problemId, difficulty, tier]);

  // Main countdown / countup tick loop
  useEffect(() => {
    let interval: any = null;

    if (isRunning) {
      interval = setInterval(() => {
        if (tier === 'stopwatch') {
          setSeconds((prev) => prev + 1);
        } else {
          setSeconds((prev) => {
            if (prev <= 1) {
              clearInterval(interval);
              setIsExpired(true);
              if (!hasChimedRef.current) {
                hasChimedRef.current = true;
                playSoundChime('expired');
                onTimeExpired?.();
              }
              return 0;
            }
            if (prev === 61 && !hasChimedRef.current) {
              playSoundChime('warning');
            }
            return prev - 1;
          });
        }
      }, 1000);
    }

    return () => clearInterval(interval);
  }, [isRunning, tier, soundEnabled]);

  // Close dropdown on outside click
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setIsOpenMenu(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSelectTier = (newTier: ChallengeTier) => {
    setTier(newTier);
    try {
      localStorage.setItem('dsa_timer_tier', newTier);
    } catch {}
    setIsOpenMenu(false);
  };

  const handleToggleSound = () => {
    const next = !soundEnabled;
    setSoundEnabled(next);
    try {
      localStorage.setItem('dsa_timer_sound', String(next));
    } catch {}
  };

  const handleAddFiveMinutes = () => {
    if (tier !== 'stopwatch') {
      setSeconds((prev) => prev + 300);
      setTotalSeconds((prev) => prev + 300);
      setIsExpired(false);
      hasChimedRef.current = false;
      setIsRunning(true);
    }
  };

  const handleReset = () => {
    hasChimedRef.current = false;
    setIsExpired(false);
    setIsRunning(true);
    if (tier === 'stopwatch') {
      setSeconds(0);
    } else {
      const alloc = TIER_CONFIG[tier].times[difficulty] || 20 * 60;
      setSeconds(alloc);
      setTotalSeconds(alloc);
    }
  };

  // Format seconds into HH:MM:SS or MM:SS
  const formatTime = (totalSecs: number) => {
    const hrs = Math.floor(totalSecs / 3600);
    const mins = Math.floor((totalSecs % 3600) / 60);
    const secs = totalSecs % 60;

    if (hrs > 0) {
      return `${hrs}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  // Color calculation
  const isUrgent = tier !== 'stopwatch' && !isExpired && seconds <= 180; // <= 3 minutes
  const isCritical = tier !== 'stopwatch' && !isExpired && seconds <= 60; // <= 1 minute

  const getTimerColorClass = () => {
    if (tier === 'stopwatch') return 'text-[#eff1f6]';
    if (isExpired) return 'text-[#ff375f] font-bold animate-pulse';
    if (isCritical) return 'text-[#ff375f] font-bold animate-pulse';
    if (isUrgent) return 'text-[#ffc01e] font-semibold';
    return 'text-[#eff1f6]';
  };

  return (
    <div className="relative flex items-center select-none" ref={menuRef}>
      {/* Timer Bar Box */}
      <div
        className={`flex items-center gap-1.5 px-2.5 py-1 rounded text-xs transition border ${
          isExpired
            ? 'bg-[#3b1219] border-[#ff375f]/50'
            : isCritical
            ? 'bg-[#331c1c] border-[#ff375f]/40'
            : isUrgent
            ? 'bg-[#2d2516] border-[#ffc01e]/30'
            : 'bg-[#1e1e1e] border-[#3e3e3e]'
        }`}
      >
        <button
          onClick={() => setIsOpenMenu(!isOpenMenu)}
          className="flex items-center gap-1 text-[#a0a0a0] hover:text-white transition mr-0.5"
          title="Change challenge time limits"
        >
          <Timer
            className={`w-3.5 h-3.5 ${
              isExpired
                ? 'text-[#ff375f]'
                : isCritical
                ? 'text-[#ff375f]'
                : isUrgent
                ? 'text-[#ffc01e]'
                : 'text-[#ffa116]'
            }`}
          />
          <ChevronDown className="w-3 h-3 text-[#777]" />
        </button>

        {/* Formatted Countdown Text */}
        <span className={`font-mono text-xs tracking-wider ${getTimerColorClass()}`}>
          {isExpired ? "00:00 (Time's Up!)" : formatTime(seconds)}
        </span>

        {/* Play/Pause Button */}
        <button
          onClick={() => setIsRunning(!isRunning)}
          className="hover:text-white ml-1 text-[#8a8a8a] p-0.5 rounded transition"
          title={isRunning ? 'Pause timer' : 'Resume timer'}
        >
          {isRunning ? (
            <Pause className="w-3 h-3" />
          ) : (
            <Play className="w-3 h-3 fill-current text-[#2cbb5d]" />
          )}
        </button>

        {/* Reset Button */}
        <button
          onClick={handleReset}
          className="hover:text-white text-[#8a8a8a] p-0.5 rounded transition"
          title="Reset timer for current problem"
        >
          <RotateCcw className="w-3 h-3" />
        </button>

        {/* +5 Minutes Extension Button */}
        {tier !== 'stopwatch' && (
          <button
            onClick={handleAddFiveMinutes}
            className="flex items-center text-[10px] bg-[#2a2a2a] hover:bg-[#3a3a3a] text-[#a0a0a0] hover:text-white px-1.5 py-0.5 rounded transition ml-0.5"
            title="Add +5 minutes"
          >
            <Plus className="w-2.5 h-2.5" />
            <span>5m</span>
          </button>
        )}
      </div>

      {/* Settings / Tier Selection Popover */}
      {isOpenMenu && (
        <div className="absolute right-0 top-full mt-2 w-80 bg-[#242424] border border-[#3e3e3e] rounded-xl shadow-2xl z-50 p-3 space-y-3 animate-in fade-in zoom-in-95 duration-150">
          <div className="flex items-center justify-between pb-2 border-b border-[#3e3e3e]">
            <div className="flex items-center gap-1.5 font-semibold text-xs text-white">
              <Timer className="w-3.5 h-3.5 text-[#ffa116]" />
              <span>Challenge Target Time</span>
            </div>
            <button
              onClick={handleToggleSound}
              className="text-[#8a8a8a] hover:text-white p-1 rounded hover:bg-[#333] transition"
              title={soundEnabled ? 'Mute chimes' : 'Enable chimes'}
            >
              {soundEnabled ? (
                <Volume2 className="w-3.5 h-3.5 text-[#2cbb5d]" />
              ) : (
                <VolumeX className="w-3.5 h-3.5 text-[#666]" />
              )}
            </button>
          </div>

          {/* Tier options */}
          <div className="space-y-1.5">
            {/* Beginner */}
            <button
              onClick={() => handleSelectTier('beginner')}
              className={`w-full text-left p-2.5 rounded-lg border transition flex items-start gap-2.5 ${
                tier === 'beginner'
                  ? 'bg-[#332b1a] border-[#ffa116]/60 text-white'
                  : 'bg-[#1e1e1e] border-[#333] text-[#aaa] hover:bg-[#282828] hover:text-white'
              }`}
            >
              <GraduationCap className="w-4 h-4 text-[#ffa116] shrink-0 mt-0.5" />
              <div>
                <div className="text-xs font-semibold text-white">Beginner (Just Starting Out)</div>
                <div className="text-[11px] text-[#888] mt-0.5">
                  Easy: <span className="text-[#00b8a3]">30m</span> · Medium: <span className="text-[#ffc01e]">45m</span> · Hard: <span className="text-[#ff375f]">1h</span>
                </div>
              </div>
            </button>

            {/* Intermediate */}
            <button
              onClick={() => handleSelectTier('intermediate')}
              className={`w-full text-left p-2.5 rounded-lg border transition flex items-start gap-2.5 ${
                tier === 'intermediate'
                  ? 'bg-[#332b1a] border-[#ffa116]/60 text-white'
                  : 'bg-[#1e1e1e] border-[#333] text-[#aaa] hover:bg-[#282828] hover:text-white'
              }`}
            >
              <Zap className="w-4 h-4 text-[#3b82f6] shrink-0 mt-0.5" />
              <div>
                <div className="text-xs font-semibold text-white">Intermediate (Pattern Mastery)</div>
                <div className="text-[11px] text-[#888] mt-0.5">
                  Easy: <span className="text-[#00b8a3]">20m</span> · Medium: <span className="text-[#ffc01e]">35m</span> · Hard: <span className="text-[#ff375f]">50m</span>
                </div>
              </div>
            </button>

            {/* Advanced */}
            <button
              onClick={() => handleSelectTier('advanced')}
              className={`w-full text-left p-2.5 rounded-lg border transition flex items-start gap-2.5 ${
                tier === 'advanced'
                  ? 'bg-[#332b1a] border-[#ffa116]/60 text-white'
                  : 'bg-[#1e1e1e] border-[#333] text-[#aaa] hover:bg-[#282828] hover:text-white'
              }`}
            >
              <Trophy className="w-4 h-4 text-[#ffc01e] shrink-0 mt-0.5" />
              <div>
                <div className="text-xs font-semibold text-white">Advanced / Interview Ready</div>
                <div className="text-[11px] text-[#888] mt-0.5">
                  Easy: <span className="text-[#00b8a3]">15m</span> · Medium: <span className="text-[#ffc01e]">25m</span> · Hard: <span className="text-[#ff375f]">45m</span>
                </div>
              </div>
            </button>

            {/* Free Stopwatch */}
            <button
              onClick={() => handleSelectTier('stopwatch')}
              className={`w-full text-left p-2.5 rounded-lg border transition flex items-start gap-2.5 ${
                tier === 'stopwatch'
                  ? 'bg-[#332b1a] border-[#ffa116]/60 text-white'
                  : 'bg-[#1e1e1e] border-[#333] text-[#aaa] hover:bg-[#282828] hover:text-white'
              }`}
            >
              <Timer className="w-4 h-4 text-[#2cbb5d] shrink-0 mt-0.5" />
              <div>
                <div className="text-xs font-semibold text-white">Stopwatch Mode (Count Up)</div>
                <div className="text-[11px] text-[#888] mt-0.5">No time pressure · Regular elapsed timer</div>
              </div>
            </button>
          </div>

          <div className="pt-2 border-t border-[#3e3e3e] flex items-center justify-between text-[11px] text-[#777]">
            <span>Current: {difficulty}</span>
            <span>
              Target: {tier === 'stopwatch' ? 'None' : `${Math.floor((TIER_CONFIG[tier]?.times[difficulty] || 0) / 60)} min`}
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
