# NYC Subway Reference Images

This folder contains a curated set of reference photos of New York City subway stations, optimized for use in creative projects (e.g. StudioRich x Sora loops).

## Contents
- **Format**: All images are `.webp` (compressed for CDN use).
- **Count**: ~441 images as of this commit.
- **Index**: See [`image_index.csv`](./image_index.csv) for the complete mapping of filenames → GitHub Pages URLs.

## File Naming
- Filenames are based on station slugs:  
  `station-name.webp`  
  e.g. `42nd-st-times-square.webp`
- Current structure captures the *station name* only.  
- If richer metadata is needed (e.g. line, borough, angle), add suffixes separated by underscores before conversion.

## CSV Structure
The `image_index.csv` contains the following columns:
- `file_stem` — base filename without extension.
- `station` — station slug (matches `file_stem`).
- `location` — optional, currently empty unless encoded in filename.
- `angle` — optional, currently empty unless encoded in filename.
- `rel_path` — relative path to the `.webp` file.
- `url` — full GitHub Pages URL for public use.

## Usage
- Use the `url` column for direct image access (e.g., for AI batching or web embeds).
- Images are already optimized to WebP for fast loading and reduced repo size.
- For Sora prompts: pair the `url` with descriptive text (colors, textures, signage, etc.) to generate station-accurate outputs.

## Notes
- Images are intentionally captured with **minimal or no people**, focusing on infrastructure (stairs, platforms, signage, textures).
- Expect occasional grime, patina, and imperfect lighting — this is part of the dataset’s authenticity.
- Expansion: future commits may add parsed columns (`borough`, `line`, `angle`) once naming conventions are standardized.
