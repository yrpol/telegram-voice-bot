#!/bin/bash

# Telegram Voice Bot - Setup Script
# This script sets up the project for first time use

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Telegram Voice Bot - Setup Wizard    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Step 1: Create virtual environment
echo -e "${GREEN}[1/4] 📦 Creating virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}   ⚠️  Virtual environment already exists, skipping${NC}"
else
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}   ✅ Virtual environment created${NC}"
    else
        echo -e "${RED}   ❌ Failed to create virtual environment${NC}"
        exit 1
    fi
fi
echo ""

# Step 2: Activate and install dependencies
echo -e "${GREEN}[2/4] 📥 Installing dependencies...${NC}"
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}   ✅ Dependencies installed${NC}"
else
    echo -e "${RED}   ❌ Failed to install dependencies${NC}"
    exit 1
fi
echo ""

# Step 3: Setup .env file
echo -e "${GREEN}[3/4] 🔐 Setting up environment variables...${NC}"
if [ -f .env ]; then
    echo -e "${YELLOW}   ⚠️  .env file already exists${NC}"
    read -p "   Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}   Keeping existing .env file${NC}"
        SKIP_ENV=true
    fi
fi

if [ "$SKIP_ENV" != "true" ]; then
    cp .env.example .env
    echo -e "${GREEN}   ✅ .env file created from template${NC}"
    echo ""
    echo -e "${YELLOW}   ⚠️  IMPORTANT: Edit .env file and add your API keys!${NC}"
    echo -e "${YELLOW}   Required keys:${NC}"
    echo -e "${YELLOW}   - TELEGRAM_TOKEN${NC}"
    echo -e "${YELLOW}   - OPENAI_KEY${NC}"
    echo -e "${YELLOW}   - NOTION_TOKEN${NC}"
    echo -e "${YELLOW}   - NOTION_DATABASE_ID${NC}"
    echo -e "${YELLOW}   - ALLOWED_USERS${NC}"
    echo ""
    read -p "   Press Enter to open .env in nano editor (or Ctrl+C to skip)..."
    nano .env
fi
echo ""

# Step 4: Make scripts executable
echo -e "${GREEN}[4/4] 🔧 Making scripts executable...${NC}"
chmod +x start.sh
chmod +x stop.sh
chmod +x setup.sh

if [ $? -eq 0 ]; then
    echo -e "${GREEN}   ✅ Scripts are now executable${NC}"
else
    echo -e "${RED}   ❌ Failed to make scripts executable${NC}"
fi
echo ""

# Final instructions
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║          Setup Complete! 🎉            ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}Next steps:${NC}"
echo -e "1. Make sure your .env file has all API keys"
echo -e "2. Run: ${GREEN}./start.sh${NC} to start the bot"
echo -e "3. Send a voice message to your bot in Telegram"
echo ""
echo -e "${YELLOW}Useful commands:${NC}"
echo -e "  ${GREEN}./start.sh${NC}  - Start the bot"
echo -e "  ${GREEN}./stop.sh${NC}   - Stop the bot"
echo -e "  ${GREEN}nano .env${NC}   - Edit API keys"
echo ""

deactivate
