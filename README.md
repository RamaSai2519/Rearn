# Instagram Brainrot Bot

A fully autonomous Linux-compatible bot that finds trending "brainrot" content on Instagram, downloads it, and reposts it automatically.

## Features

- **Autonomous Operation**: Fully automated content discovery and posting
- **Credential Management**: Automatically creates Instagram credentials if missing
- **Content Discovery**: Finds trending brainrot content using hashtags and engagement metrics
- **Duplicate Prevention**: Uses MongoDB to track posted content and avoid duplicates
- **Smart Posting**: Posts at least 5 unique reels per run with auto-generated captions
- **Rate Limiting**: Built-in delays to avoid Instagram's rate limits

## Architecture

The bot is built using Object-Oriented Programming (OOP) principles with the following modules:

### Core Classes

1. **InstagramBrainrotBot** (`bot.py`)
   - Main orchestrator class
   - Coordinates all bot operations
   - Manages workflow from discovery to posting

2. **MongoDBHandler** (`database.py`)
   - Handles all MongoDB operations
   - Tracks posted content to prevent duplicates
   - Provides query methods for posted content

3. **CredentialManager** (`credentials.py`)
   - Manages Instagram credentials
   - Auto-generates credentials if missing
   - Handles session persistence

4. **ContentDiscovery** (`content_discovery.py`)
   - Discovers trending brainrot content
   - Searches by hashtags
   - Ranks content by engagement

5. **ContentDownloader** (`downloader.py`)
   - Downloads videos from Instagram
   - Manages local file storage
   - Handles cleanup of old files

6. **ContentPoster** (`poster.py`)
   - Posts content to Instagram
   - Generates engaging captions
   - Handles reel/video uploads

## Requirements

- Python 3.8+
- MongoDB Atlas account (connection string provided)
- Linux-compatible system

## Installation

1. Clone the repository:
```bash
git clone https://github.com/RamaSai2519/Rearn.git
cd Rearn
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the bot:
```bash
python bot.py
```

The bot will:
1. Check for existing Instagram credentials
2. Create new credentials if none exist (including email)
3. Connect to MongoDB
4. Search for trending brainrot content
5. Download and post at least 5 unique items
6. Track all posted content to avoid duplicates

## Configuration

### MongoDB Connection
The bot uses the following MongoDB connection string (embedded in code):
```
mongodb+srv://rama:7MR9oLpef122UCdy@cluster0.fquqway.mongodb.net/?retryWrites=true&w=majority&appName=Cluster
```

### Brainrot Content Discovery
The bot searches for content using these hashtags:
- #brainrot
- #skibiditoilet
- #gyatt, #rizz, #sigma
- #ohio, #griddy, #fanum
- #mewing, #mogger, #looksmaxxing
- #ishowspeed, #kaicentat
- And more trending terms

## Project Structure

```
Rearn/
├── bot.py                  # Main bot orchestrator
├── database.py             # MongoDB handler
├── credentials.py          # Credential manager
├── content_discovery.py    # Content discovery module
├── downloader.py          # Content downloader
├── poster.py              # Content poster
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Output Files

- `credentials.json` - Stored Instagram credentials (gitignored)
- `instagram_session.json` - Instagram session data (gitignored)
- `bot.log` - Bot execution logs
- `downloads/` - Downloaded content directory (gitignored)

## How It Works

1. **Startup**: Bot initializes and connects to MongoDB
2. **Credentials**: Checks for credentials, creates if missing
3. **Login**: Authenticates with Instagram
4. **Discovery**: Searches for trending brainrot content
5. **Filtering**: Removes already-posted content using MongoDB
6. **Download**: Downloads selected videos
7. **Post**: Uploads to Instagram with auto-generated captions
8. **Track**: Marks content as posted in MongoDB
9. **Repeat**: Posts 5+ items per run

## Rate Limiting

The bot includes built-in delays:
- 2 seconds after downloads
- 30 seconds between posts
- Respects Instagram's rate limits

## Error Handling

- Graceful handling of login failures
- Automatic retry on download failures
- Skips problematic content items
- Comprehensive logging for debugging

## Security

- Credentials stored locally (not in git)
- Session data excluded from repository
- MongoDB connection uses secure URI
- No hardcoded secrets in code

## License

This project is for educational purposes only. Ensure you comply with Instagram's Terms of Service when using this bot.