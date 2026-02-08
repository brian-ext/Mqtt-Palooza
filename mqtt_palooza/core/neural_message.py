"""
Neural Message Bus
The core communication layer for Mqtt-Palooza.

Provides binary-serializable messages with:
- Priority levels for QoS
- Focus modes for LLM context optimization
- En-route context refinement tracking
- Constitutional compliance verification
"""

import uuid
import time
import json
import hashlib
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
import msgpack


class MessagePriority(Enum):
    """Priority levels for message routing (QoS)"""
    CRITICAL = 1    # System alerts, immediate action
    HIGH = 2        # Time-sensitive scraping tasks
    NORMAL = 3      # Standard operations
    LOW = 4         # Background learning, DNA updates
    BATCH = 5       # Bulk data operations


class FocusMode(Enum):
    """LLM focus modes for dynamic context optimization"""
    RELEVANCE = "relevance"       # Filter for relevant content
    EXTRACTION = "extraction"     # Structured data extraction
    ANALYSIS = "analysis"         # Deep analysis mode
    SUMMARIZATION = "summarize"   # Condense information
    REASONING = "reasoning"        # Logical reasoning focus
    CREATIVE = "creative"          # Novel approach generation
    VERIFICATION = "verify"        # Fact-checking mode
    NAVIGATION = "navigation"      # Page navigation focus


@dataclass
class MessageFocus:
    """Defines LLM focus for this message."""
    mode: FocusMode = None
    target_entities: List[str] = None
    relevance_threshold: float = 0.7
    max_tokens: int = 4096
    keywords: List[str] = None
    negative_keywords: List[str] = None
    
    def __post_init__(self):
        if self.mode is None:
            self.mode = FocusMode.EXTRACTION
        if self.target_entities is None:
            self.target_entities = []
        if self.keywords is None:
            self.keywords = []
        if self.negative_keywords is None:
            self.negative_keywords = []
    
    def to_dict(self) -> Dict:
        return {
            'mode': self.mode.value,
            'target_entities': self.target_entities,
            'relevance_threshold': self.relevance_threshold,
            'max_tokens': self.max_tokens,
            'keywords': self.keywords,
            'negative_keywords': self.negative_keywords
        }


@dataclass
class EnRouteContext:
    """Context refined during message transit."""
    original_size: int = 0
    current_size: int = 0
    compression_ratio: float = 0.0
    relevance_score: float = 0.0
    filtered_elements: List[str] = None
    focus_mode: FocusMode = None
    timestamp: float = 0.0
    hops: int = 0
    refinements: List[Dict] = None
    
    def __post_init__(self):
        if self.filtered_elements is None:
            self.filtered_elements = []
        if self.refinements is None:
            self.refinements = []
        if self.focus_mode is None:
            self.focus_mode = FocusMode.EXTRACTION
        if self.timestamp == 0.0:
            self.timestamp = time.time()


@dataclass
class NeuralMessage:
    """
    Core message structure for the neural communication bus.
    """
    id: str = None
    topic: str = ""
    priority: MessagePriority = None
    focus: MessageFocus = None
    payload: Dict = None
    context: EnRouteContext = None
    source: str = ""
    destination: str = ""
    timestamp: float = 0.0
    ttl_seconds: int = 300
    requires_ack: bool = False
    correlation_id: str = None
    constitutional_compliance: bool = True
    
    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())[:8]
        if self.priority is None:
            self.priority = MessagePriority.NORMAL
        if self.focus is None:
            self.focus = MessageFocus()
        if self.payload is None:
            self.payload = {}
        if self.context is None:
            self.context = EnRouteContext()
        if self.timestamp == 0.0:
            self.timestamp = time.time()
    
    def to_binary(self) -> bytes:
        """Serialize to binary for efficient transmission."""
        data = {
            'id': self.id,
            't': self.topic,
            'p': self.priority.value,
            'f': self.focus.to_dict(),
            'pl': self.payload,
            'c': {
                'os': self.context.original_size,
                'cs': self.context.current_size,
                'rs': self.context.relevance_score,
                'fe': self.context.filtered_elements,
                'fm': self.context.focus_mode.value,
                'h': self.context.hops,
                'r': self.context.refinements
            },
            's': self.source,
            'd': self.destination,
            'ts': self.timestamp,
            'ttl': self.ttl_seconds,
            'ack': self.requires_ack,
            'corr': self.correlation_id,
            'cc': self.constitutional_compliance
        }
        return msgpack.packb(data)
    
    @classmethod
    def from_binary(cls, data: bytes) -> 'NeuralMessage':
        """Deserialize from binary."""
        raw = msgpack.unpackb(data)
        
        msg = cls(
            id=raw['id'],
            topic=raw['t'],
            priority=MessagePriority(raw['p']),
            payload=raw['pl'],
            source=raw['s'],
            destination=raw['d'],
            timestamp=raw['ts'],
            ttl_seconds=raw['ttl'],
            requires_ack=raw['ack'],
            correlation_id=raw.get('corr'),
            constitutional_compliance=raw.get('cc', True)
        )
        
        if raw.get('f'):
            msg.focus = MessageFocus(
                mode=FocusMode(raw['f']['mode']),
                target_entities=raw['f']['target_entities'],
                relevance_threshold=raw['f']['relevance_threshold'],
                max_tokens=raw['f']['max_tokens'],
                keywords=raw['f']['keywords'],
                negative_keywords=raw['f']['negative_keywords']
            )
        
        msg.context = EnRouteContext(
            original_size=raw['c']['os'],
            current_size=raw['c']['cs'],
            relevance_score=raw['c']['rs'],
            filtered_elements=raw['c']['fe'],
            focus_mode=FocusMode(raw['c']['fm']),
            hops=raw['c']['h'],
            refinements=raw['c']['r']
        )
        
        return msg
    
    def to_json(self) -> str:
        """Serialize to JSON for debugging."""
        return json.dumps(self.to_dict(), indent=2)
    
    def to_dict(self) -> Dict:
        """Serialize to dictionary."""
        return {
            'id': self.id,
            'topic': self.topic,
            'priority': self.priority.name if self.priority else 'NORMAL',
            'focus': self.focus.to_dict() if self.focus else None,
            'payload': self.payload,
            'context': {
                'original_size': self.context.original_size,
                'current_size': self.context.current_size,
                'compression_ratio': self.context.compression_ratio,
                'relevance_score': self.context.relevance_score,
                'filtered_elements': self.context.filtered_elements,
                'focus_mode': self.context.focus_mode.value if self.context.focus_mode else 'extraction',
                'hops': self.context.hops,
                'refinements': self.context.refinements
            },
            'source': self.source,
            'destination': self.destination,
            'timestamp': self.timestamp,
            'ttl_seconds': self.ttl_seconds,
            'requires_ack': self.requires_ack,
            'correlation_id': self.correlation_id,
            'constitutional_compliance': self.constitutional_compliance
        }
    
    def is_expired(self) -> bool:
        """Check if message has expired."""
        return (time.time() - self.timestamp) > self.ttl_seconds
    
    def create_signature(self) -> str:
        """Create message signature for integrity."""
        data = f"{self.id}:{self.topic}:{self.timestamp}"
        return hashlib.blake2b(data.encode(), digest_size=8).hexdigest()


