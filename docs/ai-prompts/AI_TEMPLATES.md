# AI Instruction Templates

This document provides standardized templates for common AI operations across all repositories.

## General Templates

### 1. Code Modification Request
```json
{
    "type": "code_modification",
    "file": "path/to/file",
    "purpose": "Brief description of the change",
    "requirements": {
        "functionality": ["list", "of", "requirements"],
        "constraints": ["any", "limitations"],
        "testing": ["required", "tests"]
    },
    "context": {
        "related_files": ["other/relevant/files"],
        "dependencies": ["any/dependencies"],
        "background": "Additional context"
    }
}
```

### 2. Feature Implementation
```json
{
    "type": "feature_implementation",
    "feature": "Feature name",
    "scope": {
        "components": ["affected", "components"],
        "services": ["impacted", "services"]
    },
    "requirements": {
        "functional": ["list", "of", "requirements"],
        "non_functional": ["performance", "security"],
        "integration": ["integration", "points"]
    },
    "validation": {
        "tests": ["required", "tests"],
        "metrics": ["success", "metrics"]
    }
}
```

### 3. Bug Fix
```json
{
    "type": "bug_fix",
    "issue": {
        "description": "Problem description",
        "reproduction": ["steps", "to", "reproduce"],
        "impact": "Impact description"
    },
    "context": {
        "expected": "Expected behavior",
        "current": "Current behavior",
        "affected_areas": ["impacted", "areas"]
    },
    "constraints": {
        "backwards_compatibility": true,
        "performance": "requirements",
        "security": "considerations"
    }
}
```

## Repository-Specific Templates

### AI Scraper VM

#### Browser Automation Task
```json
{
    "type": "browser_automation",
    "target": {
        "url": "target_url",
        "selectors": ["css", "selectors"],
        "actions": ["click", "scroll", "wait"]
    },
    "data": {
        "extract": ["fields", "to", "extract"],
        "validate": ["validation", "rules"]
    },
    "error_handling": {
        "retries": 3,
        "timeout": 30,
        "recovery": ["recovery", "steps"]
    }
}
```

### AI Scraper Dashboard

#### Component Update
```json
{
    "type": "component_update",
    "component": {
        "name": "ComponentName",
        "path": "src/components/path",
        "type": "functional|class"
    },
    "changes": {
        "props": ["updated", "props"],
        "state": ["state", "changes"],
        "styling": ["style", "updates"]
    },
    "testing": {
        "unit": ["test", "cases"],
        "integration": ["test", "scenarios"]
    }
}
```

### Frankenstein DB

#### Query Optimization
```json
{
    "type": "query_optimization",
    "query": {
        "type": "select|update|delete",
        "tables": ["involved", "tables"],
        "conditions": ["where", "clauses"]
    },
    "optimization": {
        "indexes": ["suggested", "indexes"],
        "joins": ["join", "optimizations"],
        "caching": ["cache", "strategies"]
    },
    "validation": {
        "performance": {
            "current": "metrics",
            "target": "metrics"
        },
        "testing": ["test", "cases"]
    }
}
```

## Usage Guidelines

1. **Template Selection**
   - Choose the most appropriate template for the task
   - Customize fields as needed while maintaining structure
   - Include all required information

2. **Context Provision**
   - Always provide necessary context
   - Include related files and dependencies
   - Specify constraints and requirements

3. **Validation**
   - Include success criteria
   - Specify required tests
   - Define performance metrics

4. **Documentation**
   - Update documentation when adding new templates
   - Keep examples current
   - Document template modifications

5. **Security**
   - Follow security guidelines
   - Respect access limitations
   - Validate all inputs