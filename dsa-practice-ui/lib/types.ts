export type Difficulty = 'Easy' | 'Medium' | 'Hard';

export interface Example {
  input: string;
  output: string;
  explanation?: string;
}

export interface TestCase {
  id: number;
  args?: any[];
  input?: any[];
  expected: any;
  inputDisplay: string;
  expectedDisplay: string;
  methods?: string[];
  methodArgs?: any[][];
  hasLinkedList?: boolean;
  hasTree?: boolean;
  orderInsensitive?: boolean;
}

export interface Editorial {
  step1: string; // Clarify problem
  step2: string; // Brute force
  step3: string; // Optimal strategy
  step5: string; // Complexity analysis
  solutionCode: string;
}

export interface Problem {
  id: string;
  slug: string;
  lcNumber: number;
  title: string;
  difficulty: Difficulty;
  category: string;
  pattern: string;
  companies: string;
  description: string;
  examples: Example[];
  constraints: string[];
  starterCode: string;
  entryFunction: string;
  editorial: Editorial;
  testCases: TestCase[];
}

export interface CaseResult {
  caseIndex: number;
  passed: boolean;
  inputDisplay: string;
  expectedDisplay: string;
  actualDisplay: string;
  stdout?: string;
  error?: string;
}

export interface ExecutionResponse {
  status: 'Accepted' | 'Wrong Answer' | 'Runtime Error' | 'Compile Error' | 'Time Limit Exceeded';
  runtimeMs: number;
  passedCount: number;
  totalCount: number;
  results: CaseResult[];
  error?: string;
  stdout?: string;
}
