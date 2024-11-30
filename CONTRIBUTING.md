# Contributing to golinks-local 🚀

First off, thank you for considering contributing to golinks-local! Every contribution helps make this project better for everyone. This document provides guidelines and steps for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Documentation](#documentation)
- [Community](#community)

## 📜 Code of Conduct

This project follows a Code of Conduct that all contributors are expected to adhere to. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

Key points:
- Be respectful and inclusive
- Focus on constructive feedback
- Maintain professional communication
- Report unacceptable behavior

## 🛠 Development Setup

### Prerequisites
- Python 3.10+
- Git
- Your favorite code editor (VS Code recommended)
- Platform-specific tools:
  * Windows: PowerShell, NSSM
  * Linux: systemd
  * macOS: launchctl

### Environment Setup

1. **Fork & Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/golinks-local.git
   cd golinks-local
   ```

2. **Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: .\venv\Scripts\activate
   ```

3. **Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Environment Variables**
   ```bash
   export FLASK_ENV=development
   export FLASK_DEBUG=1
   export SECRET_KEY='your-dev-secret-key'
   ```

## 🏗 Project Structure

```
golinks-local/
├── app.py              # Main application entry
├── config.py           # Configuration management
├── golinks.py          # Cross-platform service manager
├── migrations/         # Database migrations
├── scripts/           # Platform-specific scripts
│   ├── windows_*.py   # Windows service scripts
│   ├── macos_*.py     # macOS service scripts
│   └── linux_*.py     # Linux service scripts
├── templates/          # HTML templates
├── static/            # Static assets
└── tests/             # Test suite
```

### Key Components

#### Service Manager (golinks.py)
The `golinks.py` utility provides a unified interface for managing the golinks service across different platforms:

- **Platform Detection**: Automatically detects the operating system
- **Script Loading**: Dynamically imports platform-specific scripts
- **Command Line Interface**: Provides --start and --stop options
- **Error Handling**: Graceful handling of platform-specific issues

Example usage in development:
```python
# Import the service manager
from golinks import get_platform, import_script

# Get current platform
platform = get_platform()  # Returns 'windows', 'macos', or 'linux'

# Import platform-specific script
start_script = import_script('start')
stop_script = import_script('stop')

# Execute platform-specific functionality
start_script.main()
```

#### Platform-Specific Scripts
Located in the `scripts/` directory, these implement the actual service management:
- **Start Scripts**: Handle service installation and startup
- **Stop Scripts**: Handle service shutdown and cleanup
- Must implement a `main()` function
- Should handle platform-specific paths and commands

## 🔄 Development Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Development Server**
   ```bash
   python app.py  # Access at http://localhost:8080
   ```

3. **Auto-formatting**
   ```bash
   # Format code
   black .
   
   # Sort imports
   isort .
   ```

4. **Type Checking**
   ```bash
   mypy .
   ```

### Working with Platform-Specific Code

When developing platform-specific features:

1. **Testing Different Platforms**
   ```bash
   # Test on current platform
   python golinks.py --start

   # Test specific platform script directly
   python scripts/macos_golinks_start.py
   ```

2. **Adding New Platform Support**
   - Create new scripts in `scripts/` directory
   - Follow naming convention: `{platform}_golinks_{action}.py`
   - Implement required `main()` function
   - Add platform detection in `golinks.py` if needed

3. **Debugging Platform Issues**
   - Use `--debug` flag for verbose logging
   - Check platform-specific logs
   - Test with different Python versions

## ✅ Testing Guidelines

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_links.py

# Run with coverage
pytest --cov=. tests/
```

### Writing Tests
- Test file naming: `test_*.py`
- Class naming: `Test*`
- Function naming: `test_*`
- Use fixtures for common setup
- Include docstrings explaining test purpose

Example:
```python
def test_create_link():
    """Test creation of a new go link."""
    link = GoLink(short="test", url="https://example.com")
    assert link.short == "test"
```

## 🔍 Pull Request Process

1. **Before Submitting**
   - Update documentation
   - Add/update tests
   - Run full test suite
   - Update CHANGELOG.md
   - Rebase on main

2. **PR Guidelines**
   - Clear, descriptive title
   - Reference related issues
   - Include before/after screenshots for UI changes
   - List breaking changes
   - Update README if needed

3. **Review Process**
   - Two approvals required
   - All checks must pass
   - No merge conflicts
   - Clean commit history

## 📝 Style Guidelines

### Python Code Style
- Follow PEP 8
- Use type hints
- Maximum line length: 88 characters (Black default)
- Docstrings: Google style
- Clear variable/function names

### Commit Messages
- Format: `type(scope): description`
- Types: feat, fix, docs, style, refactor, test, chore
- Keep under 72 characters
- Use present tense

Example:
```
feat(links): add support for custom search parameters

- Add query parameter support
- Update documentation
- Add tests
```

## 📚 Documentation

- Update README.md for user-facing changes
- Update docstrings for API changes
- Include code examples
- Keep configuration examples up-to-date
- Document breaking changes

## 👥 Community

- GitHub Discussions for feature requests
- Issues for bug reports
- Pull Requests for contributions
- Stack Overflow for questions

## 🎉 Recognition

Contributors will be:
- Added to CONTRIBUTORS.md
- Mentioned in release notes
- Thanked in our documentation

Thank you for contributing to golinks-local! 🙌
