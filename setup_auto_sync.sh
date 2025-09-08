#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLIST_NAME="com.kindle.autosync"
PLIST_FILE="$SCRIPT_DIR/$PLIST_NAME.plist"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
INSTALLED_PLIST="$LAUNCH_AGENTS_DIR/$PLIST_NAME.plist"

function install() {
    echo "Installing Kindle auto-sync service..."
    
    mkdir -p "$LAUNCH_AGENTS_DIR"
    
    cp "$PLIST_FILE" "$INSTALLED_PLIST"
    
    launchctl unload "$INSTALLED_PLIST" 2>/dev/null
    
    launchctl load "$INSTALLED_PLIST"
    
    if launchctl list | grep -q "$PLIST_NAME"; then
        echo "✓ Service installed and started successfully"
        echo "  The service will now monitor for your Kindle and auto-sync clippings"
        echo "  Logs are available at:"
        echo "    - $SCRIPT_DIR/kindle_auto_sync.log"
        echo "    - $SCRIPT_DIR/kindle_auto_sync.stdout.log"
        echo "    - $SCRIPT_DIR/kindle_auto_sync.stderr.log"
    else
        echo "✗ Failed to start service"
        exit 1
    fi
}

function uninstall() {
    echo "Uninstalling Kindle auto-sync service..."
    
    if [ -f "$INSTALLED_PLIST" ]; then
        launchctl unload "$INSTALLED_PLIST" 2>/dev/null
        rm "$INSTALLED_PLIST"
        echo "✓ Service uninstalled"
    else
        echo "Service is not installed"
    fi
}

function status() {
    if launchctl list | grep -q "$PLIST_NAME"; then
        echo "✓ Kindle auto-sync service is running"
        launchctl list | grep "$PLIST_NAME"
    else
        echo "✗ Kindle auto-sync service is not running"
    fi
}

function restart() {
    echo "Restarting Kindle auto-sync service..."
    launchctl unload "$INSTALLED_PLIST" 2>/dev/null
    launchctl load "$INSTALLED_PLIST"
    status
}

function test_manual() {
    echo "Starting manual test of Kindle auto-sync..."
    echo "Press Ctrl+C to stop"
    python3 "$SCRIPT_DIR/kindle_auto_sync.py"
}

function show_logs() {
    echo "=== Recent auto-sync logs ==="
    tail -n 20 "$SCRIPT_DIR/kindle_auto_sync.log" 2>/dev/null || echo "No logs found yet"
}

case "$1" in
    install)
        install
        ;;
    uninstall)
        uninstall
        ;;
    status)
        status
        ;;
    restart)
        restart
        ;;
    test)
        test_manual
        ;;
    logs)
        show_logs
        ;;
    *)
        echo "Usage: $0 {install|uninstall|status|restart|test|logs}"
        echo ""
        echo "Commands:"
        echo "  install   - Install and start the auto-sync service"
        echo "  uninstall - Stop and remove the auto-sync service"
        echo "  status    - Check if the service is running"
        echo "  restart   - Restart the service"
        echo "  test      - Run the sync monitor manually (for testing)"
        echo "  logs      - Show recent sync logs"
        exit 1
        ;;
esac