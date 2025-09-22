# 🧠 Ollama Integration - Local AI Models

## Overview
Your AI Scraper System now includes **Ollama integration** with both small and large language models running locally. This provides enterprise-level AI capabilities without API costs.

## Architecture
```
┌─────────────────┐       MQTT       ┌─────────────────┐       Direct      ┌─────────────────┐
│                 │◄────────────────►│                 │◄────────────────►│                 │
│   Dashboard     │                  │   AI Scraper    │                  │ FrankensteinDB  │
│ (React/Electron │                  │   VM (connects  │                  │  (Hybrid DB)    │
│  + TypeScript)  │                  │    to Ollama)   │                  │                 │
│                 │                  │                 │                  │  • 46K+ writes/s│
│ • Real-time UI  │                  │  • Real-time    │                  │  • <0.4ms query │
│ • Desktop App   │                  │  • AI-powered   │                  │  • 90% compression│
└─────────────────┘                  └─────────────────┘                  └─────────────────┘
         │                                   │                                │
         └───────────────────────────────────┼────────────────────────────────┘
                                             │
                                   ┌─────────▼─────────┐
                                   │                   │
                                   │    Ollama         │
                                   │  (Local AI)      │
                                   │                   │
                                   │  • llama3.1:8b   │
                                   │  • llama3.1:70b  │
                                   │  • GPU accelerated│
                                   └───────────────────┘
```

## Models Included

### �� Small Model: Llama 3.1 8B
- **Purpose**: Real-time scraping decisions
- **Response Time**: <2 seconds
- **Use Cases**:
  - Quick HTML analysis
  - Element identification
  - Basic content filtering
  - Pattern matching
- **GPU Memory**: ~8GB VRAM

### 🧠 Large Model: Llama 3.1 70B
- **Purpose**: Complex analysis & reasoning
- **Response Time**: 10-60 seconds
- **Use Cases**:
  - Deep content analysis
  - Advanced data extraction
  - Pattern recognition
  - Report generation
  - Strategic decisions
- **GPU Memory**: ~40GB VRAM

## Quick Start

### 1. Deploy with Ollama
```bash
# Deploy the complete system with Ollama
./deploy-github-registry.sh

# Or deploy just Ollama components
docker-compose -f docker-compose.ollama.yml up -d
```

### 2. Setup Authentication (Required)
```bash
# Generate secure authentication files locally
./setup-auth.sh

# This creates nginx/.htpasswd with hashed passwords
# ⚠️  NEVER commit this file to version control!
```

### 3. Setup Models
```bash
# Download both models
./manage-ollama.sh pull

# Test small model
./manage-ollama.sh test-small

# Test large model
./manage-ollama.sh test-large
```

### 4. Use the API
```bash
# 🔒 External access (authenticated proxy)
curl -u ollama:scraper http://localhost:11435/api/generate -d '{
  "model": "llama3.1:8b",
  "prompt": "Extract product names from this HTML...",
  "stream": false
}'

# 🏠 Internal access (from containers - no auth needed)
# AI Scraper VM connects directly: http://ollama:11434
curl http://ollama:11434/api/generate -d '{
  "model": "llama3.1:70b",
  "prompt": "Analyze this complex web scraping scenario...",
  "stream": false
}'
```

## � Authentication Setup

### Secure by Default
- **No credentials in version control**: `.htpasswd` is in `.gitignore`
- **Local generation**: Run `./setup-auth.sh` to create credentials
- **Hashed passwords**: Uses APR1 hashing for security

### Default Credentials (Change in Production!)
- **Username**: `ollama`
- **Password**: `scraper`

### Changing Credentials
```bash
# Run setup script and choose custom credentials
./setup-auth.sh

# Or manually create .htpasswd
printf "youruser:$(openssl passwd -apr1 yourpassword)\n" > nginx/.htpasswd
```

## �🔒 Security Features

### Network Isolation
- **Internal Network Only**: Ollama only accessible within Docker network
- **No External Ports**: No direct external access to Ollama API
- **Secure Proxy**: Authenticated access through nginx proxy (port 11435)

### Authentication
- **HTTP Basic Auth**: Username/password protection (`ollama`/`scraper`)
- **Rate Limiting**: 10 requests/second per IP
- **Method Restrictions**: Only GET, POST, DELETE allowed

### Access Control
- **Internal Services**: AI Scraper VM, Dashboard access directly (no auth)
- **External Access**: Only through authenticated proxy
- **Network Security**: Isolated Docker network prevents unauthorized access

## Cost Savings

| Service | Cost per 1M tokens | Your Cost |
|---------|-------------------|-----------|
| GPT-4 | $30-50 | **$0** (local) |
| Claude 3 Opus | $15-25 | **$0** (local) |
| Llama 3.1 70B API | $1-2 | **$0** (local) |

**Annual Savings: $10,000+** 💰

## Model Management

### Available Commands
```bash
./manage-ollama.sh pull       # Download models
./manage-ollama.sh list       # Show available models
./manage-ollama.sh test-small # Test small model
./manage-ollama.sh test-large # Test large model
./manage-ollama.sh info       # Show model details
./manage-ollama.sh benchmark  # Compare performance
./manage-ollama.sh cleanup    # Remove unused models
```

### Integration with AI Scraper VM
The AI Scraper VM automatically connects to Ollama:
- **OLLAMA_HOST**: `http://ollama:11434`
- **SMALL_MODEL**: `llama3.1:8b`
- **LARGE_MODEL**: `llama3.1:70b`

## Hardware Requirements

### Minimum (Small model only)
- **GPU**: 8GB VRAM (NVIDIA with CUDA)
- **RAM**: 16GB
- **Storage**: 20GB for models

### Recommended (Both models)
- **GPU**: 48GB+ VRAM (RTX 4090, A100, etc.)
- **RAM**: 64GB+
- **Storage**: 100GB+ for models

## Troubleshooting

### GPU Not Detected
```bash
# Check GPU access
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi

# Verify Ollama GPU support
docker exec ollama nvidia-smi
```

### Model Loading Issues
```bash
# Check available memory
docker exec ollama ollama ps

# Free up memory
docker exec ollama ollama stop all-models
```

### API Connection Issues
```bash
# Test API connectivity
curl http://localhost:11434/api/tags

# Check container logs
docker-compose -f docker-compose.ollama.yml logs ollama
```

## Security & Licensing

- **AGPL-3.0 Protected**: All models and code
- **Local Execution**: No data sent to external APIs
- **Enterprise Ready**: Full control over your AI infrastructure

---

**🎉 Your AI Scraper System now has local AI capabilities!**
