#!/bin/bash

# Telegram Voice Bot - Stop Script
# This script stops the running bot process

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🛑 Stopping Telegram Voice Bot...${NC}"

# Find bot.py process
BOT_PID=$(ps aux | grep "python bot.py" | grep -v grep | awk '{print $2}')

if [ -z "$BOT_PID" ]; then
    echo -e "${RED}❌ Bot is not running${NC}"
    exit 1
fi

# Kill the process
kill $BOT_PID

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Bot stopped successfully${NC}"
else
    echo -e "${RED}❌ Failed to stop bot${NC}"
    echo -e "${YELLOW}💡 Try: kill -9 $BOT_PID${NC}"
    exit 1
fi