class MessageBus:
    """Neural Message Bus for pub/sub messaging."""
    
    def __init__(self, broker_host: str = "localhost", broker_port: int = 1883):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.subscribers: Dict[str, List[callable]] = {}
        self.message_history: List[NeuralMessage] = []
        self.max_history = 1000
        
    def subscribe(self, topic: str, handler: callable):
        """Subscribe to a topic."""
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(handler)
    
    def publish(self, message: NeuralMessage) -> bool:
        """Publish a message to the bus."""
        if not self._check_compliance(message):
            return False
        
        for handler in self.subscribers.get(message.topic, []):
            try:
                handler(message)
            except Exception as e:
                print(f"Handler error: {e}")
        
        self.message_history.append(message)
        if len(self.message_history) > self.max_history:
            self.message_history.pop(0)
        
        return True
    
    def _check_compliance(self, message: NeuralMessage) -> bool:
        """Check constitutional compliance."""
        restricted = ['password', 'secret', 'api_key']
        for field in str(message.payload).lower():
            if field in restricted:
                return False
        return True


def create_scrape_request(
    url: str,
    selectors: Dict,
    focus_mode: FocusMode = None,
    source: str = "dashboard",
    destination: str = "scraper-vm"
) -> NeuralMessage:
    """Factory: Create a scraping request message."""
    if focus_mode is None:
        focus_mode = FocusMode.EXTRACTION
    
    return NeuralMessage(
        topic="scrape/request",
        payload={'url': url, 'selectors': selectors, 'action': 'scrape'},
        source=source,
        destination=destination,
        priority=MessagePriority.HIGH,
        focus=MessageFocus(
            mode=focus_mode,
            target_entities=list(selectors.keys()),
            keywords=list(selectors.keys())
        ),
        requires_ack=True
    )


def create_llm_request(
    prompt: str,
    focus_mode: FocusMode,
    model: str = "llama3.1:8b",
    source: str = "orchestrator",
    destination: str = "ollama"
) -> NeuralMessage:
    """Factory: Create an LLM processing request."""
    return NeuralMessage(
        topic="llm/request",
        payload={'prompt': prompt, 'model': model, 'focus': focus_mode.value},
        source=source,
        destination=destination,
        priority=MessagePriority.NORMAL,
        focus=MessageFocus(mode=focus_mode, max_tokens=8192)
    )


def create_dna_update(
    dna_type: str,
    dna_data: Dict,
    source: str = "scraper",
    destination: str = "frankenstein-db"
) -> NeuralMessage:
    """Factory: Create a DNA update message."""
    return NeuralMessage(
        topic=f"dna/update/{dna_type}",
        payload={'dna_type': dna_type, 'data': dna_data, 'timestamp': time.time()},
        source=source,
        destination=destination,
        priority=MessagePriority.LOW,
        requires_ack=True
    )


if __name__ == "__main__":
    print("Neural Message Demo")
    print("=" * 50)
    
    msg = create_scrape_request(
        url="https://example.com",
        selectors={"title": "h1", "content": ".main"},
        focus_mode=FocusMode.EXTRACTION
    )
    
    binary = msg.to_binary()
    print(f"Binary size: {len(binary)} bytes")
    print(f"\nJSON:\n{msg.to_json()}")
    
    restored = NeuralMessage.from_binary(binary)
    print(f"\nRound-trip ID match: {msg.id == restored.id}")

