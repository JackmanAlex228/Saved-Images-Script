# Image Organizer

Download and organize images from social media feeds. Currently supports BlueSky via the AT Protocol API, with plans to expand to other services.

## Architecture

- **TypeScript**: Downloads images from AT Protocol
- **Rust**: Orchestrates downloads and organizes files (duplicate detection, interactive mode, etc.)

## Setup

### Prerequisites
- Node.js and npm
- Rust and Cargo
- A BlueSky account

### Installation

1. Install dependencies:
```bash
npm install
cargo build
```

2. Create a `config.yaml` file:
```yaml
handle: your-handle.bsky.social
password: your-app-password
download_path: /path/to/download/folder
limit: 2000
```

> **Note**: Use an app password, not your main BlueSky password. Generate one at: Settings → App Passwords

## Usage

### Download images only
```bash
cargo run -- download
```

Downloads images from your BlueSky feed to the path specified in `config.yaml`.

**With custom path:**
```bash
cargo run -- download --path "/custom/path"
```

### Organize existing images
```bash
cargo run -- organize
```

Organizes images in the directory specified in `config.yaml`.

**Interactive mode:**
```bash
cargo run -- organize --interactive
```

**Find duplicates:**
```bash
cargo run -- organize --find-duplicates
```

**Custom directory:**
```bash
cargo run -- organize --directory "/custom/path"
```

### Download AND organize (one command)
```bash
cargo run -- run
```

Downloads images and then organizes them.

**With options:**
```bash
cargo run -- run --interactive
cargo run -- run --find-duplicates
```

### Help
```bash
cargo run -- --help
cargo run -- download --help
cargo run -- organize --help
cargo run -- run --help
```

## Install Globally (Optional)

Install as a system-wide command:
```bash
cargo install --path .
```

Then run from anywhere:
```bash
image_organizer download
image_organizer organize --interactive
image_organizer run
```

## Project Structure

```
.
├── src/
│   └── main.rs          # Rust CLI orchestrator
├── main.ts              # TypeScript AT Protocol downloader
├── config.yaml          # Configuration file
├── Cargo.toml           # Rust dependencies
├── package.json         # Node dependencies
└── tsconfig.json        # TypeScript config
```

## Roadmap

- [ ] Complete AT Protocol image download implementation
- [ ] Interactive TUI for manual file organization
- [ ] Perceptual hash-based duplicate detection
- [ ] Automatic file organization by date/type
- [ ] Support for additional social media platforms
- [ ] EXIF data extraction and organization

## License

MIT
