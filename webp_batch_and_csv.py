#!/usr/bin/env python3
"""
webp_batch_and_csv.py

Batch-convert images to WebP and emit a CSV for batching (e.g., Sora prompts).
- Preserves folder structure under an output dir
- Keeps stems (filenames without extension) identical; only the extension becomes .webp
- Generates a CSV with columns:
    file_stem, station, location, angle, rel_path, url
- Tries to parse `station`, `location`, `angle` from filename parts split by '_'.
  Example filename patterns it will parse:
    34th_st_times_square_platform.jpg -> station=34th, location=st, angle=times
- Works recursively
- Skips files already converted unless --overwrite is given

Usage example:
  python webp_batch_and_csv.py \
      --input-dir ./RAW_IMAGES \
      --output-dir ./PUBLIC_WEBP \
      --base-url https://USER.github.io/REPO/PUBLIC_WEBP \
      --csv-out ./image_index.csv \
      --quality 82

Requirements:
  pip install pillow
"""

import argparse
import csv
import os
from pathlib import Path
from typing import Tuple
from PIL import Image

VALID_EXTS = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.gif'}
WEBP_EXT = '.webp'


def parse_name(stem: str) -> Tuple[str, str, str]:
    """Try to split filename into station, location, angle."""
    parts = stem.split('_')
    station = parts[0] if len(parts) > 0 else ''
    location = parts[1] if len(parts) > 1 else ''
    angle = parts[2] if len(parts) > 2 else ''
    return station, location, angle


def to_webp(in_path: Path, out_path: Path, quality: int, lossless: bool, keep_exif: bool, method: int):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(in_path) as im:
        if im.mode in ('P', 'LA', 'RGBA', 'CMYK'):
            im = im.convert('RGB')

        save_kwargs = dict(format='WEBP', method=method)
        if lossless:
            save_kwargs['lossless'] = True
        else:
            save_kwargs['quality'] = quality

        if keep_exif and 'exif' in im.info:
            save_kwargs['exif'] = im.info['exif']

        im.save(out_path, **save_kwargs)


def main():
    ap = argparse.ArgumentParser(description="Convert images to WebP and emit a CSV of URLs.")
    ap.add_argument('--input-dir', required=True, help='Folder with source images')
    ap.add_argument('--output-dir', required=True, help='Folder where WebP images will be written')
    ap.add_argument('--base-url', required=True, help='Base URL for GitHub Pages (e.g., https://USER.github.io/REPO/PATH)')
    ap.add_argument('--csv-out', required=True, help='Path to write CSV index')
    ap.add_argument('--quality', type=int, default=82, help='WebP quality (ignored if --lossless). Default 82')
    ap.add_argument('--lossless', action='store_true', help='Use lossless WebP (larger files)')
    ap.add_argument('--keep-exif', action='store_true', help='Try to keep EXIF metadata if present')
    ap.add_argument('--overwrite', action='store_true', help='Re-convert even if output file exists')
    ap.add_argument('--skip-webp-inputs', action='store_true', help='Skip inputs that are already .webp')
    ap.add_argument('--method', type=int, default=6, help='WebP encoding effort method (0..6). Higher = smaller but slower. Default 6')
    args = ap.parse_args()

    in_dir = Path(args.input_dir).resolve()
    out_dir = Path(args.output_dir).resolve()
    csv_path = Path(args.csv_out).resolve()

    if not in_dir.exists():
        raise SystemExit(f"Input dir does not exist: {in_dir}")

    converted, skipped, errors = 0, 0, 0
    rows = []

    for root, _, files in os.walk(in_dir):
        for name in files:
            src = Path(root) / name
            ext = src.suffix.lower()

            if ext == WEBP_EXT and args.skip_webp_inputs:
                skipped += 1
                continue

            if ext not in VALID_EXTS and ext != WEBP_EXT:
                continue

            rel = src.relative_to(in_dir)
            out_rel = rel.with_suffix(WEBP_EXT)
            dst = out_dir / out_rel

            if dst.exists() and not args.overwrite:
                stem = dst.stem
                station, location, angle = parse_name(stem)
                url = f"{args.base_url.rstrip('/')}/{out_rel.as_posix()}"
                rows.append([stem, station, location, angle, out_rel.as_posix(), url])
                skipped += 1
                continue

            try:
                if ext == WEBP_EXT:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    dst.write_bytes(src.read_bytes())
                else:
                    to_webp(src, dst, args.quality, args.lossless, args.keep_exif, args.method)

                stem = dst.stem
                station, location, angle = parse_name(stem)
                url = f"{args.base_url.rstrip('/')}/{out_rel.as_posix()}"
                rows.append([stem, station, location, angle, out_rel.as_posix(), url])
                converted += 1
            except Exception as e:
                print(f"[ERROR] {src} -> {dst}: {e}")
                errors += 1

    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['file_stem', 'station', 'location', 'angle', 'rel_path', 'url'])
        writer.writerows(rows)

    total = converted + skipped + errors
    print(f"Done. Files seen: {total}")
    print(f"Converted: {converted}")
    print(f"Skipped: {skipped}")
    print(f"Errors: {errors}")
    print(f"CSV written: {csv_path}")
    print(f"Output root: {out_dir}")


if __name__ == "__main__":
    main()
