# Documentation Standards for AI-Friendly Code

## Overview
This document defines documentation standards to make the codebase more accessible and understandable for AI tools.

## Documentation Hierarchy

### 1. Repository Level
Each repository must have:

```markdown
# Repository Name

## Overview
Brief description of the repository's purpose and role in the system.

## Architecture
High-level architecture diagram and description.

## Setup
Step-by-step setup instructions.

## Development
Guidelines for development and contribution.

## Testing
Testing strategy and instructions.

## API Reference
Links to detailed API documentation.
```

### 2. Module Level
Each Python module should have:

```python
"""Module Name

This module handles [specific functionality].

Typical usage example:
    foo = ClassName()
    bar = foo.method(param1, param2)

Attributes:
    MODULE_LEVEL_VARIABLE: Description of the variable.
"""
```

### 3. Class Level
Use Google style docstrings for classes:

```python
class ClassName:
    """Summary of class purpose.

    This class provides functionality for [...].

    Attributes:
        attr1 (str): Description of attr1
        attr2 (int): Description of attr2

    Example:
        ```python
        obj = ClassName(param1, param2)
        result = obj.method()
        ```
    """
```

### 4. Method Level
Detailed method documentation:

```python
def method_name(param1: str, param2: int) -> bool:
    """Summary of method purpose.

    Extended description of method functionality.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: Description of when this error occurs
        TypeError: Description of when this error occurs

    Example:
        ```python
        result = obj.method_name("test", 42)
        ```
    """
```

## Comments

### 1. Code Comments
Use comments to explain WHY, not WHAT:

```python
# BAD - Describes what the code does
x = x + 1  # Increment x

# GOOD - Explains why this operation is necessary
x = x + 1  # Compensate for zero-based indexing in API response
```

### 2. TODO Comments
Standardized format for TODO comments:

```python
# TODO(username): Brief description of what needs to be done
# TODO(#123): Reference to issue number
# FIXME(username): Description of bug that needs fixing
```

## Type Hints

### 1. Basic Types
```python
from typing import List, Dict, Optional, Union

def process_data(
    items: List[str],
    config: Dict[str, any],
    timeout: Optional[int] = None
) -> Union[str, None]:
    pass
```

### 2. Custom Types
```python
from typing import TypeVar, Protocol

T = TypeVar('T')

class Scrapeable(Protocol):
    """Protocol for scrapeable items."""
    
    def get_url(self) -> str:
        """Get URL to scrape."""
        pass
```

## File Organization

### 1. Import Order
```python
# Standard library imports
import os
import sys
from typing import List, Dict

# Third-party imports
import requests
import paho.mqtt.client as mqtt

# Local application imports
from .models import User
from .utils import format_response
```

### 2. Module Structure
```python
"""Module docstring."""

# Imports (as above)

# Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3

# Exception classes
class CustomError(Exception):
    pass

# Classes
class MainClass:
    pass

# Helper functions
def helper_function():
    pass

# Main function (if applicable)
def main():
    pass

if __name__ == '__main__':
    main()
```

## API Documentation

### 1. OpenAPI/Swagger
```yaml
openapi: 3.0.0
info:
  title: API Title
  version: 1.0.0
paths:
  /endpoint:
    get:
      summary: Endpoint purpose
      description: Detailed description
      parameters:
        - name: param
          in: query
          description: Parameter description
      responses:
        '200':
          description: Success response
```

### 2. GraphQL Schema
```graphql
"""
Description of the type.
"""
type Example {
  """
  Description of the field.
  """
  field: String!
}
```

## Maintenance

### 1. Documentation Review
- Review documentation during code reviews
- Keep examples up to date
- Validate all code examples
- Update documentation when APIs change

### 2. Tools
- Use documentation generators
- Implement documentation testing
- Automate format checking
- Generate API documentation from code

### 3. Version Control
- Document breaking changes
- Maintain changelog
- Tag documentation versions
- Archive old versions