#!/bin/bash

# Setup script for Rocketbook Automation

set -e

echo "================================"
echo "Rocketbook Automation Setup"
echo "================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed"
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your configuration:"
    echo "   - CLAUDE_API_KEY"
    echo "   - OBSIDIAN_VAULT_PATH (default: /Users/nathanlittle-rea/Documents/Obsidian Vault)"
    echo "   - GOOGLE_DRIVE_FOLDER_NAME (default: Rocketbook)"
fi

# Create directories
echo ""
echo "Creating directories..."
mkdir -p logs temp config

# Make scripts executable
echo "Making scripts executable..."
chmod +x scripts/sync.py
chmod +x setup.sh
chmod +x install_cron.sh

echo ""
echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Get your Claude API key:"
echo "   - Go to https://console.anthropic.com/"
echo "   - Sign up or log in"
echo "   - Navigate to API Keys section"
echo "   - Create a new API key"
echo "   - Copy the key"
echo ""
echo "2. Edit .env file:"
echo "   nano .env"
echo "   - Add your CLAUDE_API_KEY"
echo "   - Verify OBSIDIAN_VAULT_PATH is correct"
echo ""
echo "3. Set up Google Drive API:"
echo "   - Go to https://console.cloud.google.com/"
echo "   - Create a new project (or use existing)"
echo "   - Enable Google Drive API"
echo "   - Create OAuth 2.0 credentials"
echo "   - Download credentials.json to config/ directory"
echo ""
echo "4. Test the sync:"
echo "   source venv/bin/activate"
echo "   python scripts/sync.py"
echo ""
echo "5. Set up daily automation:"
echo "   ./install_cron.sh"
echo ""
