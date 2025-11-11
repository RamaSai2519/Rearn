# Rearn - Instagram Reels Scraper

An Android app that uses accessibility features to search Instagram for trending reels and send their URLs to a webhook.

## Features

- Search Instagram reels using custom keywords
- Filter reels by minimum views and likes
- Automatically copy reel URLs
- Send reel URLs to a webhook endpoint
- Uses Android Accessibility Service for automation

## Requirements

- Android device with API level 24 (Android 7.0) or higher
- Instagram app installed
- Physical device connected via ADB for testing

## Setup

1. Clone the repository
2. Open the project in Android Studio
3. Connect your physical Android device via USB
4. Enable USB debugging on your device
5. Build and install the app:
   ```bash
   ./gradlew installDebug
   ```

## Usage

1. Launch the Rearn app
2. Click "Enable Accessibility Service" and enable the service in Settings
3. Enter your search parameters:
   - Keywords (comma-separated)
   - Minimum views
   - Minimum likes
   - Webhook URL (where reel URLs will be sent)
4. Click "Start Scraping"
5. The app will:
   - Open Instagram
   - Navigate to search/explore
   - Search for each keyword
   - Navigate to the Reels section
   - Scroll through reels
   - Copy URLs of reels matching your criteria
   - Send URLs to your webhook

## Webhook Format

The app sends POST requests to your webhook URL with the following JSON format:

```json
{
  "reel_url": "https://www.instagram.com/reel/...",
  "timestamp": 1234567890
}
```

## Testing on Physical Device

```bash
# Check connected devices
adb devices

# Install the app
./gradlew installDebug

# View logs
adb logcat -s InstagramAccessibility
```

## Permissions

The app requires the following permissions:
- `INTERNET` - To send data to webhook
- `BIND_ACCESSIBILITY_SERVICE` - To use accessibility features
- `QUERY_ALL_PACKAGES` - To detect Instagram app

## Important Notes

- This app is for educational purposes only
- Instagram's UI may change, requiring updates to the accessibility logic
- Use responsibly and in accordance with Instagram's Terms of Service
- The accessibility service must be manually enabled in device settings
- Some features may not work on all devices due to UI variations

## Architecture

- `MainActivity.kt` - Main UI activity
- `InstagramAccessibilityService.kt` - Accessibility service that automates Instagram
- `WebhookSender.kt` - Handles HTTP requests to webhook
- `ScrapingConfig.kt` - Data class for configuration

## Building

```bash
# Build debug APK
./gradlew assembleDebug

# Install on connected device
./gradlew installDebug

# Build release APK (requires signing configuration)
./gradlew assembleRelease
```

## License

This project is provided as-is for educational purposes.
