# Security Policy

## Supported versions

TaskFlow is currently a portfolio project under active development. Security fixes are applied to the latest version on the `main` branch.

## Reporting a vulnerability

Please do not disclose suspected vulnerabilities in a public issue.

Use GitHub's private vulnerability reporting feature when it is available for this repository. Include:

- A clear description of the vulnerability
- Steps to reproduce it
- The affected endpoint or component
- The potential impact
- Any suggested remediation

Please allow reasonable time for investigation before publishing details.

## Security expectations

Contributors must never commit:

- Passwords, tokens, API keys, or database credentials
- Production data or personally identifiable information
- Local environment files such as `.env`
- Private keys or generated authentication secrets

Authentication changes must include tests for unauthorized access, invalid credentials, and cross-user data access.
