#!/bin/bash

KINDLE_VOLUME="/Volumes/Kindle"
CLIPPINGS_FILE="documents/My Clippings.txt"
DESTINATION_DIR="$(dirname "$0")"

if [ -d "$KINDLE_VOLUME" ]; then
    echo "✓ Kindle detected at $KINDLE_VOLUME"
    
    KINDLE_CLIPPINGS_PATH="$KINDLE_VOLUME/$CLIPPINGS_FILE"
    
    if [ -f "$KINDLE_CLIPPINGS_PATH" ]; then
        echo "✓ Found My Clippings.txt"
        
        TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
        DESTINATION_FILE="$DESTINATION_DIR/My Clippings_${TIMESTAMP}.txt"
        
        cp "$KINDLE_CLIPPINGS_PATH" "$DESTINATION_FILE"
        
        if [ $? -eq 0 ]; then
            echo "✓ Successfully copied to: $DESTINATION_FILE"
            
            LATEST_LINK="$DESTINATION_DIR/My Clippings.txt"
            ln -sf "$(basename "$DESTINATION_FILE")" "$LATEST_LINK"
            echo "✓ Created/updated symlink: My Clippings.txt -> $(basename "$DESTINATION_FILE")"
        else
            echo "✗ Error: Failed to copy the file"
            exit 1
        fi
    else
        echo "✗ Error: My Clippings.txt not found at expected location"
        echo "  Searched in: $KINDLE_CLIPPINGS_PATH"
        exit 1
    fi
else
    echo "✗ Error: Kindle not detected"
    echo "  Please connect your Kindle and ensure it's mounted at /Volumes/Kindle"
    exit 1
fi