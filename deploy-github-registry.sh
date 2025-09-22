#!/bin/bash

set -e

echo "🚀 Deploying AI Scraper System from GitHub Container Registry..."
echo "🔒 Protected by AGPL-3.0 License - Big Tech Cannot Steal This!"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m'

# Configuration
GITHUB_USERNAME="${GITHUB_USERNAME:-scrapedat}"
REGISTRY="ghcr.io"
IMAGE_PREFIX="${REGISTRY}/${GITHUB_USERNAME}"

echo -e "${BLUE}📥 Pulling latest images from GitHub Container Registry...${NC}"

# Pull all images
docker pull ${IMAGE_PREFIX}/frankenstein-db:latest
docker pull ${IMAGE_PREFIX}/ai-scraper-vm:latest
docker pull ${IMAGE_PREFIX}/ai-scraper-dashboard:latest

echo -e "${YELLOW}🏗️ Starting AI Scraper System...${NC}"

# Deploy using GitHub registry compose file
docker-compose -f docker-compose.github.yml up -d

echo -e "${BLUE}⏳ Waiting for services to be healthy...${NC}"

# Wait for health checks
sleep 30

# Check service status
echo -e "${YELLOW}📊 Service Status:${NC}"
docker-compose -f docker-compose.github.yml ps

# Display access information
echo -e "${GREEN}✅ AI Scraper System deployed successfully!${NC}"
echo -e "${GREEN}🔗 Dashboard: http://localhost:3000${NC}"
echo -e "${GREEN}📡 MQTT Broker: localhost:1883${NC}"
echo -e "${GREEN}🗄️ FrankensteinDB: Available internally${NC}"

echo -e "${PURPLE}🛡️ System Protection:${NC}"
echo -e "${PURPLE}  • All components licensed under AGPL-3.0${NC}"
echo -e "${PURPLE}  • Big tech companies cannot use this commercially${NC}"
echo -e "${PURPLE}  • Forces open-source for any SaaS deployment${NC}"

echo -e "${BLUE}📋 Management Commands:${NC}"
echo "  View logs: docker-compose -f docker-compose.github.yml logs -f"
echo "  Stop system: docker-compose -f docker-compose.github.yml down"
echo "  Update images: ./deploy-github-registry.sh"

echo -e "${GREEN}🎉 Your AI Scraper System is now running and protected!${NC}"