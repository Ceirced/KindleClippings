#!/bin/bash

VAULT="SyncedVault"

if [ $# -eq 0 ]; then
    echo "Usage: $0 <file.md> [file2.md ...]"
    exit 1
fi

for filepath in "$@"; do
    if [ ! -f "$filepath" ]; then
        echo "File not found: $filepath"
        continue
    fi

    name="$(basename "$filepath" .md)"
    echo "Sending '$name' to Obsidian..."
    obsidian create name="$name" content="$(cat "$filepath")" vault="$VAULT"
done
