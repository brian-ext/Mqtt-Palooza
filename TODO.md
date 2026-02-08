# Mqtt-Palooza: Universal Communication & Knowledge Fabric

## Vision Statement
Build a self-modifying, adaptive communication system where:
- **MQTT is the neural nervous system** for fast AI-to-AI and AI-to-Human communication
- **Website DNA stores intelligence** about every data source (optimal LLM settings, relevance filters, focus areas)
- **Context is refined en route** to minimize payload while maximizing relevance
- **LLMs define their focus** dynamically per communication instance
- **RF/Alternative Comms** enable a parallel, unstoppable network

## Core Pillars

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MQTT PALOOZA ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐         │
│    │  KNOWLEDGE  │     │    DATA     │     │ COMMUNICATION│        │
│    │   (DNA)     │     │  (Flow)     │     │  (Pub/Sub)  │        │
│    │             │     │             │     │             │        │
│    │ • Website   │     │ • Context    │     │ • MQTT      │        │
│    │   DNA       │     │   Refinement │     │ • RF        │        │
│    │ • Command   │     │ • Relevance  │     │ • Adapters  │        │
│    │   DNA       │     │   Scoring    │     │ • Webhooks  │        │
│    │ • LLM DNA   │     │ • Compression│     │ • Binary   │        │
│    └──────┬──────┘     └──────┬──────┘     └──────┬──────┘         │
│           │                    │                    │                 │
│           └────────────────────┼────────────────────┘                 │
│                                │                                      │
│                      ┌─────────▼─────────┐                           │
│                      │   FOCUS ENGINE    │                           │
│                      │                   │                           │
│                      │ • Task Mission    │                           │
│                      │ • Relevance Filter│                           │
│                      │ • Dynamic Context │                           │
│                      │ • Self-Modification│                          │
│                      └───────────────────┘                           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Foundation - Enhanced MQTT & Core DNA

### 1.1 MQTT Message Bus with Priority & Focus

```python
# mqtt_palooza/core/message_bus.py

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from uuid import uuid4
import time

class MessagePriority(Enum):
    """Priority levels for message routing"""
    CRITICAL = 1    # System alerts, immediate action
    HIGH = 2       # Time-sensitive scraping tasks
    NORMAL = 3      # Standard operations
    LOW = 4         # Background learning, DNA updates
    BATCH = 5       # Bulk data operations

class FocusMode(Enum):
    """LLM focus modes for dynamic context"""
    RELEVANCE = "relevance"      # Filter for relevant content
    EXTRACTION = "extraction"    # Structured data extraction
    ANALYSIS = "analysis"        # Deep analysis mode
    SUMMARIZATION = "summarize"  # Condense information
    REASONING = "reasoning"      # Logical reasoning focus
    CREATIVE = "creative"        # Novel approach generation
    VERIFICATION = "verify"      # Fact-checking mode

@dataclass
class MessageFocus:
    """Defines LLM focus for this message"""
    mode: FocusMode
    target_entities: List[str] = field(default_factory=list)
    relevance_threshold: float = 0.7
    max_tokens: int = 4096
    keywords: List[str] = field(default_factory=list)
    negative_keywords: List[str] = field(default_factory=list)
    
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
    """Context refined during message transit"""
    original_size: int
    current_size: int
    compression_ratio: float
    relevance_score: float
    filtered_elements: List[str]
    focus_mode: FocusMode
    timestamp: float = field(default_factory=time.time)
    hops: int = 0
    
    def add_hop(self, processor: str):
        self.hops += 1
        self.timestamp = time.time()

@dataclass  
class NeuralMessage:
    """Core message structure for the neural bus"""
    id: str = field(default_factory=lambda: str(uuid4())[:8])
    topic: str = ""
    priority: MessagePriority = MessagePriority.NORMAL
    focus: Optional[MessageFocus] = None
    payload: Dict[str, Any] = field(default_factory=dict)
    context: EnRouteContext = field(default_factory=EnRouteContext)
    source: str = ""
    destination: str = ""
    timestamp: float = field(default_factory=time.time)
    ttl_seconds: int = 300
    requires_ack: bool = False
    correlation_id: Optional[str] = None
    
    def to_binary(self) -> bytes:
        """Serialize for efficient transmission"""
        import msgpack
        return msgpack.packb({
            'id': self.id,
            't': self.topic,
            'p': self.priority.value,
            'f': self.focus.to_dict() if self.focus else None,
            'pl': self.payload,
            'c': {
                'os': self.context.original_size,
                'cs': self.context.current_size,
                'rs': self.context.relevance_score,
                'fe': self.context.filtered_elements,
                'fm': self.context.focus_mode.value,
                'h': self.context.hops
            },
            's': self.source,
            'd': self.destination,
            'ts': self.timestamp,
            'ttl': self.ttl_seconds
        })
    
    @classmethod
    def from_binary(cls, data: bytes) -> 'NeuralMessage':
        import msgpack
        raw = msgpack.unpackb(data)
        msg = cls(
            id=raw['id'],
            topic=raw['t'],
            priority=MessagePriority(raw['p']),
            payload=raw['pl'],
            source=raw['s'],
            destination=raw['d'],
            timestamp=raw['ts'],
            ttl_seconds=raw['ttl']
        )
        if raw['f']:
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
            compression_ratio=raw['c']['cs'] / max(raw['c']['os'], 1),
            relevance_score=raw['c']['rs'],
            filtered_elements=raw['c']['fe'],
            focus_mode=FocusMode(raw['c']['fm']),
            hops=raw['c']['h']
        )
        return msg
```

