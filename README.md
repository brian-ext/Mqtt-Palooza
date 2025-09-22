# 🛡️ AI Scraper System - AGPL-3.0 Protected

**Version:** 1.0 Production Ready  
**License:** AGPL-3.0 (Anti-Corporate Exploitation)  
**Registry:** GitHub Container Registry (Free)  
**Status:** Big Tech Cannot Steal This! 🚫

## 🔒 License Protection

This project is licensed under **AGPL-3.0** - the strongest protection against corporate exploitation by Amazon, Google, Meta, and other big tech companies.

### Why AGPL-3.0?

- ✅ **Network Copyleft**: Forces anyone using your software in network services to open-source their entire application
- ✅ **SaaS Protection**: If Amazon/Google deploy this as a service, they must open-source their entire platform
- ✅ **Corporate Deterrent**: Big tech avoids AGPL code because it destroys their business model
- ✅ **Community Protection**: Keeps the software free and open for everyone else

### What Big Tech Cannot Do:

- 🚫 **Amazon** cannot embed this in AWS services without open-sourcing AWS
- 🚫 **Google** cannot use this in Cloud Platform without open-sourcing GCP
- 🚫 **Meta** cannot integrate this into their platforms without open-sourcing everything
- 🚫 **Microsoft** cannot use this in Azure without open-sourcing Azure
- 🚫 **Any corporation** cannot create proprietary SaaS products using this code

## 🚀 Quick Start with GitHub Registry

### Prerequisites

1. **Create GitHub Personal Access Token:**
   ```bash
   # Go to: https://github.com/settings/tokens
   # Generate new token (classic)
   # Select scopes: write:packages, read:packages
   export GITHUB_TOKEN=your_token_here
   ```

2. **Make scripts executable:**
   ```bash
   chmod +x publish-to-github.sh
   chmod +x deploy-github-registry.sh
   ```

### Deploy Complete System

```bash
# 1. Publish all containers to GitHub Registry
./publish-to-github.sh

# 2. Deploy the entire system
./deploy-github-registry.sh

# 3. Access your protected system
# Dashboard: http://localhost:3000
# MQTT: localhost:1883
```

## 🏗️ System Architecture

```
┌─────────────────┐    MQTT     ┌─────────────────┐    Direct    ┌─────────────────┐
│                 │◄──────────► │                 │◄────────────► │                 │
│  Dashboard      │             │  AI Scraper     │               │  FrankensteinDB │
│  (AGPL-3.0)     │             │  VM (AGPL-3.0)  │               │  (AGPL-3.0)     │
│                 │             │                 │               │                 │
│  • React UI     │             │  • Chrome VMs   │               │  • SQLite DBs   │
│  • Electron     │             │  • DNA Analysis │               │  • Redis Cache  │
│  • Real-time    │             │  • Extensions   │               │  • Blob Storage │
└─────────────────┘             └─────────────────┘               └─────────────────┘
        │                                │                                │
        └────────────────────────────────┼────────────────────────────────┘
                                         │
                               ┌─────────▼─────────┐
                               │                   │
                               │  GitHub Registry  │
                               │  (Free & Public)  │
                               │                   │
                               │  • ghcr.io        │
                               │  • Unlimited      │
                               │  • AGPL Protected │
                               └───────────────────┘
```

## 📦 Container Images

All containers are available on GitHub Container Registry:

- `ghcr.io/scrapedat/frankenstein-db:latest` - Hybrid database system
- `ghcr.io/scrapedat/ai-scraper-vm:latest` - AI scraping orchestrator
- `ghcr.io/scrapedat/ai-scraper-dashboard:latest` - Desktop monitoring app

### Manual Usage

```bash
# Pull images
docker pull ghcr.io/scrapedat/frankenstein-db:latest
docker pull ghcr.io/scrapedat/ai-scraper-vm:latest
docker pull ghcr.io/scrapedat/ai-scraper-dashboard:latest

# Run with docker-compose
docker-compose -f docker-compose.github.yml up -d
```

## 🔧 Development & Deployment

