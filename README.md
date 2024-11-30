# golinks

A local implementation of go-links for quick navigation and URL management, similar to Google's internal go links system.

## Features

- Create and manage custom URL shortcuts (e.g., `go/google` → google.com)
- Support for search parameters (e.g., `go/google "search term"`)
- Modern web interface for managing links (accessible via `go/go`)
- Usage analytics tracking
- Cross-platform support (Windows, Linux, Mac)
- SQLite database by default (pluggable database architecture)
- All data stored in `~/.golinks/` directory

## Usage Guide

### Basic Usage

1. Access the web interface:
   - Open your browser and go to `go/go` or `http://localhost:8080/go/go`
   - You'll see the main dashboard where you can manage your links

2. Adding a new link:
   - Click the "Add Link" button
   - Enter a shortlink (e.g., `google`)
   - Enter the destination URL (e.g., `https://www.google.com`)
   - Click "Add Link"

3. Using your links:
   - Basic navigation: Type `go/shortlink` in your browser
     Example: `go/google` → redirects to Google
   
   - With search terms: Type `go/shortlink "search term"`
     Example: `go/google "cascade ai"` → searches Google for "cascade ai"
   
   - With custom parameters: Use the {query} placeholder in your destination URL
     Example: Set up `go/gh` to point to `https://github.com/search?q={query}`
     Then `go/gh "python flask"` will search GitHub for "python flask"

### Advanced Features

1. Analytics:
   - Click the "Analytics" tab to view:
     * Most used links
     * Usage patterns
     * Last accessed times
     * Search term statistics

2. Link Management:
   - Delete links you no longer need
   - View creation dates and usage statistics
   - Sort and filter your links

### URL Pattern Examples

1. Simple redirect:
   - Shortlink: `docs`
   - Destination: `https://docs.google.com`
   - Usage: `go/docs`

2. Search engine:
   - Shortlink: `g`
   - Destination: `https://www.google.com/search?q={query}`
   - Usage: `go/g "your search term"`

3. GitHub repository:
   - Shortlink: `repo`
   - Destination: `https://github.com/yourusername/{query}`
   - Usage: `go/repo "project-name"`

4. JIRA tickets:
   - Shortlink: `jira`
   - Destination: `https://your-company.atlassian.net/browse/{query}`
   - Usage: `go/jira "PROJ-123"`

## Data Storage

All application data is stored in your home directory:
- Database: `~/.golinks/golinks.db`
- Log files: `~/.golinks/golinks.log`

To backup your links, simply copy the `~/.golinks` directory.

## Running as a Service

### On Linux (systemd)

1. Copy the service file:
```bash
sudo cp golinks.service /etc/systemd/system/
```

2. Start and enable the service:
```bash
sudo systemctl start golinks
sudo systemctl enable golinks
```

### On macOS (launchd)

1. Create a launch agent:
```bash
mkdir -p ~/Library/LaunchAgents
cp com.user.golinks.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.user.golinks.plist
```

### On Windows

1. Create a Windows service:
```powershell
nssm install GoLinks "path\to\python.exe" "path\to\app.py"
nssm start GoLinks
```

## Troubleshooting

1. DNS Issues:
   - Verify your hosts file contains `127.0.0.1 go`
   - Try accessing via `localhost:8080/go/shortlink`
   - Flush DNS cache if needed

2. Server Issues:
   - Check logs in `~/.golinks/golinks.log`
   - Ensure port 8080 is not in use
   - Verify Python environment is activated

3. Database Issues:
   - Run `flask db upgrade` to ensure schema is up to date
   - Check permissions on `~/.golinks` directory

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.