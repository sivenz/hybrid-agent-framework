# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please send an email to **moses@cogniolab.com**.

**Please do not create a public GitHub issue for security vulnerabilities.**

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if available)

### Response Timeline

- **Acknowledgment**: Within 24 hours
- **Initial assessment**: Within 48 hours
- **Fix timeline**: Depends on severity (critical: 1-3 days, high: 1 week, medium: 2 weeks)

## Security Best Practices

When using this framework:

1. **Never hardcode API keys** - Always use environment variables
2. **Enable guardrails** - Especially for production systems
3. **Review Claude commands** - Understand what system access agents have
4. **Enable audit logging** - Track all agent actions
5. **Use principle of least privilege** - Grant minimal necessary permissions
6. **Set rate limits** - Prevent abuse
7. **Validate inputs** - Sanitize user-provided data

## Known Security Considerations

### System Access (Claude Agents)

Claude agents have the ability to execute bash commands and access the file system. This is powerful but requires careful security considerations:

- **Use guardrails** to block destructive operations
- **Require approval** for sensitive operations
- **Whitelist allowed commands** in production
- **Enable audit logging** for compliance
- **Run in containers** for isolation

### API Keys

This framework requires API keys for OpenAI and Anthropic. Protect these keys:

- Store in environment variables or secure key management systems
- Never commit to version control
- Rotate regularly
- Use separate keys for development/production
- Monitor usage for anomalies

### Rate Limiting

Implement rate limits to prevent:
- Abuse
- Unexpected costs
- Service degradation

See `docs/best-practices.md` for detailed guidance.

## Security Updates

We will publish security advisories through GitHub Security Advisories. Subscribe to repository notifications to stay informed.
