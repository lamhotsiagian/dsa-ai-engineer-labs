'use client';

import React, { useState } from 'react';
import Editor from '@monaco-editor/react';
import { RotateCcw, Copy, Check, Terminal, Keyboard } from 'lucide-react';

interface CodeEditorProps {
  code: string;
  onChange: (value: string) => void;
  onReset: () => void;
}

export default function CodeEditor({ code, onChange, onReset }: CodeEditorProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="flex flex-col h-full bg-[#1e1e1e] border-b border-[#3e3e3e]">
      {/* Editor Header Bar */}
      <div className="h-10 bg-[#282828] border-b border-[#3e3e3e] px-4 flex items-center justify-between select-none text-xs text-[#eff1f6]">
        <div className="flex items-center gap-2">
          <span className="font-semibold text-white flex items-center gap-1.5 bg-[#3a3a3a] px-2.5 py-1 rounded">
            <Terminal className="w-3.5 h-3.5 text-[#3b82f6]" />
            <span>Python 3</span>
          </span>
          <span className="text-[#8a8a8a] text-[11px] hidden sm:inline flex items-center gap-1">
            <Keyboard className="w-3 h-3" />
            <kbd className="bg-[#333] px-1.5 py-0.5 rounded text-[10px] text-[#ccc]">Cmd</kbd> + <kbd className="bg-[#333] px-1.5 py-0.5 rounded text-[10px] text-[#ccc]">Enter</kbd> to Run
          </span>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={onReset}
            className="flex items-center gap-1 text-[#8a8a8a] hover:text-white hover:bg-[#3a3a3a] px-2 py-1 rounded transition text-xs"
            title="Reset code to default template"
          >
            <RotateCcw className="w-3 h-3" />
            <span>Reset</span>
          </button>

          <button
            onClick={handleCopy}
            className="flex items-center gap-1 text-[#8a8a8a] hover:text-white hover:bg-[#3a3a3a] px-2 py-1 rounded transition text-xs"
            title="Copy current code"
          >
            {copied ? <Check className="w-3 h-3 text-[#2cbb5d]" /> : <Copy className="w-3 h-3" />}
            <span>{copied ? 'Copied' : 'Copy'}</span>
          </button>
        </div>
      </div>

      {/* Monaco Editor Container */}
      <div className="flex-1 w-full relative">
        <Editor
          height="100%"
          language="python"
          theme="vs-dark"
          value={code}
          onChange={(val) => onChange(val || '')}
          loading={
            <div className="flex items-center justify-center h-full text-xs text-[#8a8a8a]">
              Loading Monaco Editor...
            </div>
          }
          options={{
            fontSize: 14,
            fontFamily: "'Fira Code', 'Cascadia Code', 'JetBrains Mono', Menlo, Monaco, monospace",
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            lineNumbers: 'on',
            automaticLayout: true,
            tabSize: 4,
            insertSpaces: true,
            padding: { top: 12, bottom: 12 },
            cursorBlinking: 'smooth',
            smoothScrolling: true,
            renderLineHighlight: 'all',
            scrollbar: {
              verticalScrollbarSize: 8,
              horizontalScrollbarSize: 8,
            },
          }}
        />
      </div>
    </div>
  );
}
