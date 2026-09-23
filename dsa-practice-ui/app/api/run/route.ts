import { NextRequest, NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { code, entryFunction } = body;
    const testcases = body.testCases || body.testcases || [];
    const isClass = body.isClass !== undefined 
      ? Boolean(body.isClass) 
      : Boolean(testcases.length > 0 && testcases[0].methods);

    if (!code) {
      return NextResponse.json(
        { status: 'Compile Error', error: 'No code provided.' },
        { status: 400 }
      );
    }

    const runnerPath = path.join(process.cwd(), 'lib', 'runner.py');
    const payloadStr = JSON.stringify({
      code,
      entryFunction: entryFunction || 'solution',
      isClass,
      slug: body.slug || '',
      testcases,
    });

    const executionPromise = new Promise((resolve, reject) => {
      const pyProcess = spawn('python3', [runnerPath]);
      let stdoutData = '';
      let stderrData = '';

      const timer = setTimeout(() => {
        pyProcess.kill();
        resolve({
          status: 'Time Limit Exceeded',
          runtimeMs: 4000,
          passedCount: 0,
          totalCount: testcases ? testcases.length : 0,
          results: [],
          error: 'Time Limit Exceeded (maximum allowed execution time is 4 seconds).',
        });
      }, 4000);

      pyProcess.stdin.write(payloadStr);
      pyProcess.stdin.end();

      pyProcess.stdout.on('data', (data) => {
        stdoutData += data.toString();
      });

      pyProcess.stderr.on('data', (data) => {
        stderrData += data.toString();
      });

      pyProcess.on('close', () => {
        clearTimeout(timer);
        if (stderrData && !stdoutData) {
          resolve({
            status: 'Runtime Error',
            runtimeMs: 0,
            passedCount: 0,
            totalCount: testcases ? testcases.length : 0,
            results: [],
            error: stderrData,
          });
          return;
        }

        try {
          const parsed = JSON.parse(stdoutData.trim());
          resolve(parsed);
        } catch {
          resolve({
            status: 'Compile Error',
            runtimeMs: 0,
            passedCount: 0,
            totalCount: testcases ? testcases.length : 0,
            results: [],
            error: stdoutData || stderrData || 'Failed to parse execution output.',
          });
        }
      });

      pyProcess.on('error', (err) => {
        clearTimeout(timer);
        reject(err);
      });
    });

    const result = await executionPromise;
    return NextResponse.json(result);
  } catch (error: any) {
    return NextResponse.json(
      {
        status: 'Runtime Error',
        runtimeMs: 0,
        passedCount: 0,
        totalCount: 0,
        results: [],
        error: error?.message || 'Server execution error',
      },
      { status: 500 }
    );
  }
}
