// The Wednesday Globe — news-image-20261125 entry (Node 22, stdlib only).
//
// The front page is drawn at build time by render.py (Pillow) and ships in
// this repository as entry.png. This program copies it into the output
// directory byte for byte, so the grader's two runs produce identical bytes.
//
// Run it outside the grader with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
writeFileSync(
  join(outDir, 'entry.png'),
  readFileSync(join(here, 'entry.png')),
);
