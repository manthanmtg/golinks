# Contributing to golinks-local

Thank you for your interest in contributing to golinks-local! This document provides guidelines and information for contributors.

## Development Setup

1. Install Python dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
export SECRET_KEY='your-secure-secret-key'
export SENTRY_DSN='your-sentry-dsn'  # Optional
export LOG_LEVEL='INFO'
```

3. Run the development server:
```bash
FLASK_DEBUG=1 python app.py
```

## Project Architecture

The application uses:
- Flask for the web server
- SQLAlchemy for database operations
- TailwindCSS for the UI
- Modern JavaScript for frontend interactivity

### Project Structure
```
golinks-local/
├── app.py              # Main application file
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── migrations/         # Database migrations
├── templates/          # HTML templates
│   ├── index.html     # Main UI template
│   └── error.html     # Error page template
└── golinks.service    # Systemd service file


~/.golinks/            # User data directory
├── golinks.db         # SQLite database
└── golinks.log        # Application logs
```

## Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use Black for code formatting
- Use type hints where possible
- Keep functions small and focused
- Write descriptive variable and function names

### Testing
1. Run tests:
```bash
pytest
```

2. Run linting:
```bash
flake8
black --check .
mypy .
```

### Logging
- Application logs are stored in `~/.golinks/golinks.log`
- Logs are rotated automatically (10MB per file, keeping last 10 files)
- Use appropriate log levels:
  * DEBUG for detailed debugging information
  * INFO for general information
  * WARNING for concerning but non-critical issues
  * ERROR for errors that need attention
  * CRITICAL for critical failures

### Security Best Practices
- CSRF protection enabled
- Secure session cookies
- Input validation and sanitization
- Rate limiting on API endpoints
- Never commit sensitive information (API keys, credentials)
- Always validate user input
- Use parameterized queries for database operations

### Error Tracking
- Sentry integration for production error tracking (optional)
- Set `SENTRY_DSN` environment variable to enable
- Include relevant context in error reports

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Update documentation if needed
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to your fork (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Pull Request Guidelines
- Keep changes focused and atomic
- Include tests for new functionality
- Update documentation as needed
- Reference any related issues
- Provide a clear description of changes
- Include screenshots for UI changes

## Release Process

1. Update version number in relevant files
2. Update CHANGELOG.md
3. Create a new release on GitHub
4. Tag the release with version number
5. Update documentation if needed

## Questions or Problems?

- Open an issue for bugs
- Use discussions for feature requests or questions
- Tag issues appropriately
- Provide clear reproduction steps for bugs

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.
