# SCIMF Branding and Philosophy

## Our Vision
The SCIMF (Sustainable Collaborative Integrative Management Framework) is dedicated to fostering collaboration and integration in project management, prioritizing sustainable practices that benefit both the community and environment.

## Brand Promise
By choosing SCIMF, you are committing to a framework that not only aims to achieve project success but also champions sustainability, community involvement, and integrative systems thinking.

## Core Values
- **Sustainability:** Prioritizing eco-friendly practices in all projects.
- **Collaboration:** Encouraging teamwork and community engagement.
- **Innovation:** Continuously improving processes and approaches for better outcomes.
- **Integrity:** Upholding transparency and accountability in all our actions.

Join us in making a positive impact with SCI, MF!

[🤝 Contributing](./CONTRIBUTING.md) • [📋 Code of Conduct](./CODE_OF_CONDUCT.md) • [🔒 Security](./SECURITY.md)

## 🔒 AGPL-3.0 License Benefitscraper System - Production Ready

**Version:** 1.0 Production Ready
**License:** AGPL-3.0 (Community Protected)
**Registry:** GitHub Container Registry (Free)
**Status:** Open Source & Community Driven 🌟

## 🔒 AGPL-3.0 License Benefits

This project is licensed under **AGPL-3.0** - ensuring it remains free and open for the community.

### Why AGPL-3.0?

- ✅ **Network Copyleft**: Promotes source code sharing for network services
- ✅ **SaaS Transparency**: Cloud deployments stay open source
- ✅ **Community Focus**: Keeps the software accessible and collaborative
- ✅ **Long-term Freedom**: Prevents proprietary restrictions
- ✅ **Open Development**: Encourages contribution and improvement

### License Advantages:

- � **Free Distribution**: Use, modify, and share freely
- � **Source Transparency**: Always inspectable and improvable
- 🤝 **Community Collaboration**: Open development process
- 🛡️ **Future Protection**: Safeguards against commercial exploitation

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

1. **Copyleft for Network Services**: Ensures source code availability for network deployments
2. **Patent Protection**: Contributors provide patent licenses to users
3. **Freedom Preservation**: Maintains open access without additional restrictions
4. **Global Coverage**: Applies worldwide for consistent protection

### License Benefits:

- **SaaS Transparency**: Cloud services must share their source code
- **Infrastructure Freedom**: Promotes open cloud development
- **Enterprise Collaboration**: Encourages open integration
- **Platform Openness**: Supports ecosystem-wide collaboration

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
- Support collaborative development
- Build for the community

## 📞 Support & Community

- **Issues:** [GitHub Issues](https://github.com/scrapedat/ai-scraper-dashboard/issues)
- **Discussions:** [GitHub Discussions](https://github.com/scrapedat/ai-scraper-dashboard/discussions)
- **Documentation:** [System Architecture](./SYSTEM_ARCHITECTURE.md)

## ⚖️ License Summary

**AGPL-3.0** - GNU Affero General Public License v3.0

- ✅ **Free Software**: Can be used, modified, and distributed freely
- ✅ **Copyleft Protection**: Modifications must be shared under same license
- ✅ **Network Service Protection**: SaaS deployments stay open source
- ✅ **Patent Protection**: Contributors provide patent licenses
- ✅ **Community Freedom**: Ensures long-term open access

---

**🎉 Your AI Scraper System is now ready for the open-source community!**

*Built with ❤️ for collaborative development • Protected by AGPL-3.0 • September 2025*
