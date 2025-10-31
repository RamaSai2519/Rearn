#!/bin/bash
#
# Instagram Brainrot Bot - Runner Script
# This script sets up and runs the Instagram bot
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "Instagram Brainrot Bot - Runner"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓${NC} Python version: $PYTHON_VERSION"

# Check if dependencies are installed
if ! python3 -c "import instagrapi" 2>/dev/null; then
    echo -e "${YELLOW}Installing dependencies...${NC}"
    pip install -r requirements.txt
else
    echo -e "${GREEN}✓${NC} Dependencies already installed"
fi

# Run validation tests
echo ""
echo "Running validation tests..."
python3 test_bot.py

if [ $? -ne 0 ]; then
    echo -e "${RED}Validation tests failed. Please fix errors before running the bot.${NC}"
    exit 1
fi

# Run the bot
echo ""
echo "=========================================="
echo "Starting Instagram Brainrot Bot..."
echo "=========================================="
echo ""

python3 bot.py

echo ""
echo "=========================================="
echo "Bot execution completed"
echo "=========================================="