### 1.2 Context Refinement Engine (The "En Route" Processor)

```python
# mqtt_palooza/core/context_refiner.py

class ContextRefiner:
    """
    Refines context while messages transit through the neural bus.
    Each hop can optimize, filter, and focus the content.
    """
    
    def __init__(self, small_llm_url: str = "http://localhost:11434"):
        self.llm_url = small_llm_url
        self.refinement_rules: List[RefinementRule] = []
        
    async def refine_en_route(
        self, 
        message: NeuralMessage,
        processor_id: str
    ) -> NeuralMessage:
        """
        Refine message context as it passes through a processor.
        This is where the magic happens - context is optimized in transit.
        """
        # Track the hop
        message.context.add_hop(processor_id)
        
        # Apply focus mode refinements
        if message.focus:
            if message.focus.mode == FocusMode.RELEVANCE:
                await self._apply_relevance_filter(message)
            elif message.focus.mode == FocusMode.EXTRACTION:
                await self._apply_extraction_focus(message)
            elif message.focus.mode == FocusMode.SUMMARIZATION:
                await self._apply_summarization(message)
        
        # Apply general optimizations
        await self._compress_payload(message)
        await self._remove_duplicates(message)
        await self._prune_metadata(message)
        
        return message
    
    async def _apply_relevance_filter(self, message: NeuralMessage):
        """Filter content based on relevance threshold using small LLM"""
        payload = message.payload
        
        if 'html' in payload:
            # Extract only relevant sections
            relevant_sections = await self._extract_relevant_html(
                html=payload['html'],
                keywords=message.focus.keywords,
                threshold=message.focus.relevance_threshold
            )
            payload['html'] = relevant_sections
            message.context.filtered_elements.append('irrelevant_html')
        
        if 'text' in payload:
            # Score and filter text passages
            filtered_text = await self._score_and_filter_text(
                text=payload['text'],
                keywords=message.focus.keywords,
                negative_keywords=message.focus.negative_keywords,
                threshold=message.focus.relevance_threshold
            )
            payload['text'] = filtered_text
    
    async def _apply_extraction_focus(self, message: NeuralMessage):
        """Focus on specific entities for extraction"""
        target_entities = message.focus.target_entities
        
        payload = message.payload
        if 'html' in payload:
            # Use small LLM to extract only target entities
            extraction_result = await self._llm_extract_entities(
                html=payload['html'],
                entities=target_entities,
                context=f"Focus: {message.focus.mode.value}"
            )
            payload['extracted'] = extraction_result
            message.context.filtered_elements.append('non_target_content')
    
    async def _apply_summarization(self, message: NeuralMessage):
        """Condense content based on focus"""
        payload = message.payload
        max_tokens = message.focus.max_tokens
        
        if 'html' in payload:
            payload['summary'] = await self._llm_summarize(
                content=payload['html'],
                max_tokens=max_tokens,
                focus=message.focus.keywords
            )
            payload.pop('html', None)  # Remove full HTML
            message.context.filtered_elements.append('full_html')
    
    async def _llm_extract_entities(
        self, 
        html: str, 
        entities: List[str],
        context: str
    ) -> Dict:
        """Use small LLM to extract target entities"""
        prompt = f"""
        Extract only these entities from the HTML: {', '.join(entities)}
        Focus: {context}
        
        Return JSON with structure:
        {{
            "entities": {{entity_name: value}},
            "confidence_scores": {{entity_name: 0.0-1.0}},
            "context_snippets": {{entity_name: relevant_text}}
        }}
        """
        # Call local LLM
        return {}
```

### 1.3 Enhanced Website DNA with LLM Settings

