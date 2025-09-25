# AI MQTT Access Configuration

## Overview
This document defines the MQTT topic structure and access patterns for AI components in the system.

## MQTT Access Configuration

### AI User Configuration
```yaml
# mosquitto/config/ai-user.conf
user ai-agent
topic read ai/#
topic read $SYS/#
topic write ai/agent/#
```

### Topic Structure

```
ai/
├── agent/                     # AI agent communications
│   ├── status                # AI agent status updates
│   ├── requests              # AI agent requests
│   └── responses             # System responses to AI
├── orchestrator/             # System orchestration
│   ├── status               # Overall system status
│   ├── commands             # System-wide commands
│   └── events               # System events
├── vm/                      # VM-specific topics
│   ├── status              # VM status updates
│   ├── tasks               # Scraping tasks
│   └── results             # Task results
└── dashboard/              # Dashboard topics
    ├── user_requests      # User-initiated requests
    ├── updates           # UI updates
    └── notifications     # System notifications
```

## Message Schemas

### Status Updates
```json
{
    "type": "status",
    "component": "vm|dashboard|orchestrator",
    "timestamp": "ISO8601",
    "status": {
        "state": "running|stopped|error",
        "metrics": {
            "cpu": "float",
            "memory": "float",
            "tasks_pending": "int"
        }
    }
}
```

### Task Messages
```json
{
    "type": "task",
    "task_id": "uuid",
    "timestamp": "ISO8601",
    "parameters": {
        "url": "string",
        "selectors": ["css_selectors"],
        "timeout": "int"
    },
    "status": "pending|running|completed|failed"
}
```

### Event Messages
```json
{
    "type": "event",
    "event_id": "uuid",
    "timestamp": "ISO8601",
    "category": "info|warning|error",
    "message": "string",
    "details": {}
}
```

## Access Patterns

### AI Agent Responsibilities
1. Monitor system status via status topics
2. Process and respond to user requests
3. Coordinate tasks across components
4. Report its own status and actions

### Security Considerations
1. Use TLS for all MQTT connections
2. Implement authentication for all clients
3. Restrict topic access based on client role
4. Monitor and log all AI agent actions

## Integration Examples

### Python MQTT Client
```python
import paho.mqtt.client as mqtt
from typing import Callable

class AIMQTTClient:
    """MQTT client for AI agent integration."""
    
    def __init__(self, host: str, port: int, username: str, password: str):
        """Initialize MQTT client with AI agent credentials."""
        self.client = mqtt.Client()
        self.client.username_pw_set(username, password)
        
    def on_message(self, client: mqtt.Client, userdata: any, msg: mqtt.MQTTMessage):
        """Handle incoming MQTT messages."""
        topic = msg.topic
        payload = json.loads(msg.payload)
        self.process_message(topic, payload)
        
    def process_message(self, topic: str, payload: dict):
        """Process incoming messages based on topic."""
        if topic.startswith('ai/agent/requests'):
            self.handle_request(payload)
        elif topic.startswith('ai/orchestrator/status'):
            self.update_system_status(payload)
```

### Subscribe to Topics
```python
def subscribe_to_topics(client: mqtt.Client):
    """Subscribe to relevant MQTT topics."""
    topics = [
        ('ai/agent/#', 1),        # AI agent topics
        ('ai/orchestrator/#', 1),  # System orchestration
        ('ai/vm/#', 1),           # VM updates
        ('ai/dashboard/#', 1)      # Dashboard updates
    ]
    client.subscribe(topics)
```

## Testing

### Topic Validation
```python
def test_mqtt_topics():
    """Test MQTT topic structure and permissions."""
    client = AIMQTTClient(host, port, 'ai-agent', 'password')
    
    # Test topic access
    assert client.has_permission('ai/agent/status')
    assert client.has_permission('ai/orchestrator/status')
    assert not client.has_permission('admin/#')
```

### Message Validation
```python
def test_message_schema():
    """Test MQTT message schema validation."""
    message = {
        "type": "status",
        "component": "vm",
        "timestamp": "2025-09-25T10:00:00Z",
        "status": {
            "state": "running",
            "metrics": {
                "cpu": 0.5,
                "memory": 0.7,
                "tasks_pending": 3
            }
        }
    }
    assert validate_message_schema(message)
```