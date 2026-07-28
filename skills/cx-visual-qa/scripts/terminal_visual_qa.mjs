#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, resolve } from "node:path";

function parseArgs(argv) {
  const args = {
    input: null,
    outdir: "terminal-visual-qa",
    command: "",
    cols: null,
    rows: null,
    sourceType: "replay",
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--input") args.input = argv[++i];
    else if (arg === "--outdir") args.outdir = argv[++i];
    else if (arg === "--command") args.command = argv[++i];
    else if (arg === "--cols") args.cols = Number(argv[++i]);
    else if (arg === "--rows") args.rows = Number(argv[++i]);
    else if (arg === "--source-type") args.sourceType = argv[++i];
    else if (arg === "--help" || arg === "-h") {
      printHelp();
      process.exit(0);
    } else {
      throw new Error(`unknown argument: ${arg}`);
    }
  }
  return args;
}

function printHelp() {
  console.log(`Usage:
  node terminal_visual_qa.mjs --input capture.ansi --outdir out/terminal --command "npm run tui" --cols 100 --rows 30

Writes terminal.txt, terminal-ansi.txt, terminal.html, and metadata.json.
If --input is omitted, ANSI content is read from stdin.`);
}

function stripAnsi(text) {
  return text.replace(/\u001b\[[0-?]*[ -/]*[@-~]/g, "");
}

function escapeHtml(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function xtermColor(n) {
  const base = [
    [0, 0, 0], [128, 0, 0], [0, 128, 0], [128, 128, 0],
    [0, 0, 128], [128, 0, 128], [0, 128, 128], [192, 192, 192],
    [128, 128, 128], [255, 0, 0], [0, 255, 0], [255, 255, 0],
    [0, 0, 255], [255, 0, 255], [0, 255, 255], [255, 255, 255],
  ];
  if (n < 16) return base[n] || base[7];
  if (n >= 16 && n <= 231) {
    const v = n - 16;
    const r = Math.floor(v / 36);
    const g = Math.floor((v % 36) / 6);
    const b = v % 6;
    const scale = [0, 95, 135, 175, 215, 255];
    return [scale[r], scale[g], scale[b]];
  }
  const gray = 8 + (n - 232) * 10;
  return [gray, gray, gray];
}

function rgb([r, g, b]) {
  return `rgb(${r}, ${g}, ${b})`;
}

function styleToCss(style) {
  const css = [];
  if (style.bold) css.push("font-weight:700");
  if (style.dim) css.push("opacity:.72");
  if (style.italic) css.push("font-style:italic");
  if (style.underline) css.push("text-decoration:underline");
  if (style.fg) css.push(`color:${style.fg}`);
  if (style.bg) css.push(`background:${style.bg}`);
  return css.join(";");
}

function applySgr(style, codes) {
  const next = { ...style };
  if (codes.length === 0) codes = [0];
  for (let i = 0; i < codes.length; i += 1) {
    const code = codes[i];
    if (code === 0) {
      for (const key of Object.keys(next)) delete next[key];
    } else if (code === 1) next.bold = true;
    else if (code === 2) next.dim = true;
    else if (code === 3) next.italic = true;
    else if (code === 4) next.underline = true;
    else if (code === 22) {
      delete next.bold;
      delete next.dim;
    } else if (code === 23) delete next.italic;
    else if (code === 24) delete next.underline;
    else if (code === 39) delete next.fg;
    else if (code === 49) delete next.bg;
    else if (code >= 30 && code <= 37) next.fg = rgb(xtermColor(code - 30));
    else if (code >= 90 && code <= 97) next.fg = rgb(xtermColor(code - 90 + 8));
    else if (code >= 40 && code <= 47) next.bg = rgb(xtermColor(code - 40));
    else if (code >= 100 && code <= 107) next.bg = rgb(xtermColor(code - 100 + 8));
    else if ((code === 38 || code === 48) && codes[i + 1] === 5 && Number.isFinite(codes[i + 2])) {
      next[code === 38 ? "fg" : "bg"] = rgb(xtermColor(codes[i + 2]));
      i += 2;
    } else if ((code === 38 || code === 48) && codes[i + 1] === 2) {
      const triplet = codes.slice(i + 2, i + 5);
      if (triplet.length === 3 && triplet.every(Number.isFinite)) {
        next[code === 38 ? "fg" : "bg"] = rgb(triplet);
        i += 4;
      }
    }
  }
  return next;
}

function ansiToHtml(text) {
  let html = "";
  let buffer = "";
  let style = {};

  function flush() {
    if (!buffer) return;
    const css = styleToCss(style);
    const escaped = escapeHtml(buffer);
    html += css ? `<span style="${css}">${escaped}</span>` : escaped;
    buffer = "";
  }

  for (let i = 0; i < text.length; i += 1) {
    if (text.charCodeAt(i) !== 27 || text[i + 1] !== "[") {
      buffer += text[i];
      continue;
    }
    let j = i + 2;
    while (j < text.length && !/[A-Za-z~]/.test(text[j])) j += 1;
    if (j >= text.length) break;
    const command = text[j];
    const raw = text.slice(i + 2, j);
    if (command === "m") {
      flush();
      const codes = raw.split(";").filter(Boolean).map((value) => Number(value));
      style = applySgr(style, codes);
    }
    i = j;
  }
  flush();
  return `<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Terminal Visual QA</title>
  <style>
    :root { color-scheme: dark; }
    body { margin: 0; background: #111; color: #eee; }
    pre {
      box-sizing: border-box;
      margin: 0;
      min-height: 100vh;
      padding: 16px;
      background: #111;
      color: #eee;
      font: 14px/1.45 ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
      white-space: pre-wrap;
      overflow-wrap: anywhere;
    }
  </style>
</head>
<body><pre>${html}</pre></body>
</html>
`;
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const ansi = args.input ? readFileSync(args.input, "utf8") : readFileSync(0, "utf8");
  const outdir = resolve(args.outdir);
  mkdirSync(outdir, { recursive: true });

  const plain = stripAnsi(ansi);
  const metadata = {
    generatedAt: new Date().toISOString(),
    input: args.input ? resolve(args.input) : "stdin",
    outdir,
    command: args.command || null,
    terminal: {
      cols: Number.isFinite(args.cols) ? args.cols : null,
      rows: Number.isFinite(args.rows) ? args.rows : null,
    },
    sourceType: args.sourceType,
    files: ["terminal.txt", "terminal-ansi.txt", "terminal.html", "metadata.json"],
    notes: [
      "ANSI SGR styling is preserved in terminal-ansi.txt and rendered into terminal.html.",
      "PNG is optional and not generated by this dependency-free helper.",
    ],
  };

  writeFileSync(`${outdir}/terminal-ansi.txt`, ansi);
  writeFileSync(`${outdir}/terminal.txt`, plain);
  writeFileSync(`${outdir}/terminal.html`, ansiToHtml(ansi));
  writeFileSync(`${outdir}/metadata.json`, `${JSON.stringify(metadata, null, 2)}\n`);

  console.log(JSON.stringify({
    ok: true,
    outdir,
    input: metadata.input,
    files: metadata.files.map((file) => `${outdir}/${file}`),
    preview: basename(`${outdir}/terminal.html`),
  }, null, 2));
}

try {
  main();
} catch (error) {
  console.error(error?.message || String(error));
  process.exit(1);
}