```python
# mqtt_palooza/dna/website_dna.py

@dataclass
class LLMConfigDNA:
    """Optimal LLM settings for scraping this website"""
    # Model selection
    recommended_model: str = "llama3.1:8b"  # Default for speed
    deep_analysis_model: str = "llama3.1:70b"  # For complex pages
    
    # Context optimization
    optimal_context_length: int = 8192
    max_tokens_for_extraction: int = 2048
    context_truncation_strategy: str = "smart"  # "smart", "head", "tail", "hybrid"
    
    # Focus modes for different tasks
    task_focus_modes: Dict[str, FocusMode] = field(default_factory=lambda: {
        'navigation': FocusMode.RELEVANCE,
        'extraction': FocusMode.EXTRACTION,
        'analysis': FocusMode.ANALYSIS,
        'verification': FocusMode.VERIFICATION
    })
    
    # Extraction settings
    extraction_prompt_template: str = ""
    entity_list: List[str] = field(default_factory=list)
    
    # Performance hints
    expected_load_time_ms: int = 3000
    rate_limit_safe: bool = True
    requires_human_verification: bool = False
    
    # Learning history
    successful_prompts: List[Dict] = field(default_factory=list)
    failed_prompts: List[Dict] = field(default_factory=list)
    model_performance: Dict[str, Dict] = field(default_factory=dict)
    
    def get_optimal_settings(self, task_type: str) -> Dict:
        """Get optimal settings for a specific task"""
        return {
            'model': self.recommended_model if task_type != 'deep_analysis' 
                     else self.deep_analysis_model,
            'focus_mode': self.task_focus_modes.get(
                task_type, FocusMode.EXTRACTION
            ).value,
            'max_tokens': self.max_tokens_for_extraction,
            'prompt_template': self.extraction_prompt_template or self._default_prompt(task_type)
        }
    
    def record_success(self, task_type: str, prompt: str, metrics: Dict):
        """Record successful extraction for learning"""
        self.successful_prompts.append({
            'task_type': task_type,
            'prompt': prompt,
            'metrics': metrics,
            'timestamp': time.time()
        })
        # Keep only recent successes
        self.successful_prompts = self.successful_prompts[-100:]
        
        # Update performance tracking
        if task_type not in self.model_performance:
            self.model_performance[task_type] = {'successes': 0, 'total': 0}
        self.model_performance[task_type]['successes'] += 1
        self.model_performance[task_type]['total'] += 1
        
        # Auto-optimize if enough data
        if len(self.successful_prompts) >= 10:
            self._auto_optimize(task_type)
    
    def _auto_optimize(self, task_type: str):
        """Automatically optimize settings based on history"""
        successes = [s for s in self.successful_prompts 
                    if s['task_type'] == task_type]
        
        if not successes:
            return
            
        # Find optimal settings from history
        avg_tokens = sum(s['metrics'].get('tokens_used', 4096) 
                        for s in successes) / len(successes)
        
        self.max_tokens_for_extraction = int(avg_tokens * 1.2)  # 20% buffer
```

### 1.4 Command DNA - Terminal Intelligence

```python
# mqtt_palooza/dna/command_dna.py

@dataclass
class CommandDNA:
    """
    Stores intelligence about terminal commands and software interfaces.
    Enables natural language → command translation with auto-completion.
    """
    
    software_name: str = ""
    software_version: str = ""
    command_patterns: Dict[str, 'CommandPattern'] = field(default_factory=dict)
    
    # Auto-completion tree
    completion_tree: Dict = field(default_factory=dict)
    
    # Natural language mappings
    nl_to_command: Dict[str, List[Dict]] = field(default_factory=dict)
    
    # Documentation DNA
    doc_pages: List['DocPageDNA'] = field(default_factory=list)
    
    # Usage patterns learned
    common_workflows: List['WorkflowDNA'] = field(default_factory=list)
    
    # Generated shortcuts
    shortcuts: Dict[str, str] = field(default_factory=dict)
    
    async def learn_from_documentation(self, url: str, doc_content: str):
        """Extract command patterns from documentation pages"""
        # Use LLM to parse documentation
        prompt = f"""
        Extract all terminal commands and their usage from this documentation:
        
        {doc_content[:10000]}  # Limit context
        
        Return JSON:
        {{
            "commands": [
                {{
                    "command": "exact command string",
                    "description": "what it does",
                    "flags": [{{"flag": "-v", "description": "verbose"}}],
                    "examples": ["example usage"],
                    "related_commands": ["related command"]
                }}
            ],
            "workflows": [
                {{
                    "name": "workflow name",
                    "steps": ["step 1", "step 2"]
                }}
            ]
        }}
        """
        # Parse and store extracted patterns
    
    async def natural_language_to_command(
        self, 
        user_input: str,
        context: Optional[Dict] = None
    ) -> Dict:
        """Convert natural language to exact command"""
        # Search NL mappings first
        if user_input.lower() in self.nl_to_command:
            return self.nl_to_command[user_input.lower()][0]
        
        # Use LLM to match/generate
        prompt = f"""
        Convert this natural language to the best command:
        
        Input: "{user_input}"
        Software: {self.software_name}
        Available commands: {list(self.command_patterns.keys())}
        
        Return JSON:
        {{
            "command": "exact command string",
            "confidence": 0.0-1.0,
            "reasoning": "why this command fits",
            "alternatives": [{{"command": "...", "confidence": 0.5}}]
        }}
        """
        # Return best match
    
    def get_completions(self, partial: str) -> List[Dict]:
        """Get auto-completions for partial command"""
        completions = []
        
        # Check direct matches
        for cmd_name, pattern in self.command_patterns.items():
            if cmd_name.startswith(partial):
                completions.append({
                    'type': 'command',
                    'value': cmd_name,
                    'description': pattern.description
                })
            
            # Check flags
            for flag in pattern.flags:
                if flag['flag'].startswith(partial):
                    completions.append({
                        'type': 'flag',
                        'value': flag['flag'],
                        'description': flag['description']
                    })
        
        return sorted(completions, key=lambda x: x['value'])
```

