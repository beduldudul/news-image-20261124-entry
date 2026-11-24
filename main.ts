// news-image-20261124 entry program (Node 22, standard library only).
//
// Writes the drawn front page for Tuesday 24 November 2026 to
// /output/entry.png. The image lives in this repository as entry.png;
// this program copies it byte for byte and verifies the gate limits
// (PNG magic, at most 1 MiB, exactly 1024 x 1024) before writing.
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1048576;
const EXPECTED_WIDTH = 1024;
const EXPECTED_HEIGHT = 1024;

const repoDir = fileURLToPath(new URL(".", import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const source = join(repoDir, "entry.png");
const target = join(outDir, "entry.png");

const bytes = readFileSync(source);
if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error("entry.png is not a PNG (bad magic bytes)");
}
if (bytes.length > MAX_BYTES) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
}

// PNG header: width at bytes 16-19, height at bytes 20-23 (big-endian).
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width !== EXPECTED_WIDTH || height !== EXPECTED_HEIGHT) {
  throw new Error(
    `entry.png is ${width}x${height}, expected ${EXPECTED_WIDTH}x${EXPECTED_HEIGHT}`,
  );
}

mkdirSync(outDir, { recursive: true });
writeFileSync(target, bytes);

// Byte-for-byte check: what we wrote must be exactly what we read.
const written = readFileSync(target);
if (!written.equals(bytes)) {
  throw new Error("output differs from entry.png after copy");
}
console.log(`wrote ${target} (${bytes.length} bytes, ${width}x${height})`);
