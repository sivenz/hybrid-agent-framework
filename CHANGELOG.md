# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-10-15

### Added
- Initial release of Hybrid Agent Framework
- Core `HybridPlatform` orchestrator combining OpenAI and Claude agents
- Intelligent task routing based on requirements
- Guardrail system for safety and compliance
- Task lifecycle management with status tracking
- Four production-ready examples:
  - DevOps incident response
  - Code review and deployment pipeline
  - Financial audit automation
  - Research pipeline automation
- Comprehensive documentation:
  - Getting started guide
  - Architecture deep dive
  - Best practices guide
- Test suite with pytest
- GitHub Actions CI/CD
- MIT License

### Features
- **Intelligent Routing**: Automatically selects optimal platform (OpenAI, Claude, or hybrid)
- **Hybrid Workflows**: Multi-stage execution combining both platforms
- **Guardrails**: Safety mechanisms including validation, blocking, and approval workflows
- **Observability**: Task history tracking and tracing support
- **Type Safety**: Full type hints for IDE support
- **Async Support**: Asynchronous task execution
- **Extensible**: Easy to add custom agents and platforms

### Documentation
- README with quick start and feature overview
- Getting Started guide for new users
- Architecture documentation for developers
- Best Practices for production deployment
- Contributing guidelines
- Security policy

### Examples
- DevOps incident response (MTTR reduction: 45 min → 5 min)
- Automated code review and deployment (2 hours → 20 minutes)
- Financial audit automation (6 months → 6 weeks)
- Research pipeline (10x faster research cycles)

[Unreleased]: https://github.com/cogniolab/hybrid-agent-framework/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/cogniolab/hybrid-agent-framework/releases/tag/v0.1.0