---

## Phase 2: Adapter System

### 2.1 Universal Adapter Framework

```python
# mqtt_palooza/adapters/base.py

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ..core.neural_message import NeuralMessage

class MessageAdapter(ABC):
    """Base class for all communication adapters"""
    
    @abstractmethod
    async def send(self, message: NeuralMessage) -> bool:
        """Send message through this adapter"""
        pass
    
    @abstractmethod
    async def receive(self) -> Optional[NeuralMessage]:
        """Receive message from this adapter"""
        pass
    
    @abstractmethod
    def can_handle(self, platform: str) -> bool:
        """Check if this adapter handles the platform"""
        pass

# mqtt_palooza/adapters/telegram.py

class TelegramAdapter(MessageAdapter):
    """Adapter for Telegram messaging"""
    
    def __init__(self, bot_token: str, allowed_chats: List[str]):
        self.bot_token = bot_token
        self.allowed_chats = set(allowed_chats)
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
    
    async def send(self, message: NeuralMessage) -> bool:
        """Convert NeuralMessage to Telegram format"""
        telegram_message = {
            'chat_id': message.destination,
            'text': self._format_for_telegram(message),
            'parse_mode': 'Markdown',
            'reply_markup': self._create_keyboard(message)
        }
        # Send via Telegram API
        return True
    
    def _format_for_telegram(self, message: NeuralMessage) -> str:
        """Format message for Telegram with focus mode"""
        focus_emoji = {
            FocusMode.RELEVANCE: "🎯",
            FocusMode.EXTRACTION: "📊",
            FocusMode.ANALYSIS: "🔍",
            FocusMode.SUMMARIZATION: "📝",
            FocusMode.REASONING: "🧠",
            FocusMode.CREATIVE: "💡",
            FocusMode.VERIFICATION: "✅"
        }
        
        emoji = focus_emoji.get(message.focus.mode, "📨") if message.focus else "📨"
        
        return f"{emoji} *{message.topic}*\n\n{self._truncate_for_telegram(message.payload)}"
    
    async def receive(self) -> Optional[NeuralMessage]:
        """Receive Telegram updates and convert to NeuralMessage"""
        # Poll for updates
        pass
```

### 2.2 RF/Alternative Communication Adapter

```python
# mqtt_palooza/adapters/rf.py

class RFAdapter(MessageAdapter):
    """
    RF/Radio Frequency adapter for alternative communications.
    Enables parallel through Lo internetRa, Ham Radio, or mesh networks.
    """
    
    def __init__(self, device: str = "/dev/ttyUSB0", baudrate: int = 9600):
        self.device = device
        self.baudrate = baudrate
        self.serial = None
        
    async def send(self, message: NeuralMessage) -> bool:
        """Send message via RF"""
        # Serialize message for RF transmission
        rf_payload = self._serialize_for_rf(message)
        
        # Fragment if too long (RF has low bandwidth)
        fragments = self._fragment(rf_payload, max_size=256)
        
        for fragment in fragments:
            await self._transmit(fragment)
            
        return True
    
    def _serialize_for_rf(self, message: NeuralMessage) -> bytes:
        """Create compact RF-ready message"""
        # Use binary encoding for bandwidth efficiency
        return message.to_binary()
    
    async def _transmit(self, fragment: bytes):
        """Transmit fragment via hardware"""
        # For LoRa: use RFM95W or similar
        # For Ham: use AX.25 protocol
        # For Mesh: use some mesh networking library
        pass
```

