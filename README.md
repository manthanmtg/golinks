# golinks-local

A powerful and user-friendly local implementation of go-links for quick navigation and URL management, inspired by Google's internal go links system. Simply type `go/shortlink` in your browser to instantly access your favorite websites!

## Key Features

- **Quick Navigation**: Create and use custom URL shortcuts (e.g., `go/google` → google.com)
- **Smart Search**: Support for dynamic search parameters (e.g., `go/google "search term"`)
- **Modern Interface**: Clean web dashboard for link management (accessible via `go/go`)
- **Analytics**: Track usage patterns and popular links
- **Cross-Platform**: Full support for Windows, Linux, and macOS
- **Local Storage**: SQLite database with all data stored securely in `~/.golinks/`
- **Customizable**: Pluggable database architecture for flexibility
- **Privacy-Focused**: All data stays on your machine

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package installer)
- Administrative privileges (for DNS setup)
- For Windows users: [NSSM](https://nssm.cc/) (Non-Sucking Service Manager)

### Installation Steps

1. **Get the Code**
   ```bash
   git clone https://github.com/yourusername/golinks-local.git
   cd golinks-local
   ```

2. **Set Up Environment**
   ```bash
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Install required packages
   pip install -r requirements.txt
   ```

3. **Start the Service**

   Use the convenient `golinks.py` utility to manage the service:
   ```bash
   # Start the service
   python golinks.py --start

   # Stop the service (when needed)
   python golinks.py --stop
   ```

   The utility automatically detects your platform (Windows/macOS/Linux) and runs the appropriate scripts.

   Alternatively, you can run platform-specific scripts directly:
   ```bash
   # macOS
   python3 scripts/macos_golinks_start.py

   # Linux
   sudo python3 scripts/linux_golinks_start.py

   # Windows (Run PowerShell as Admin)
   python scripts/windows_golinks_start.py
   ```

### Service Management

You can manage the golinks service using the following commands:

```bash
# View help
python golinks.py --help

# Start the service
python golinks.py --start

# Stop the service
python golinks.py --stop
```

The service manager will:
- Automatically detect your operating system
- Run the appropriate platform-specific scripts
- Handle service installation and configuration
- Manage DNS settings
- Start/stop the service as needed

## Using golinks

### Initial Setup

1. Open your browser
2. Navigate to `go/go` or `http://localhost:8080/go/go`
3. You'll see the management dashboard
4. Start by adding your first link!

### Link Management

#### Creating Links
- Basic: `go/github` → `https://github.com`
- With Search: `go/google "{query}"` → Searches Google
- With Parameters: `go/jira "{ticket}"` → Opens JIRA tickets

#### Using Links
- Direct Navigation: Type `go/shortlink` in your browser
- With Search: `go/google "golinks tutorial"`
- With Parameters: `go/jira "PROJ-123"`

#### Advanced Features
- **Analytics**: Track usage patterns
- **Bulk Operations**: Import/export links
- **Categories**: Organize links by teams/projects
- **Access Control**: Restrict link management

## Configuration

### Data Location
All data is stored in `~/.golinks/`:
```
~/.golinks/
├── golinks.db    # SQLite database
└── golinks.log   # Application logs
```

### Environment Variables
- `SECRET_KEY`: Application secret (auto-generated if not set)
- `LOG_LEVEL`: Logging detail (default: INFO)
- `PORT`: Server port (default: 8080)

## Troubleshooting Guide

### Common Issues

1. **DNS Resolution Failed**
   ```bash
   # Verify DNS configuration
   cat /etc/hosts  # Should show: 127.0.0.1 go
   
   # Flush DNS cache
   # macOS
   sudo killall -HUP mDNSResponder
   # Windows
   ipconfig /flushdns
   # Linux
   sudo systemd-resolve --flush-caches
   ```

2. **Service Not Running**
   ```bash
   # Check service status
   # macOS
   launchctl list | grep golinks
   # Windows
   sc query GoLinks
   # Linux
   systemctl status golinks
   ```

3. **Database Issues**
   - Check permissions: `ls -la ~/.golinks/`
   - View logs: `tail -f ~/.golinks/golinks.log`
   - Reset database: `rm ~/.golinks/golinks.db && flask db upgrade`

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup
- Code style guidelines
- Testing procedures
- Pull request process

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Inspired by Google's internal go links system
- Built with Flask, SQLAlchemy, and modern web technologies
- Thanks to all contributors!