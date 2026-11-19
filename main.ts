// "Sum up 18 November's world news in one image" (news-image-20261118).
// Node 22, standard library only. The image is the entry.png beside this
// file — a 1024x1024 front-page infographic drawn by gen.py from the
// verified briefing (news-18nov-facts.md) — and the program copies it to
// /output/entry.png, byte for byte. The gate takes a whole PNG or JPEG of
// at most 1 MiB and 1024 by 1024 pixels, and the judge sees exactly the
// bytes copied. The program runs twice in the grader; a plain copy is
// deterministic by construction.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const outPath = join(outDir, 'entry.png');
copyFileSync(new URL('./entry.png', import.meta.url), outPath);

// Fail loudly instead of shipping a bad image: the gate wants a whole PNG
// of at most 1 MiB and exactly 1024 by 1024 pixels. PNG signature is 8
// bytes, then the IHDR chunk holds width/height as big-endian u32 at
// offsets 16 and 20.
const buf = readFileSync(outPath);
const isPng = buf.subarray(0, 8).equals(
  Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]));
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (!isPng || width !== 1024 || height !== 1024 || buf.length > 1048576) {
  throw new Error(
    `entry.png failed the gate: png=${isPng} ${width}x${height} ` +
    `${buf.length} bytes`);
}
console.log(`entry.png OK: 1024x1024, ${buf.length} bytes`);
