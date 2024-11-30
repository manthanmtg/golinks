# golinks

A local implementation of go-links for quick navigation and URL management, similar to Google's internal go links system. Type `go/shortlink` in your browser to quickly access your favorite websites!

## Features

- Create and manage custom URL shortcuts (e.g., `go/google` → google.com)
- Support for search parameters (e.g., `go/google "search term"`)
- Modern web interface for managing links (accessible via `go/go`)
- Usage analytics tracking
- Cross-platform support (Windows, Linux, Mac)
- SQLite database by default (pluggable database architecture)
- All data stored in `~/.golinks/` directory

## Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package installer)
- Administrative access (for DNS configuration)
- For Windows: [NSSM](https://nssm.cc/) (the Non-Sucking Service Manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/golinks-local.git
cd golinks-local
```

2. Create a virtual environment and install dependencies:
```bash
# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

3. Run the installation script for your platform:

macOS:
```bash
python3 macos_install.py
```

Linux:
```bash
sudo python3 linux_install.py
```

Windows (run PowerShell as Administrator):
```powershell
python windows_install.py
```

The installation script will:
- Configure DNS to resolve `go` to localhost
- Set up the service to run on startup
- Start the service

## Using golinks

### First Time Setup

1. Open your browser and go to `go/go` or `http://localhost:8080/go/go`
2. You'll see the main dashboard where you can manage your links
3. Click "Add Link" to create your first shortlink

### Adding Links

1. Click "Add Link" in the dashboard
2. Enter a shortlink (e.g., `google`)
3. Enter the destination URL (e.g., `https://www.google.com`)
4. Click "Add Link"

### Using Your Links

#### Basic Navigation
Just type `go/shortlink` in your browser:
- `go/google` → redirects to Google
- `go/github` → redirects to GitHub
- `go/docs` → redirects to your documentation

#### Search Shortcuts
Add search terms in quotes:
- `go/google "cascade ai"` → searches Google for "cascade ai"
- `go/youtube "cute cats"` → searches YouTube for "cute cats"

#### Advanced Usage
Use the {query} placeholder in your destination URLs:
1. Set up GitHub search:
   - Shortlink: `gh`
   - URL: `https://github.com/search?q={query}`
   - Usage: `go/gh "python flask"` searches GitHub

2. Set up JIRA tickets:
   - Shortlink: `jira`
   - URL: `https://your-company.atlassian.net/browse/{query}`
   - Usage: `go/jira "PROJ-123"` opens ticket

### Managing Links

1. View all links at `go/go`
2. Click on a link to:
   - View usage statistics
   - Edit the destination URL
   - Delete the link
3. Use the search bar to find specific links
4. Sort links by usage, creation date, or name

## Backup and Data

All data is stored in `~/.golinks/`:
- `golinks.db`: Your links database
- `golinks.log`: Application logs

To backup your links, copy the `~/.golinks` directory.

## Troubleshooting

### Can't access go/links
1. Verify DNS configuration:
   ```bash
   # On macOS/Linux:
   cat /etc/hosts  # Should show: 127.0.0.1 go

   # On Windows:
   type C:\Windows\System32\drivers\etc\hosts
   ```

2. Flush DNS cache:
   ```bash
   # macOS
   sudo killall -HUP mDNSResponder

   # Windows
   ipconfig /flushdns

   # Linux
   sudo systemd-resolve --flush-caches
   ```

### Service Issues
1. Check service status:
   ```bash
   # macOS
   launchctl list | grep golinks

   # Windows
   sc query GoLinks

   # Linux
   systemctl status golinks
   ```

2. View logs:
   ```bash
   tail -f ~/.golinks/golinks.log
   ```

### Database Issues
1. Check permissions:
   ```bash
   ls -la ~/.golinks/
   ```

2. Reset database (will delete all links):
   ```bash
   rm ~/.golinks/golinks.db
   flask db upgrade
   ```

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.