---

## Phase 3: Neural Dashboard

### 3.1 Auto-Adjusting Context Dashboard

```typescript
// ai-scraper-dashboard/src/neural/Dashboard.tsx

class NeuralDashboard {
  async initialize() {
    // Auto-detect system capabilities
    await this.detectCapabilities();
    
    // Load DNA configurations
    this.websiteDNA = await this.loadWebsiteDNA();
    this.commandDNA = await this.loadCommandDNA();
    
    // Setup neural message bus
    this.messageBus = new NeuralMessageBus({
      onMessage: this.handleNeuralMessage.bind(this),
      onFocusChange: this.handleFocusChange.bind(this)
    });
  }
  
  async detectCapabilities() {
    // Detect LLM models available
    const models = await this.ollamaAPI.listModels();
    this.capabilities = {
      smallModel: models.includes('llama3.1:8b'),
      largeModel: models.includes('llama3.1:70b'),
      gpuMemory: await this.getGPUMemory(),
      contextWindow: 32768 // Detect actual window
    };
    
    // Adjust dashboard based on capabilities
    this.adjustUIForCapabilities();
  }
  
  adjustUIForCapabilities() {
    // Show/hide features based on capabilities
    if (!this.capabilities.smallModel) {
      this.showWarning('Small model not available - using API fallback');
    }
    
    // Set default context size
    this.maxContextSize = Math.min(
      this.capabilities.contextWindow,
      this.autoDetectOptimalContext()
    );
  }
  
  autoDetectOptimalContext(): number {
    // Analyze recent usage patterns
    const avgRecentUsage = this.getAverageRecentContextUsage();
    const gpuHeadroom = this.capabilities.gpuMemory / 4; // Reserve 75%
    
    return Math.min(avgRecentUsage * 1.5, gpuHeadroom);
  }
  
  handleFocusChange(newFocus: FocusMode) {
    // Update UI for new focus mode
    this.applyFocusTheme(newFocus);
    this.updateCommandPalette(newFocus);
    this.adjustStreamingSpeed(newFocus);
  }
}
```

---

## File Structure

```
mqtt_palooza/
├── core/
│   ├── message_bus.py         # MQTT neural message bus
│   ├── context_refiner.py     # En-route context optimization
│   ├── neural_message.py      # Core message structure
│   ├── focus_engine.py        # Dynamic focus management
│   └── protocol_adapters.py   # Binary/MQTT protocols
│
├── dna/
│   ├── website_dna.py         # Website intelligence DNA
│   ├── command_dna.py         # Terminal command DNA
│   ├── llm_config_dna.py      # LLM optimal settings DNA
│   └── rf_dna.py              # RF communication DNA
│
├── adapters/
│   ├── base.py                # Adapter interface
│   ├── telegram.py            # Telegram integration
│   ├── discord.py             # Discord integration
│   ├── email.py               # Email/SMTP adapter
│   ├── rf.py                  # RF/Radio adapter
│   └── webhook.py             # Generic webhook adapter
│
├── llm/
│   ├── focus_prompts.py       # Focus-optimized prompts
│   ├── context_optimizer.py   # Token optimization
│   └── multi_model_router.py  # Route to optimal model
│
├── dashboard/
│   ├── neural_ui.tsx         # Auto-adjusting dashboard
│   ├── command_palette.ts    # Natural language commands
│   └── focus_visualizer.ts   # Visualize focus modes
│
└── main.py                    # Entry point
```

---

## Implementation Priority

| Phase | Component | Priority | Reason |
|-------|-----------|----------|--------|
| 1 | NeuralMessage & MessageBus | P0 | Core foundation |
| 2 | ContextRefiner | P0 | Unique value proposition |
| 3 | LLMConfigDNA | P1 | Auto-optimization |
| 4 | CommandDNA | P1 | User experience |
| 5 | Telegram/Discord Adapters | P2 | Immediate utility |
| 6 | RF Adapter | P3 | Long-term vision |

---

## Success Metrics

- **Context Reduction**: 80%+ size reduction while maintaining relevance
- **Focus Accuracy**: LLM focus matches user intent 95%+ of time
- **Command DNA Coverage**: 80% of common commands matched naturally
- **Adapter Latency**: <100ms for message conversion
- **RF Throughput**: >1KB/min for mesh network