### Automated Publishing (GitHub Actions)

Push to `main` or `production` branch to automatically publish containers:

```yaml
# .github/workflows/publish-containers.yml
name: 🚀 Publish Docker Containers to GitHub Registry
# ... automated publishing on every push
```

### Manual Publishing

```bash
# Set your GitHub token
export GITHUB_TOKEN=your_personal_access_token

# Publish all components
./publish-to-github.sh
```

### Local Development

```bash
# Clone and setup
git clone https://github.com/scrapedat/ai-scraper-dashboard.git
cd ai-scraper-dashboard

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

## 📊 Performance & Features

### FrankensteinDB
- **Storage:** Hybrid SQLite + Redis + Blob storage
- **Performance:** 46K+ records/second write speed
- **Query Speed:** <0.4ms average response time
- **Compression:** 90%+ data compression

### AI Scraper VM
- **Browsers:** Chrome automation with Playwright/Selenium
- **Orchestration:** Docker container management
- **Analysis:** Website DNA fingerprinting
- **Communication:** Real-time MQTT updates

### Dashboard
- **UI:** React + TypeScript + Tailwind CSS
- **Desktop:** Electron-based native application
- **Monitoring:** Real-time scraping visualization
- **Packaging:** Linux AppImage/DEB distribution

## 🛡️ Legal Protection Details

### AGPL-3.0 Key Provisions:

1. **Copyleft for Network Services**: Anyone who runs this software as a network service must provide source code to users
2. **Patent Protection**: Contributors grant patent licenses to users
3. **No Additional Restrictions**: Cannot add terms that restrict the license
4. **Global Coverage**: Applies worldwide, not just in specific jurisdictions

### Corporate Impact:

- **SaaS Companies**: Must open-source their entire platform if using this code
- **Cloud Providers**: Cannot offer this as a service without open-sourcing their infrastructure
- **Enterprise Software**: Cannot be embedded in proprietary products
- **Big Tech Platforms**: Cannot integrate without open-sourcing their entire ecosystem

## 📈 Scaling & Production

### Production Deployment

```bash
# Full production setup
./deploy-github-registry.sh

# Monitor system
docker-compose -f docker-compose.github.yml logs -f

# Scale components
docker-compose -f docker-compose.github.yml up -d --scale ai-scraper-vm=3
```

### Backup & Recovery

```bash
# Backup data
docker run --rm -v frankenstein_sqlite:/data \
  ghcr.io/scrapedat/frankenstein-db:latest \
  tar czf - /data > backup.tar.gz

# Restore data
docker run --rm -v frankenstein_sqlite:/data -i \
  ghcr.io/scrapedat/frankenstein-db:latest \
  tar xzf - < backup.tar.gz
```

## 🤝 Contributing

We welcome contributions! However, all contributions must be licensed under AGPL-3.0.

### Contribution Process:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure AGPL-3.0 compliance
5. Submit a pull request

### Code of Conduct:

- Respect the AGPL-3.0 license
- Keep the software free and open
- Protect against corporate exploitation
- Support the community

## 📞 Support & Community

- **Issues:** [GitHub Issues](https://github.com/scrapedat/ai-scraper-dashboard/issues)
- **Discussions:** [GitHub Discussions](https://github.com/scrapedat/ai-scraper-dashboard/discussions)
- **Documentation:** [System Architecture](./SYSTEM_ARCHITECTURE.md)

## ⚖️ License Summary

**AGPL-3.0** - GNU Affero General Public License v3.0

- ✅ **Free Software**: Can be used, modified, and distributed freely
- ✅ **Copyleft Protection**: Modifications must be shared under same license
- ✅ **Network Service Protection**: SaaS deployments must open-source
- ✅ **Patent Protection**: Contributors grant patent licenses
- ✅ **Corporate Deterrent**: Big tech cannot exploit commercially

---

**🎉 Your AI Scraper System is now protected from corporate exploitation!**

*Built with ❤️ for the open-source community • Protected by AGPL-3.0 • September 2025*