#!/bin/bash
set -euo pipefail

# Adjust these paths as needed
SRC_DIR="mta"
DEST_DIR="PUBLIC_WEBP"

# Create destination if it doesn’t exist
mkdir -p "$DEST_DIR"

# Loop through subdirectories of SRC_DIR
for dir in "$SRC_DIR"/*/; do
  # Move files only (skip subdirs)
  find "$dir" -maxdepth 1 -type f -exec mv -n {} "$DEST_DIR"/ \;
done

echo "✅ All files moved from $SRC_DIR subfolders into $DEST_DIR"
