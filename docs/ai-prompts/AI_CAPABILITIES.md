# AI Capabilities and Instructions

This document outlines the AI capabilities, permissions, and instructions for each repository in the AI Scraper System.

## General Structure

Each repository should have the following AI-related documentation:

1. **Capabilities Overview**
   - What the AI can access and modify
   - Available tools and functions
   - Scope and limitations

2. **Permission Levels**
   - Read/write access to specific directories
   - API endpoints accessible to AI
   - Security boundaries and restrictions

3. **Examples and Templates**
   - Common use cases with example prompts
   - Code modification templates
   - Error handling examples

4. **Integration Points**
   - How AI interfaces with the repository
   - Data flow and communication channels
   - Required environment setup

## Repository-Specific Capabilities

### ai-scraper-vm

- **Capabilities**:
  - Access to browser automation code
  - MQTT message handling
  - AI model integration (Ollama)
  - Docker environment management

- **Permissions**:
  - Read/write access to `projects/` directory
  - Read-only access to configuration files
  - Full access to test environments

- **Examples**:
  ```json
  {
    "task": "web_scraping",
    "ai_prompt": "Extract product information from e-commerce page",
    "capabilities": ["browser_control", "data_extraction", "error_handling"]
  }
  ```

### ai-scraper-dashboard

- **Capabilities**:
  - Frontend component modification
  - State management
  - API integration
  - UI/UX improvements

- **Permissions**:
  - Full access to `src/components/`
  - Read-only access to configuration
  - Style modification permissions

### frankenstein-db

- **Capabilities**:
  - Database schema suggestions
  - Query optimization
  - Data modeling assistance
  - Migration planning

- **Permissions**:
  - Read access to schema definitions
  - Suggestion-only for structural changes
  - Full access to test data

## Standard Prompting Templates

1. **Code Modification Request**:
   ```
   Task: [Brief description]
   File: [Target file path]
   Purpose: [Why this change is needed]
   Constraints: [Any limitations or requirements]
   ```

2. **Feature Implementation**:
   ```
   Feature: [Feature name]
   Scope: [Affected components]
   Requirements: [Specific requirements]
   Integration: [Integration points]
   ```

3. **Bug Fix Request**:
   ```
   Issue: [Problem description]
   Reproduction: [Steps to reproduce]
   Expected: [Expected behavior]
   Current: [Current behavior]
   ```

## Best Practices

1. Always specify the context and scope of AI operations
2. Use standardized templates for common operations
3. Include clear examples for complex tasks
4. Document any limitations or restrictions
5. Keep security considerations in mind

## Updating This Documentation

1. When adding new capabilities, update both general and repository-specific sections
2. Keep examples current and relevant
3. Document any changes to permission structures
4. Maintain consistent formatting and structure