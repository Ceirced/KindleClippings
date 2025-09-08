#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLIST_NAME="com.kindle.usb.autosync"
PLIST_FILE="$SCRIPT_DIR/$PLIST_NAME.plist"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
INSTALLED_PLIST="$LAUNCH_AGENTS_DIR/$PLIST_NAME.plist"

function install() {
    echo "Installing USB-triggered Kindle sync..."
    
    mkdir -p "$LAUNCH_AGENTS_DIR"
    cp "$PLIST_FILE" "$INSTALLED_PLIST"
    
    launchctl unload "$INSTALLED_PLIST" 2>/dev/null
    launchctl load "$INSTALLED_PLIST"
    
    echo "✓ USB-triggered sync installed"
    echo "  Will automatically sync when any volume is mounted"
    echo "  Much more efficient than continuous monitoring"
    echo "  Sync activity will be logged to: $SCRIPT_DIR/.sync/sync.log"
}

function uninstall() {
    echo "Uninstalling USB-triggered sync..."
    
    if [ -f "$INSTALLED_PLIST" ]; then
        launchctl unload "$INSTALLED_PLIST" 2>/dev/null
        rm "$INSTALLED_PLIST"
        echo "✓ Service uninstalled"
    else
        echo "Service is not installed"
    fi
}

case "$1" in
    install)
        install
        ;;
    uninstall)
        uninstall
        ;;
    *)
        echo "Usage: $0 {install|uninstall}"
        echo ""
        echo "USB-triggered sync - only runs when volumes are mounted"
        echo "Much more efficient than continuous monitoring"
        exit 1
        ;;
esac