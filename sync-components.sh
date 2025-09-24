#!/bin/bash

# AI Scraper System - Component Sync Script
# Syncs individual component repos into the production-VMs monorepo

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MONOREPO_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🤖 AI Scraper System - Component Sync"
echo "====================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to sync a component
sync_component() {
    local component_name="$1"
    local standalone_path="$MONOREPO_ROOT/$component_name"
    local monorepo_path="$SCRIPT_DIR/$component_name"

    echo -e "\n${BLUE}🔄 Syncing $component_name${NC}"

    # Check if standalone repo exists
    if [ ! -d "$standalone_path" ]; then
        echo -e "${RED}❌ Standalone repo not found: $standalone_path${NC}"
        return 1
    fi

    # Check if monorepo component exists
    if [ ! -d "$monorepo_path" ]; then
        echo -e "${YELLOW}⚠️  Monorepo component not found, creating: $monorepo_path${NC}"
        mkdir -p "$monorepo_path"
    fi

    # Get latest changes from standalone repo
    echo "📥 Pulling latest changes from standalone repo..."
    cd "$standalone_path"
    git fetch origin
    git checkout main
    git pull origin main

    # Copy files to monorepo (excluding .git)
    echo "📋 Copying files to monorepo..."
    cd "$standalone_path"
    # Use rsync to sync files, excluding .git and other unwanted files
    rsync -av --delete \
        --exclude='.git/' \
        --exclude='.github/' \
        --exclude='node_modules/' \
        --exclude='__pycache__/' \
        --exclude='*.pyc' \
        --exclude='.pytest_cache/' \
        --exclude='.DS_Store' \
        ./ "$monorepo_path/"

    # Special handling for .github directory - we want workflows but not issues/PR templates
    if [ -d ".github/workflows" ]; then
        echo "🔧 Syncing workflows..."
        mkdir -p "$monorepo_path/.github"
        cp -r .github/workflows "$monorepo_path/.github/"
    fi

    echo -e "${GREEN}✅ $component_name synced successfully${NC}"
}

# Function to commit changes in monorepo
commit_changes() {
    echo -e "\n${BLUE}💾 Committing changes to monorepo${NC}"

    cd "$SCRIPT_DIR"
    git add .

    # Check if there are changes to commit
    if git diff --cached --quiet; then
        echo -e "${YELLOW}ℹ️  No changes to commit${NC}"
        return 0
    fi

    # Create commit message
    local commit_msg="🔄 Auto-sync components

$(git diff --cached --name-only | head -10 | sed 's/^/- /')
$(if [ "$(git diff --cached --name-only | wc -l)" -gt 10 ]; then echo "- ... and $(($(git diff --cached --name-only | wc -l) - 10)) more files"; fi)"

    git commit -m "$commit_msg"
    echo -e "${GREEN}✅ Changes committed${NC}"
}

# Function to push changes
push_changes() {
    echo -e "\n${BLUE}🚀 Pushing changes to remote${NC}"

    cd "$SCRIPT_DIR"
    git push origin main
    echo -e "${GREEN}✅ Changes pushed${NC}"
}

# Main sync process
main() {
    echo "📍 Monorepo root: $MONOREPO_ROOT"
    echo "📍 Production-VMs path: $SCRIPT_DIR"

    # Parse command line arguments
    local specific_component=""
    while [[ $# -gt 0 ]]; do
        case $1 in
            --component)
                if [ -n "$2" ] && [[ "$2" != --* ]]; then
                    specific_component="$2"
                    shift 2
                else
                    echo "Error: --component requires a component name"
                    exit 1
                fi
                ;;
            -h|--help)
                echo "Usage: $0 [--component COMPONENT_NAME]"
                echo "Sync AI Scraper components from standalone repos to monorepo"
                echo ""
                echo "Options:"
                echo "  --component NAME    Sync only the specified component"
                echo "  -h, --help         Show this help message"
                echo ""
                echo "Available components: frankenstein-db, ai-scraper-vm, ai-scraper-dashboard"
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                echo "Use --help for usage information"
                exit 1
                ;;
        esac
    done

    # Components to sync
    local components=("frankenstein-db" "ai-scraper-vm" "ai-scraper-dashboard")

    # Filter components if specific one requested
    if [ -n "$specific_component" ]; then
        echo "🔍 Syncing specific component: $specific_component"
        components=("$specific_component")
    else
        echo "🔄 Syncing all components..."
    fi

    # Sync each component
    for component in "${components[@]}"; do
        if ! sync_component "$component"; then
            echo -e "${RED}❌ Failed to sync $component${NC}"
            exit 1
        fi
    done

    # Only commit and push if not in CI environment
    if [ -z "$CI" ]; then
        commit_changes
        push_changes
    fi

    echo -e "\n${GREEN}🎉 Components synced successfully!${NC}"
    echo "📊 Summary:"
    for component in "${components[@]}"; do
        echo "   - $component: ✅ Synced"
    done
}

# Run main function
main "$@"