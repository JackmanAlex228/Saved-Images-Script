use clap::{Parser, Subcommand};
use serde::{Deserialize, Serialize};
use std::path::PathBuf;
use std::process::Command;
use anyhow::{Context, Result};

#[derive(Parser, Debug)]
#[command(name = "image_organizer")]
#[command(about = "Download and organize images from social media", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand, Debug)]
enum Commands {
    /// Download images from AT Protocol
    Download {
        /// Custom download path (overrides config)
        #[arg(short, long)]
        path: Option<PathBuf>,
    },
    /// Organize files in a directory
    Organize {
        /// Directory containing images to organize
        #[arg(short, long)]
        directory: Option<PathBuf>,

        /// Enable interactive mode
        #[arg(short, long)]
        interactive: bool,

        /// Run duplicate detection
        #[arg(long)]
        find_duplicates: bool,
    },
    /// Download and then organize images
    Run {
        /// Enable interactive mode for organization
        #[arg(short, long)]
        interactive: bool,

        /// Run duplicate detection
        #[arg(long)]
        find_duplicates: bool,
    },
}

#[derive(Debug, Deserialize, Serialize)]
struct Config {
    handle: String,
    password: String,
    download_path: String,
    limit: u32,
}

fn main() -> Result<()> {
    let cli = Cli::parse();

    match cli.command {
        Commands::Download { path } => {
            let config = read_config()?;
            let download_path = path.unwrap_or_else(|| PathBuf::from(&config.download_path));
            run_downloader(&download_path)?;
        }
        Commands::Organize {
            directory,
            interactive,
            find_duplicates,
        } => {
            let config = read_config()?;
            let dir = directory.unwrap_or_else(|| PathBuf::from(&config.download_path));

            if !dir.exists() {
                eprintln!("Error: Directory {:?} does not exist", dir);
                std::process::exit(1);
            }

            if interactive {
                run_interactive_mode(&dir)?;
            } else if find_duplicates {
                find_duplicates_fn(&dir)?;
            } else {
                organize_files(&dir)?;
            }
        }
        Commands::Run {
            interactive,
            find_duplicates,
        } => {
            let config = read_config()?;
            let download_path = PathBuf::from(&config.download_path);

            println!("Step 1: Downloading images...");
            run_downloader(&download_path)?;

            println!("\nStep 2: Organizing images...");
            if interactive {
                run_interactive_mode(&download_path)?;
            } else if find_duplicates {
                find_duplicates_fn(&download_path)?;
            } else {
                organize_files(&download_path)?;
            }
        }
    }

    Ok(())
}

fn read_config() -> Result<Config> {
    let config_path = "config.yaml";
    let contents = std::fs::read_to_string(config_path)
        .context("Failed to read config.yaml")?;
    let config: Config = serde_yaml::from_str(&contents)
        .context("Failed to parse config.yaml")?;
    Ok(config)
}

fn run_downloader(download_path: &PathBuf) -> Result<()> {
    println!("Downloading to: {:?}", download_path);

    // First, build the TypeScript
    let build_status = Command::new("npm")
        .arg("run")
        .arg("build")
        .status()
        .context("Failed to build TypeScript")?;

    if !build_status.success() {
        anyhow::bail!("TypeScript build failed");
    }

    // Run the downloader
    let status = Command::new("node")
        .arg("dist/main.js")
        .status()
        .context("Failed to run downloader")?;

    if !status.success() {
        anyhow::bail!("Downloader failed");
    }

    println!("Download complete!");
    Ok(())
}

fn run_interactive_mode(dir: &PathBuf) -> Result<()> {
    println!("\nRunning interactive mode in {:?}...", dir);
    println!("TODO: Implement interactive TUI for manual file organization");
    // TODO: Implement interactive TUI using ratatui
    Ok(())
}

fn find_duplicates_fn(dir: &PathBuf) -> Result<()> {
    println!("\nSearching for duplicates in {:?}...", dir);
    println!("TODO: Implement perceptual hashing and duplicate detection");
    // TODO: Implement duplicate detection using img_hash crate
    Ok(())
}

fn organize_files(dir: &PathBuf) -> Result<()> {
    println!("\nOrganizing files in {:?}...", dir);
    println!("TODO: Implement automatic file organization");
    // TODO: Implement file organization logic
    Ok(())
}
