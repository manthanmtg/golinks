# golinks

A local implementation of go-links for quick navigation and URL management.

## Features

- Create and manage custom URL shortcuts (e.g., `go/google` → google.com)
- Support for search parameters (e.g., `go/google "search term"`)
- Modern web interface for managing links (accessible via `go/go`)
- Usage analytics tracking
- Cross-platform support (Windows, Linux, Mac)
- SQLite database by default (pluggable database architecture)

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

The server will start on `http://localhost:8080`

## Usage

1. Access the web interface by navigating to `go/go` or `http://localhost:8080/go/go`
2. Add new links through the web interface
3. Use your links:
   - Basic: `go/shortlink`
   - With search: `go/shortlink "search term"`

## System Configuration

To make `go/` URLs work system-wide, you need to configure your system's DNS:

### For Mac/Linux:
1. Edit `/etc/hosts`:
```
127.0.0.1 go
```

### For Windows:
1. Edit `C:\Windows\System32\drivers\etc\hosts`:
```
127.0.0.1 go
```

## Development

The application uses:
- Flask for the web server
- SQLAlchemy for database operations (SQLite database stored in `~/.golinks.db`)
- TailwindCSS for the UI
- Modern JavaScript for frontend interactivity