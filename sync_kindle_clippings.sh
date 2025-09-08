#!/bin/bash

KINDLE_VOLUME="/Volumes/Kindle"
CLIPPINGS_FILE="documents/My Clippings.txt"
DESTINATION_DIR="$(dirname "$0")"
SYNC_DIR="$DESTINATION_DIR/.sync"
LOG_FILE="$SYNC_DIR/sync.log"

# Function to log messages with timestamp
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
    echo "$1"
}

# Create sync directory if it doesn't exist
mkdir -p "$SYNC_DIR"

log_message "=== Kindle Sync Started ==="

if [ -d "$KINDLE_VOLUME" ]; then
    log_message "✓ Kindle detected at $KINDLE_VOLUME"
    
    KINDLE_CLIPPINGS_PATH="$KINDLE_VOLUME/$CLIPPINGS_FILE"
    
    if [ -f "$KINDLE_CLIPPINGS_PATH" ]; then
        log_message "✓ Found My Clippings.txt"
        
        TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
        DESTINATION_FILE="$SYNC_DIR/My Clippings_${TIMESTAMP}.txt"
        
        cp "$KINDLE_CLIPPINGS_PATH" "$DESTINATION_FILE"
        
        if [ $? -eq 0 ]; then
            log_message "✓ Successfully copied to: $DESTINATION_FILE"
            
            LATEST_LINK="$DESTINATION_DIR/My Clippings.txt"
            ln -sf ".sync/$(basename "$DESTINATION_FILE")" "$LATEST_LINK"
            log_message "✓ Created/updated symlink: My Clippings.txt -> .sync/$(basename "$DESTINATION_FILE")"
            
            log_message "📚 Parsing clippings into individual book files..."
            
            # Copy the latest file to the expected location for parse_clippings.py
            cp "$DESTINATION_FILE" "$DESTINATION_DIR/My Clippings.txt"
            
            # Run the parser using uv (unset VIRTUAL_ENV to avoid path mismatch warning)
            cd "$DESTINATION_DIR"
            unset VIRTUAL_ENV
            uv run python parse_clippings.py
            PARSE_RESULT=$?
            
            if [ $PARSE_RESULT -eq 0 ]; then
                log_message "✓ Successfully parsed clippings into individual book files"
                log_message "=== Kindle Sync Completed Successfully ==="
            else
                log_message "⚠ Warning: Failed to parse clippings (sync was successful though)"
                log_message "=== Kindle Sync Completed with Warnings ==="
            fi
        else
            log_message "✗ Error: Failed to copy the file"
            log_message "=== Kindle Sync Failed ==="
            exit 1
        fi
    else
        log_message "✗ Error: My Clippings.txt not found at expected location"
        log_message "  Searched in: $KINDLE_CLIPPINGS_PATH"
        log_message "=== Kindle Sync Failed ==="
        exit 1
    fi
else
    log_message "✗ Error: Kindle not detected"
    log_message "  Please connect your Kindle and ensure it's mounted at /Volumes/Kindle"
    log_message "=== Kindle Sync Skipped ==="
    exit 1
fi