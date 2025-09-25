# Frankenstein DB - AI Capabilities

## Overview
This document details the AI capabilities and permissions within the frankenstein-db repository.

## Directory Structure Access

```
frankenstein-db/
├── src/
│   ├── models/      # Limited access - Schema definitions
│   ├── queries/     # Full access - Query optimization
│   ├── utils/       # Limited access - Utility functions
│   └── migrations/  # Read-only - Database migrations
├── tests/           # Full access - Test creation
└── config/          # Read-only - Configuration
```

## AI Capabilities

### 1. Schema Management
- Analyze database schemas
- Suggest optimizations
- Generate migrations
- Document data models

### 2. Query Optimization
- Analyze query performance
- Suggest indexes
- Optimize complex queries
- Generate query patterns

### 3. Data Modeling
- Design data structures
- Implement relationships
- Generate validation rules
- Optimize storage patterns

### 4. Testing
- Generate test cases
- Create sample data
- Validate migrations
- Performance testing

## Example Prompts

### Schema Analysis
```python
task = {
    "type": "schema_analysis",
    "description": "Optimize product catalog schema",
    "focus": ["indexing", "relationships", "constraints"],
    "performance_targets": {
        "query_time": "< 100ms",
        "storage_efficiency": "high"
    }
}
```

### Query Optimization
```python
task = {
    "type": "query_optimization",
    "description": "Optimize complex product search",
    "requirements": {
        "filters": ["category", "price", "availability"],
        "sort": ["relevance", "price"],
        "performance": "sub-second"
    }
}
```

## Security Considerations

1. **Schema Access**
   - Read-only access to production schemas
   - Can suggest but not implement changes
   - Must validate all modifications

2. **Data Access**
   - No access to production data
   - Use sample data for testing
   - Follow data privacy rules

3. **Query Security**
   - Must use parameterized queries
   - No direct write operations
   - Validate all inputs

## Integration Points

1. **ORM Layer**
   - Model definitions
   - Query builders
   - Relationship mapping

2. **Migration System**
   - Schema versions
   - Data transformations
   - Rollback procedures

3. **Testing Framework**
   - Unit tests
   - Integration tests
   - Performance tests

## Best Practices

1. Document all schema changes
2. Include rollback plans
3. Test performance impact
4. Maintain backwards compatibility
5. Follow naming conventions

## Performance Guidelines

1. Proper indexing strategies
2. Query optimization patterns
3. Data normalization rules
4. Caching strategies
5. Batch processing patterns