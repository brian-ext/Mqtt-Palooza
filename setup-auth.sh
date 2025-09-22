#!/bin/bash

# Secure Authentication Setup for Ollama Proxy
# This script creates the necessary authentication files locally

set -e

echo "🔐 Setting up secure authentication for Ollama proxy..."
echo "⚠️  WARNING: Never commit authentication files to version control!"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Create nginx directory if it doesn't exist
mkdir -p nginx

# Check if .htpasswd already exists
if [ -f "nginx/.htpasswd" ]; then
    echo -e "${YELLOW}⚠️  Authentication file already exists: nginx/.htpasswd${NC}"
    read -p "Overwrite? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}Keeping existing authentication file.${NC}"
        exit 0
    fi
fi

echo -e "${BLUE}Setting up HTTP Basic Authentication...${NC}"
echo ""

# Option 1: Use default credentials
echo -e "${GREEN}Default credentials:${NC}"
echo "  Username: ollama"
echo "  Password: scraper"
echo ""

read -p "Use default credentials? (Y/n): " -n 1 -r
echo

if [[ $REPLY =~ ^[Nn]$ ]]; then
    # Option 2: Custom credentials
    echo -e "${BLUE}Enter custom credentials:${NC}"
    read -p "Username: " username
    read -s -p "Password: " password
    echo ""
    read -s -p "Confirm password: " password_confirm
    echo ""

    if [ "$password" != "$password_confirm" ]; then
        echo -e "${RED}❌ Passwords do not match!${NC}"
        exit 1
    fi
else
    # Use defaults
    username="ollama"
    password="scraper"
fi

# Generate .htpasswd file
printf "${username}:$(openssl passwd -apr1 ${password})\n" > nginx/.htpasswd

echo -e "${GREEN}✅ Authentication setup complete!${NC}"
echo ""
echo -e "${BLUE}📁 Files created:${NC}"
echo "  nginx/.htpasswd (contains hashed passwords)"
echo ""
echo -e "${BLUE}🔑 Credentials:${NC}"
echo "  Username: ${username}"
echo "  Password: ${password}"
echo ""
echo -e "${YELLOW}🚨 SECURITY REMINDER:${NC}"
echo "  • Never commit nginx/.htpasswd to version control"
echo "  • The file is already in .gitignore"
echo "  • Change default passwords in production"
echo "  • Use strong, unique passwords"
echo ""
echo -e "${GREEN}Ready to deploy with: docker-compose -f docker-compose.ollama.yml up -d${NC}"