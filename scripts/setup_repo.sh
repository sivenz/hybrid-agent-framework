#!/bin/bash
# Setup script for Hybrid Agent Framework repository

set -e

echo "🚀 Setting up Hybrid Agent Framework repository..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if git is initialized
if [ ! -d .git ]; then
    echo -e "${BLUE}Initializing git repository...${NC}"
    git init
    echo -e "${GREEN}✓ Git repository initialized${NC}"
fi

# Create .gitignore if it doesn't exist
if [ ! -f .gitignore ]; then
    echo -e "${YELLOW}Warning: .gitignore not found${NC}"
fi

# Add all files
echo -e "${BLUE}Adding files to git...${NC}"
git add .

# Create initial commit
echo -e "${BLUE}Creating initial commit...${NC}"
git commit -m "Initial commit: Hybrid Agent Framework - OpenAI + Claude Power Duo

- Core framework with intelligent routing
- 4 production-ready examples (DevOps, Code Review, Financial Audit, Research)
- Comprehensive documentation (Getting Started, Architecture, Best Practices)
- Test suite with pytest
- GitHub Actions CI/CD
- Professional repository structure
- MIT License

Features:
✅ Intelligent task routing (OpenAI, Claude, or hybrid)
✅ Multi-agent orchestration
✅ Guardrails and safety mechanisms
✅ Task lifecycle management
✅ Full type hints and async support
✅ Extensible architecture"

echo -e "${GREEN}✓ Initial commit created${NC}"

# Set main branch
echo -e "${BLUE}Setting main branch...${NC}"
git branch -M main

echo ""
echo -e "${GREEN}✓ Repository setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Create repository on GitHub: https://github.com/new"
echo "   Repository name: hybrid-agent-framework (or your choice)"
echo "   Description: Combine OpenAI's orchestration with Claude's system execution for production-ready AI agents"
echo ""
echo "2. Add remote and push:"
echo "   git remote add origin https://github.com/cogniolab/hybrid-agent-framework.git"
echo "   git push -u origin main"
echo ""
echo "3. (Optional) Set up GitHub repository settings:"
echo "   - Enable Issues"
echo "   - Add topics: ai, agents, openai, claude, automation, llm"
echo "   - Set up branch protection for main"
echo ""
