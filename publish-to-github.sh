#!/bin/bash

set -e

echo "🚀 Publishing AI Scraper System to GitHub Container Registry..."
echo "🔒 Protected by AGPL-3.0 License - Big Tech Cannot Steal This!"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
GITHUB_USERNAME="${GITHUB_USERNAME:-scrapedat}"
REGISTRY="ghcr.io"
IMAGE_PREFIX="${REGISTRY}/${GITHUB_USERNAME}"

# Check if GitHub token is set
if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${RED}❌ GITHUB_TOKEN environment variable not set${NC}"
    echo -e "${YELLOW}Please create a Personal Access Token with 'write:packages' permission${NC}"
    echo -e "${BLUE}1. Go to: https://github.com/settings/tokens${NC}"
    echo -e "${BLUE}2. Generate new token (classic)${NC}"
    echo -e "${BLUE}3. Select scopes: write:packages, read:packages${NC}"
    echo -e "${BLUE}4. Set: export GITHUB_TOKEN=your_token_here${NC}"
    exit 1
fi

# Login to GitHub Container Registry
echo -e "${BLUE}🔐 Logging in to GitHub Container Registry...${NC}"
echo $GITHUB_TOKEN | docker login $REGISTRY -u $GITHUB_USERNAME --password-stdin

# Function to build and push image
build_and_push() {
    local component=$1
    local path=$2
    local dockerfile=$3
    local image_name="${IMAGE_PREFIX}/${component}"

    echo -e "${YELLOW}📦 Building ${component}...${NC}"

    # Build the image
    if [ -f "${path}/${dockerfile}" ]; then
        docker build -f "${path}/${dockerfile}" \
            --build-arg BUILD_DATE="$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
            --build-arg VERSION="${VERSION:-latest}" \
            --build-arg REVISION="${GITHUB_SHA:-$(git rev-parse HEAD)}" \
            -t "${image_name}:latest" "$path"
    else
        echo -e "${RED}❌ Dockerfile not found: ${path}/${dockerfile}${NC}"
        return 1
    fi

    # Tag with version if provided
    if [ ! -z "$VERSION" ]; then
        docker tag "${image_name}:latest" "${image_name}:${VERSION}"
    fi

    # Push the image
    echo -e "${BLUE}⬆️ Pushing ${component} to GitHub Container Registry...${NC}"
    docker push "${image_name}:latest"

    if [ ! -z "$VERSION" ]; then
        docker push "${image_name}:${VERSION}"
    fi

    echo -e "${GREEN}✅ ${component} published successfully!${NC}"
    echo -e "${GREEN}📦 Available at: ${REGISTRY}/${GITHUB_USERNAME}/${component}${NC}"
    echo -e "${PURPLE}🛡️  Protected by AGPL-3.0 - Amazon/Google cannot use this commercially!${NC}"
}

# Get version from git tag or use timestamp
VERSION=$(git describe --tags --exact-match 2>/dev/null || echo "")
if [ -z "$VERSION" ]; then
    VERSION=$(date +%Y%m%d-%H%M%S)
    echo -e "${YELLOW}ℹ️ No git tag found, using timestamp version: ${VERSION}${NC}"
fi

echo -e "${BLUE}🏷️ Publishing version: ${VERSION}${NC}"
echo -e "${PURPLE}🛡️ All components protected by AGPL-3.0 License${NC}"

# Build and push all components
echo -e "${YELLOW}🔨 Building and pushing all components...${NC}"

# 1. FrankensteinDB
build_and_push "frankenstein-db" "./frankenstein-db" "Dockerfile.production"

# 2. AI Scraper VM
build_and_push "ai-scraper-vm" "./ai-scraper-vm" "Dockerfile"

# 3. Dashboard (create Dockerfile if needed)
if [ ! -f "./ai-scraper-dashboard/Dockerfile" ]; then
    echo -e "${YELLOW}📝 Creating Dockerfile for Dashboard...${NC}"
    cat > ./ai-scraper-dashboard/Dockerfile << 'EOF'
FROM node:18-alpine

# Add metadata labels
LABEL org.opencontainers.image.title="AI Scraper Dashboard"
LABEL org.opencontainers.image.description="Desktop monitoring interface for AI Scraper System"
LABEL org.opencontainers.image.vendor="AI Scraper Contributors"
LABEL org.opencontainers.image.licenses="AGPL-3.0"
LABEL org.opencontainers.image.source="https://github.com/scrapedat/ai-scraper-dashboard"

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Build application
RUN npm run build

# Expose port
EXPOSE 3000

# Start application
CMD ["npm", "start"]
EOF
fi

build_and_push "ai-scraper-dashboard" "./ai-scraper-dashboard" "Dockerfile"

echo -e "${GREEN}🎉 All components published successfully to GitHub Container Registry!${NC}"
echo -e "${GREEN}🔗 View packages at: https://github.com/orgs/${GITHUB_USERNAME}/packages${NC}"
echo -e "${PURPLE}🛡️ All containers are protected by AGPL-3.0 License${NC}"
echo -e "${PURPLE}🚫 Amazon, Google, Meta, and other big tech companies cannot use this commercially!${NC}"

# Display usage instructions
echo -e "${BLUE}📋 Usage Instructions:${NC}"
echo "Pull and run any component:"
echo "  docker pull ${IMAGE_PREFIX}/frankenstein-db:latest"
echo "  docker pull ${IMAGE_PREFIX}/ai-scraper-vm:latest"
echo "  docker pull ${IMAGE_PREFIX}/ai-scraper-dashboard:latest"
echo ""
echo "Update docker-compose.yml to use GitHub registry images:"
echo "  image: ${IMAGE_PREFIX}/frankenstein-db:latest"
echo ""
echo -e "${CYAN}🔒 License Protection:${NC}"
echo "  • AGPL-3.0 requires source code sharing for network services"
echo "  • Big tech cannot embed this in proprietary products"
echo "  • Forces open-source for any commercial SaaS usage"
echo "  • Protects against corporate exploitation"