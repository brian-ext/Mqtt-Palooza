# AI-Optimized Repository Structure

## Version Control Organization

### Current Structure
```
production-VMs/
├── ai-scraper-dashboard/    # Frontend dashboard
├── ai-scraper-vm/          # Core scraping logic
├── frankenstein-db/        # Database management
└── docs/
    └── ai-prompts/        # AI documentation and prompts
```

### Recommended Improvements

1. **Monorepo Integration**
   ```bash
   # Proposed structure
   ai-scraper-system/
   ├── apps/
   │   ├── dashboard/      # Former ai-scraper-dashboard
   │   └── vm/            # Former ai-scraper-vm
   ├── libs/
   │   ├── frankenstein-db/
   │   └── shared-utils/
   ├── docs/
   │   └── ai/
   └── tools/
       └── ci/
   ```

2. **Git Commit Standards**
   ```
   <type>(<scope>): <description>

   [optional body]

   [optional footer]
   ```

   Types:
   - feat: New feature
   - fix: Bug fix
   - docs: Documentation only
   - style: Code style changes
   - refactor: Code refactoring
   - test: Adding/modifying tests
   - chore: Maintenance tasks

   Example:
   ```
   feat(vm): implement intelligent retry mechanism for scraping

   - Add exponential backoff
   - Implement failure detection
   - Add logging for retry attempts

   Closes #123
   ```

3. **Branch Strategy**
   ```
   main
   ├── develop
   │   ├── feature/ai-retry-logic
   │   ├── fix/mqtt-connection
   │   └── docs/ai-capabilities
   └── hotfix/critical-error
   ```

## Real-Time Data Access

### MQTT Topic Structure
```
ai/
├── orchestrator/
│   ├── status
│   ├── commands
│   └── events
├── vm/
│   ├── status
│   ├── tasks
│   └── results
└── dashboard/
    ├── user_requests
    ├── updates
    └── notifications
```

### API Documentation
```yaml
openapi: 3.0.0
info:
  title: AI Scraper System API
  version: 1.0.0
paths:
  /api/v1/tasks:
    get:
      summary: List all scraping tasks
  /api/v1/status:
    get:
      summary: Get system status
  /api/v1/metrics:
    get:
      summary: Get performance metrics
```

## Code Standards

### Type Hints Example
```python
from typing import Dict, List, Optional

def process_scraping_task(
    task_id: str,
    config: Dict[str, any],
    retries: Optional[int] = 3
) -> List[Dict[str, any]]:
    """Process a web scraping task.

    Args:
        task_id: Unique identifier for the task
        config: Configuration dictionary for the task
        retries: Number of retry attempts (default: 3)

    Returns:
        List of extracted data dictionaries

    Raises:
        ScrapingError: If scraping fails after all retries
    """
    pass
```

### Configuration Management
```python
# config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    """System configuration with environment variables.
    
    Environment Variables:
        MQTT_HOST: MQTT broker hostname
        MQTT_PORT: MQTT broker port
        MQTT_USER: MQTT username for AI access
        MQTT_PASSWORD: MQTT password for AI access
        DB_URL: Database connection URL
    """
    mqtt_host: str
    mqtt_port: int
    mqtt_user: str
    mqtt_password: str
    db_url: str

    class Config:
        env_file = ".env"
```

### Testing Structure
```python
# test_scraper.py
import pytest
from unittest.mock import Mock, patch

def test_scraping_task_success():
    """Test successful scraping task execution."""
    pass

def test_scraping_task_retry():
    """Test retry mechanism for failed scraping."""
    pass

def test_scraping_task_timeout():
    """Test timeout handling in scraping tasks."""
    pass
```