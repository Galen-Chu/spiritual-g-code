# Security Policy

## Supported Versions

Currently, only the latest version of Spiritual G-Code is supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |

## Reporting a Vulnerability

The Spiritual G-Code team takes security vulnerabilities seriously. We appreciate your efforts to responsibly disclose your findings.

If you discover a security vulnerability, please **DO NOT** open a public issue.

### How to Report

**Send an email to**: galen.chu@example.com

Please include:
* A description of the vulnerability
* Steps to reproduce the issue
* Potential impact of the vulnerability
* Any suggested mitigation (if known)

### What to Expect

* **Response Time**: We will acknowledge your report within 48 hours
* **Investigation**: We will investigate the vulnerability and determine the severity
* **Resolution**: We will work on a fix and provide an estimated timeline
* **Disclosure**: We will coordinate disclosure with you to ensure users are protected

### Safe Harbor

We commit to:
* Respond to your report within 48 hours
* Work with you to understand and validate the report
* Handle the report in a confidential manner
* Credit you in our security advisory (unless you wish to remain anonymous)

Acting in good faith means you:
* Never exploit the vulnerability in any way
* Provide reasonable time for us to fix the issue before making it public
* Follow the principles of responsible disclosure

## Security Best Practices

### For Users

1. **Keep Dependencies Updated**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Use Environment Variables**
   - Never commit `.env` files
   - Use strong, unique secrets
   - Rotate credentials regularly

3. **Enable HTTPS in Production**
   ```env
   SECURE_SSL_REDIRECT=True
   SESSION_COOKIE_SECURE=True
   CSRF_COOKIE_SECURE=True
   ```

4. **Regular Database Backups**
   - Backup PostgreSQL database regularly
   - Test restore procedures
   - Store backups securely

### For Developers

1. **Dependency Scanning**
   ```bash
   pip install safety
   safety check
   ```

2. **Code Review**
   - All code changes require review
   - Security-sensitive changes require additional scrutiny

3. **Testing**
   - Run security tests in CI/CD
   - Use tools like `bandit` for Python security checks
   ```bash
   pip install bandit
   bandit -r api/ ai_engine/ core/
   ```

## Security Features

### Built-in Protections

* **CSRF Protection**: Django's built-in CSRF middleware
* **SQL Injection**: ORM-based queries prevent SQL injection
* **XSS Protection**: Django templates auto-escape content
* **Authentication**: JWT-based secure authentication
* **Password Security**: PBKDF2 with SHA256 hash

### Environment Configuration

Ensure these security settings are enabled in production:

```env
DEBUG=False
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True
X_FRAME_OPTIONS=DENY
```

## Public Disclosure

When a security vulnerability is fixed:
1. A new version will be released
2. A security advisory will be published on GitHub
3. The CHANGELOG will be updated
4. Credits will be given to the reporter (if desired)

## Security Audits

Periodic security audits may be conducted. Results will be:
* Summarized (no sensitive details)
* Used to improve security posture
* Incorporated into future releases

## Contact Information

For general security questions:
* **Email**: galen.chu@example.com
* **GitHub Security**: Use GitHub's private vulnerability reporting feature

## Resources

* [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
* [OWASP Python Security](https://cheatsheetseries.owasp.org/cheatsheets/Python_Security_Cheat_Sheet.html)
* [Python Bandit](https://bandit.readthedocs.io/)
