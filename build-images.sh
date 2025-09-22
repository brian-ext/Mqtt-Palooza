#!/bin/bash

# AI Scraper System - Docker Image Builder
# Builds and tags images for GitHub Container Registry

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REGISTRY="ghcr.io/scrapedat"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo -e "${BLUE}🚀 Building AI Scraper System Docker Images${NC}"
echo -e "${BLUE}Registry: ${REGISTRY}${NC}"
echo -e "${BLUE}Timestamp: ${TIMESTAMP}${NC}"
echo

# Function to build and tag image
build_image() {
    local component=$1
    local dockerfile_path=$2
    local dockerfile_name=$3
    local image_name="${REGISTRY}/${component}"

    echo -e "${YELLOW}📦 Building ${component}...${NC}"

    # Build the image
    if [ -f "${dockerfile_path}/${dockerfile_name}" ]; then
        docker build -f "${dockerfile_path}/${dockerfile_name}" -t "${image_name}:latest" -t "${image_name}:${TIMESTAMP}" "${dockerfile_path}"
        echo -e "${GREEN}✅ Built ${component}${NC}"
    else
        echo -e "${RED}❌ ${dockerfile_name} not found for ${component} at ${dockerfile_path}${NC}"
        return 1
    fi

    # Show image info
    docker images "${image_name}:latest"
    echo
}

# Build FrankensteinDB
echo -e "${BLUE}Building FrankensteinDB...${NC}"
build_image "frankenstein-db" "frankenstein-db" "Dockerfile.production"

# Build AI Scraper VM
echo -e "${BLUE}Building AI Scraper VM...${NC}"
build_image "ai-scraper-vm" "ai-scraper-vm" "Dockerfile.production"

# Build AI Scraper Dashboard
echo -e "${BLUE}Building AI Scraper Dashboard...${NC}"
build_image "ai-scraper-dashboard" "ai-scraper-dashboard" "Dockerfile"

echo -e "${GREEN}🎉 All images built successfully!${NC}"
echo
echo -e "${BLUE}📋 Built Images:${NC}"
docker images "${REGISTRY}/*" | head -20

echo
echo -e "${YELLOW}💡 Next Steps:${NC}"
echo -e "1. Test images locally: ${BLUE}docker run -p 3000:3000 ${REGISTRY}/ai-scraper-dashboard:latest${NC}"
echo -e "2. Push to registry: ${BLUE}./publish-to-github.sh${NC}"
echo -e "3. Deploy: ${BLUE}./deploy-github-registry.sh${NC}"

echo
echo -e "${GREEN}✅ Docker images ready for GitHub Container Registry!${NC}"