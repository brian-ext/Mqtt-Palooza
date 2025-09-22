#!/bin/bash

set -e

echo "🧠 Ollama Model Management for AI Scraper System"
echo "🔒 Protected by AGPL-3.0 License"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
NC='\033[0m'

# Configuration
OLLAMA_CONTAINER="ollama"
OLLAMA_PROXY_URL="http://localhost:11435"
OLLAMA_USERNAME="ollama"
OLLAMA_PASSWORD="scraper"
SMALL_MODEL="llama3.1:8b"
LARGE_MODEL="llama3.1:70b"

# Function to check if Ollama is running
check_ollama() {
    if ! docker-compose -f docker-compose.ollama.yml ps ollama | grep -q "Up"; then
        echo -e "${RED}❌ Ollama service is not running${NC}"
        echo -e "${YELLOW}Start it with: docker-compose -f docker-compose.ollama.yml up -d ollama${NC}"
        exit 1
    fi
}

# Function to pull models
pull_models() {
    echo -e "${BLUE}📥 Pulling AI models...${NC}"

    echo -e "${YELLOW}Pulling small model: $SMALL_MODEL${NC}"
    docker-compose -f docker-compose.ollama.yml exec -T ollama ollama pull $SMALL_MODEL

    echo -e "${YELLOW}Pulling large model: $LARGE_MODEL${NC}"
    docker-compose -f docker-compose.ollama.yml exec -T ollama ollama pull $LARGE_MODEL

    echo -e "${GREEN}✅ All models downloaded!${NC}"
}

# Function to list available models
list_models() {
    echo -e "${BLUE}📋 Available models:${NC}"
    docker-compose -f docker-compose.ollama.yml exec -T ollama ollama list
}

# Function to test small model
test_small() {
    echo -e "${BLUE}🧪 Testing small model ($SMALL_MODEL)...${NC}"
    docker-compose -f docker-compose.ollama.yml exec -T ollama ollama run $SMALL_MODEL "Analyze this web scraping task: extract product names and prices from an e-commerce page. Respond in JSON format." | head -20
}

# Function to test large model
test_large() {
    echo -e "${BLUE}🧪 Testing large model ($LARGE_MODEL)...${NC}"
    echo -e "${YELLOW}Note: Large model may take 10-30 seconds to respond${NC}"
    docker-compose -f docker-compose.ollama.yml exec -T ollama ollama run $LARGE_MODEL "Analyze this complex web scraping scenario: You need to scrape a dynamic e-commerce site with infinite scroll, handle anti-bot measures, and extract structured product data. Provide a detailed technical approach." | head -30
}

# Function to show model info
model_info() {
    echo -e "${BLUE}📊 Model Information:${NC}"
    echo -e "${GREEN}Small Model ($SMALL_MODEL):${NC}"
    echo "  • Purpose: Real-time scraping decisions"
    echo "  • Response time: <2 seconds"
    echo "  • Use case: Quick analysis, filtering, basic extraction"
    echo ""
    echo -e "${GREEN}Large Model ($LARGE_MODEL):${NC}"
    echo "  • Purpose: Complex analysis & reasoning"
    echo "  • Response time: 10-60 seconds"
    echo "  • Use case: Deep analysis, pattern recognition, strategic decisions"
}

# Function to test API proxy authentication
test_proxy() {
    echo -e "${BLUE}🔒 Testing secure API proxy...${NC}"

    # Test without authentication (should fail)
    echo -e "${YELLOW}Testing without authentication:${NC}"
    if curl -s -o /dev/null -w "%{http_code}" $OLLAMA_PROXY_URL/api/tags | grep -q "401"; then
        echo -e "${GREEN}✅ Authentication required (good)${NC}"
    else
        echo -e "${RED}❌ No authentication required${NC}"
    fi

    # Test with authentication (should work)
    echo -e "${YELLOW}Testing with authentication:${NC}"
    if curl -s -u $OLLAMA_USERNAME:$OLLAMA_PASSWORD $OLLAMA_PROXY_URL/api/tags | grep -q "models"; then
        echo -e "${GREEN}✅ Authentication successful${NC}"
    else
        echo -e "${RED}❌ Authentication failed${NC}"
    fi
}

# Function to clean up models
cleanup() {
    echo -e "${YELLOW}🧹 Cleaning up unused models...${NC}"
    docker-compose -f docker-compose.ollama.yml exec -T ollama ollama list
    echo -e "${RED}This will remove all models except currently loaded ones.${NC}"
    read -p "Continue? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose -f docker-compose.ollama.yml exec -T ollama ollama prune
        echo -e "${GREEN}✅ Cleanup completed${NC}"
    fi
}

# Main menu
case "${1:-help}" in
    "pull")
        check_ollama
        pull_models
        ;;
    "list")
        check_ollama
        list_models
        ;;
    "test-small")
        check_ollama
        test_small
        ;;
    "test-large")
        check_ollama
        test_large
        ;;
    "info")
        model_info
        ;;
    "benchmark")
        check_ollama
        benchmark
        ;;
    "cleanup")
        check_ollama
        cleanup
        ;;
    "test-proxy")
        test_proxy
        ;;
    "help"|*)
        echo -e "${BLUE}🧠 Ollama Model Management${NC}"
        echo ""
        echo "Usage: $0 <command>"
        echo ""
        echo "Commands:"
        echo "  pull       - Download both small and large models"
        echo "  list       - Show available models"
        echo "  test-small - Test the small model with a simple task"
        echo "  test-large - Test the large model with a complex task"
        echo "  test-proxy   - Test secure API authentication"
        echo "  info         - Show model information and use cases"
        echo "  benchmark  - Compare response times"
        echo "  cleanup    - Remove unused models"
        echo "  help       - Show this help"
        echo ""
        echo "Examples:"
        echo "  $0 pull"
        echo "  $0 test-small"
        echo "  $0 benchmark"
        ;;
esac