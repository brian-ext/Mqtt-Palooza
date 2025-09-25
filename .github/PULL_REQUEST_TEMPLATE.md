## 📝 Description
Brief description of the changes made.
github_username: ["your_github_username"] (github.com/scrapedat)
repos: "["ui_repo"](../ai-scraper-dashboard)
repos: "["orchestrator_repo"](../ai-scraper-vm)
repos: "["database_repo"](../frankenstein-db)
monorepo: ["separated_repos"] (Each component has its own repo)***they are all inside of ["/home/b/teamai/production-vms/"]***

env example : variables & secrets for each repo:
github_separated_repos:
  ui_repo:
    - GITHUB_ENV: ${{ secrets.GITHUB_ENV }} (for pushing to GHCR)  
  orchestrator_repo:
    - GITHUB_ENV: ${{ secrets.GITHUB_ENV }} (for pushing to GHCR)   
  database_repo:    
    - GITHUB_ENV: ${{ secrets.GITHUB_ENV }} (for pushing to GHCR)   
    production_vms_repo:
    - GITHUB_ENV: ${{ secrets.GITHUB_ENV }} (for pushing to GHCR)   

## 🔧 Changes Made
- Change 1
- Change 2
- Change 3

## 🧪 Testing
How have you tested these changes?

## 📋 Checklist
- [ ] Tests pass
- [ ] Documentation updated (if needed)
- [ ] Code follows project standards
- [ ] Commit messages are clear

## 🔗 Related Issues
Closes #123
Related to #456

## 📸 Screenshots (if applicable)
Add screenshots or GIFs, text snippets etc to help explain your changes.

## 🤔 Additional Notes
Any additional information or context?