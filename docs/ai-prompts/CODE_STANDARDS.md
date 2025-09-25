# Code Standards for AI-Friendly Development

## Overview
This document defines coding standards to make the codebase more accessible and maintainable for AI tools.

## Naming Conventions

### 1. Python
```python
# Variables and Functions (snake_case)
user_name = "John"
def calculate_total(items: List[Dict]):
    pass

# Classes (PascalCase)
class UserAccount:
    pass

# Constants (UPPERCASE)
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# Private attributes (single leading underscore)
class Example:
    def __init__(self):
        self._private_var = 42
```

### 2. TypeScript/JavaScript
```typescript
// Variables and Functions (camelCase)
const userName = "John";
function calculateTotal(items: Array<object>): number {
    return 0;
}

// Classes (PascalCase)
class UserAccount {
    // Properties
    private readonly id: string;
}

// Constants (UPPERCASE)
const MAX_RETRIES = 3;
```

## Type Hints and Interfaces

### 1. Python Type Hints
```python
from typing import List, Dict, Optional, Union, TypeVar

T = TypeVar('T')

def process_data(
    items: List[Dict[str, any]],
    config: Optional[Dict[str, any]] = None,
    callback: Callable[[T], None] = None
) -> Union[List[T], None]:
    pass

class DataProcessor[T]:  # Python 3.12+ generic class
    def process(self, item: T) -> T:
        pass
```

### 2. TypeScript Interfaces
```typescript
interface User {
    id: string;
    name: string;
    email?: string;  // Optional property
}

type ProcessorConfig = {
    readonly timeout: number;
    retries?: number;
}

class DataProcessor<T> {
    process(item: T): Promise<T> {
        // Implementation
    }
}
```

## Code Organization

### 1. File Structure
```python
# example_module.py

"""Module docstring with purpose and usage examples."""

# Standard library imports
import os
from typing import Dict, List

# Third-party imports
import requests
from pydantic import BaseModel

# Local imports
from .utils import helper_function
from .types import CustomType

# Constants
DEFAULT_TIMEOUT = 30

# Type definitions
ConfigDict = Dict[str, any]

# Main class
class ExampleClass:
    """Main class docstring."""
    
    def __init__(self):
        """Initialize the class."""
        pass
```

### 2. Class Organization
```python
class WebScraper:
    """Web scraper implementation."""
    
    def __init__(self, config: Dict[str, any]):
        """Initialize scraper with configuration."""
        self._config = config
        self._session = None
    
    # Public methods first
    def scrape(self, url: str) -> Dict[str, any]:
        """Main public interface."""
        pass
    
    # Protected methods (with leading underscore)
    def _create_session(self) -> None:
        """Create HTTP session."""
        pass
    
    # Private methods (with double underscore)
    def __validate_config(self) -> bool:
        """Internal config validation."""
        pass
```

## Error Handling

### 1. Custom Exceptions
```python
class ScraperError(Exception):
    """Base exception for scraper errors."""
    pass

class ConnectionError(ScraperError):
    """Raised when connection fails."""
    pass

class ValidationError(ScraperError):
    """Raised when validation fails."""
    pass

def process_url(url: str) -> Dict[str, any]:
    """Process URL with proper error handling."""
    try:
        response = fetch_url(url)
        data = validate_response(response)
        return process_data(data)
    except ConnectionError as e:
        logger.error(f"Connection failed: {e}")
        raise
    except ValidationError as e:
        logger.error(f"Validation failed: {e}")
        raise
```

## Configuration Management

### 1. Environment Variables
```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    """System configuration."""
    
    # Database
    db_host: str
    db_port: int
    db_name: str
    
    # API
    api_key: str
    api_url: str
    
    # MQTT
    mqtt_host: str
    mqtt_port: int = 1883  # Default value
    
    class Config:
        env_file = ".env"
```

## Testing Standards

### 1. Test Organization
```python
# test_example.py

import pytest
from unittest.mock import Mock

class TestWebScraper:
    """Test suite for WebScraper class."""
    
    @pytest.fixture
    def scraper(self):
        """Create test scraper instance."""
        return WebScraper(config={})
    
    def test_successful_scrape(self, scraper):
        """Test successful scraping operation."""
        result = scraper.scrape("http://example.com")
        assert result is not None
    
    def test_error_handling(self, scraper):
        """Test error handling during scraping."""
        with pytest.raises(ScraperError):
            scraper.scrape("invalid-url")
```

## Logging

### 1. Structured Logging
```python
import structlog

logger = structlog.get_logger()

def process_task(task_id: str, data: Dict[str, any]) -> None:
    """Process task with structured logging."""
    logger.info(
        "processing_task",
        task_id=task_id,
        data_size=len(data),
        timestamp=datetime.now().isoformat()
    )
```

## Code Formatting

### 1. Tool Configuration
```toml
# pyproject.toml

[tool.black]
line-length = 88
target-version = ['py39']
include = '\.pyi?$'

[tool.isort]
profile = "black"
multi_line_output = 3
```

### 2. Pre-commit Hooks
```yaml
# .pre-commit-config.yaml

repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
        language_version: python3.9
  
  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
        name: isort (python)