# Ollama Docker Compute Analysis

## Where Compute Comes From:
1. **Host Machine Hardware** - CPU cores, RAM, GPU
2. **Docker Resource Limits** - Container constraints
3. **Model Size** - Different models need different resources
4. **GPU Acceleration** - If available and enabled

## Typical Resource Requirements:
- **Small models (7B)**: 4-8GB RAM, decent CPU
- **Medium models (13B)**: 8-16GB RAM, good CPU  
- **Large models (30B+)**: 16-32GB+ RAM, powerful CPU/GPU
- **GPU acceleration**: Significantly faster inference

## Your Current Setup:
- AI Scraper VM has Docker installed
- Could run Ollama as additional container
- Compute comes from your deployment host
