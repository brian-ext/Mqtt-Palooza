# Mqtt-Palooza: Universal Communication & Knowledge Fabric

"""
Mqtt-Palooza - An adaptive intelligent communication system.

Core Components:
- NeuralMessage: Binary-serializable messages with focus modes
- ContextRefiner: En-route context optimization
- Darwin: Evolutionary adaptation system
- DNA: Self-modifying knowledge structures
- Adapters: Multi-platform communication bridges
"""

__version__ = "1.0.0"
__author__ = "Mqtt-Palooza Team"

from .core.neural_message import NeuralMessage, MessagePriority, FocusMode
from .core.darwin import (
    DarwinOrchestrator,
    DarwinEvolutionType,
    DarwinMutation,
    create_darwin_mutation
)

__all__ = [
    # Core
    "NeuralMessage",
    "MessagePriority", 
    "FocusMode",
    # Darwin
    "DarwinOrchestrator",
    "DarwinEvolutionType",
    "DarwinMutation",
    "create_darwin_mutation"
]

