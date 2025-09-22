# GitHub Repository Setup Guide

This guide helps you configure branch protections and other safety measures for your AI Scraper System repositories.

## 🛡️ Branch Protection Setup

### For Each Repository (scrapedat/scrapedat, ai-scraper-dashboard, ai-scraper-vm, frankenstein-db, production-vms):

1. **Go to repository Settings → Branches**
2. **Click "Add rule"**
3. **Configure these settings:**

#### Branch Protection Rules:
```
Branch name pattern: main, master

✅ Require a pull request before merging
  - Required approvals: 1
  - Dismiss stale pull request approvals when new commits are pushed
  - Require review from Code Owners (optional)
  - Restrict who can dismiss pull request reviews: Repository administrators

✅ Require status checks to pass before merging
  - Require branches to be up to date before merging
  - Status checks found in the last week for this repository:
    - (Add your CI/CD checks here)

✅ Require conversation resolution before merging
✅ Include administrators
✅ Restrict pushes that create matching branches
✅ Allow force pushes: Only by maintainers
✅ Allow deletions: Only by maintainers
```

## 🔧 Additional Repository Settings

### General Settings:
- ✅ **Restrict editing to maintainers** (for issues and PRs)
- ✅ **Allow auto-merge**
- ✅ **Automatically delete head branches** after PR merge

### Security & Analysis:
- ✅ **Enable Dependabot security updates**
- ✅ **Enable Dependabot version updates**
- ✅ **Run code scanning with CodeQL**
- ✅ **Enable secret scanning**

### Moderation:
- ✅ **Block force pushes** (except by maintainers)
- ✅ **Require linear history**
- ✅ **Include administrators** in restrictions

## 🤝 Community Standards

### Enable These Features:
- ✅ **Issues** - Allow bug reports and feature requests
- ✅ **Discussions** - Enable for questions and community chat
- ✅ **Wiki** - Allow community documentation
- ✅ **Projects** - Enable project boards for organization

### Templates:
The following templates are already set up:
- 🐛 Bug report template
- 💡 Feature request template
- 📝 Pull request template

## 🚨 Emergency Contacts

### Security Issues:
- Email: brian@useragent.id
- Response time: Within 48 hours

### General Support:
- Issues: Use GitHub Issues
- Discussions: Use GitHub Discussions
- Documentation: Check repository READMEs

## 📊 Monitoring

### Recommended Alerts:
- Security vulnerabilities
- Dependabot updates
- Failed CI/CD pipelines
- New contributor PRs

### Regular Maintenance:
- Review open issues weekly
- Update dependencies monthly
- Audit repository settings quarterly

## 🎯 Implementation Checklist

- [ ] Set up branch protection rules for all repos
- [ ] Enable security features (Dependabot, CodeQL)
- [ ] Configure repository settings
- [ ] Test contribution workflow
- [ ] Review and update documentation

---

*These settings help maintain code quality while welcoming contributions.*