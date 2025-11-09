#!/bin/bash

# Install cron job for daily Rocketbook sync

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_PATH="$SCRIPT_DIR/venv/bin/python"
SYNC_SCRIPT="$SCRIPT_DIR/scripts/sync.py"
LOG_DIR="$SCRIPT_DIR/logs"

echo "================================"
echo "Cron Job Installation"
echo "================================"
echo ""
echo "This will set up a cron job to run the sync once daily at 8:00 PM"
echo ""
echo "Script location: $SYNC_SCRIPT"
echo "Python: $PYTHON_PATH"
echo ""

# Check if virtual environment exists
if [ ! -f "$PYTHON_PATH" ]; then
    echo "Error: Virtual environment not found. Run ./setup.sh first"
    exit 1
fi

# Create wrapper script
WRAPPER_SCRIPT="$SCRIPT_DIR/run_sync.sh"
cat > "$WRAPPER_SCRIPT" << EOF
#!/bin/bash
# Auto-generated wrapper for cron execution

cd "$SCRIPT_DIR"
source venv/bin/activate
python scripts/sync.py >> logs/cron.log 2>&1
EOF

chmod +x "$WRAPPER_SCRIPT"

echo "Created wrapper script: $WRAPPER_SCRIPT"
echo ""

# Cron job entry - runs daily at 8 PM
CRON_JOB="0 20 * * * $WRAPPER_SCRIPT"

echo "Cron job to be added:"
echo "$CRON_JOB"
echo ""

read -p "Install this cron job? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Check if cron job already exists
    if crontab -l 2>/dev/null | grep -q "$WRAPPER_SCRIPT"; then
        echo "Cron job already exists. Skipping..."
    else
        # Add to crontab
        (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
        echo "✓ Cron job installed successfully!"
        echo ""
        echo "The sync will run daily at 8:00 PM"
        echo "Logs will be written to: $LOG_DIR/cron.log"
    fi
else
    echo "Installation cancelled"
    echo ""
    echo "To run manually:"
    echo "  cd $SCRIPT_DIR"
    echo "  source venv/bin/activate"
    echo "  python scripts/sync.py"
fi

echo ""
echo "To view/edit your cron jobs:"
echo "  crontab -l    # List"
echo "  crontab -e    # Edit"
echo ""

# Show existing cron jobs
echo "Your current cron jobs:"
crontab -l 2>/dev/null || echo "(none)"
echo ""
