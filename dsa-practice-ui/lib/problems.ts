import { Problem } from './types';
import problemsData from './problems.json';

export const PROBLEMS: Problem[] = problemsData as unknown as Problem[];
export const ALL_PROBLEMS = PROBLEMS;

export const DEFAULT_PROBLEM: Problem =
  PROBLEMS.find((p) => p.lcNumber === 1 || p.id === 'two-sum') || PROBLEMS[0];

export const CATEGORIES = Array.from(new Set(PROBLEMS.map((p) => p.category)));

export function getProblemById(id: string): Problem | undefined {
  return PROBLEMS.find((p) => p.id === id);
}

export function getProblemBySlug(slug: string): Problem | undefined {
  return PROBLEMS.find((p) => p.slug === slug);
}

export function getProblemByNumber(num: number): Problem | undefined {
  return PROBLEMS.find((p) => p.lcNumber === num);
}
