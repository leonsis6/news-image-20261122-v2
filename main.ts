// main.ts — news-image-20261122 v2 entry program.
// Copies entry.png from the repo root to $MAKEFUN_OUTPUT_DIR/entry.png
// (default /output). Refuses to copy a truncated file: the PNG must end
// with a valid IEND chunk, otherwise exit 1.
import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const dst = join(outDir, "entry.png");

const buf = readFileSync(src);

// PNG signature: 89 50 4E 47 0D 0A 1A 0A. Reject anything that is not a PNG
// at all (e.g. a truncated download or a misnamed file).
const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (buf.length < 8 || !buf.subarray(0, 8).equals(PNG_SIG)) {
  console.error("entry.png: missing PNG signature — not a PNG file, refusing to copy");
  process.exit(1);
}
if (buf.length < 1000) {
  console.error("entry.png: implausibly small for a 1024x1024 front page, refusing to copy");
  process.exit(1);
}

// IEND chunk: 4-byte length (0) + "IEND" + CRC AE 42 60 82.
const IEND = Buffer.from([
  0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82,
]);
if (buf.length < 12 || !buf.subarray(buf.length - 12).equals(IEND)) {
  console.error("entry.png: missing IEND chunk — file is truncated, refusing to copy");
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(src, dst);
console.log(`copied entry.png (${buf.length} bytes) -> ${dst}`);
