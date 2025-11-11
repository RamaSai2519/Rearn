# Testing and Deployment Guide

## Prerequisites

Before you can test the Instagram Reels Scraper app on a physical device, ensure you have the following:

### Required Software

1. **Android Studio** (Latest version recommended)
   - Download from: https://developer.android.com/studio

2. **Java Development Kit (JDK) 17 or higher**
   - Check your JDK version: `java -version`

3. **Android SDK** (installed with Android Studio)
   - Required SDK components:
     - Android SDK Platform 34
     - Android SDK Build-Tools 34.0.0
     - Android SDK Platform-Tools

### Physical Device Setup

1. **Android Device Requirements:**
   - Android 7.0 (API 24) or higher
   - Instagram app installed from Google Play Store
   - USB debugging enabled

2. **Enable Developer Options:**
   - Go to Settings > About Phone
   - Tap "Build Number" 7 times
   - Developer options will be enabled

3. **Enable USB Debugging:**
   - Go to Settings > Developer Options
   - Enable "USB debugging"
   - Connect device via USB cable
   - Accept the USB debugging authorization on your device

## Building the App

### Using Android Studio

1. **Open Project:**
   ```bash
   # Open Android Studio and select "Open an existing project"
   # Navigate to the Rearn directory
   ```

2. **Sync Gradle:**
   - Android Studio will automatically sync Gradle files
   - Wait for the sync to complete
   - If prompted, download any missing SDK components

3. **Build the App:**
   - Click Build > Make Project
   - Or use shortcut: Ctrl+F9 (Windows/Linux) or Cmd+F9 (Mac)

4. **Run on Device:**
   - Connect your device via USB
   - Select your device from the device dropdown
   - Click Run > Run 'app'
   - Or use shortcut: Shift+F10 (Windows/Linux) or Ctrl+R (Mac)

### Using Command Line

1. **Build Debug APK:**
   ```bash
   cd /path/to/Rearn
   ./gradlew assembleDebug
   ```
   
   The APK will be generated at:
   `app/build/outputs/apk/debug/app-debug.apk`

2. **Install on Device:**
   ```bash
   # Check if device is connected
   adb devices
   
   # Install the APK
   adb install app/build/outputs/apk/debug/app-debug.apk
   
   # Or use Gradle to build and install
   ./gradlew installDebug
   ```

## Testing the App

### Step 1: Enable Accessibility Service

1. Launch the Rearn app on your device
2. Click "Enable Accessibility Service" button
3. You'll be taken to Settings > Accessibility
4. Find "Rearn - Instagram Reels Scraper" in the list
5. Toggle it ON
6. Confirm by clicking "Allow" in the permission dialog
7. Return to the Rearn app

### Step 2: Configure Scraping Parameters

1. **Enter Keywords:**
   - Example: `travel, food, fitness`
   - Separate multiple keywords with commas

2. **Set Minimum Views:**
   - Enter the minimum number of views (e.g., `10000`)
   - Leave empty or enter `0` for no minimum

3. **Set Minimum Likes:**
   - Enter the minimum number of likes (e.g., `500`)
   - Leave empty or enter `0` for no minimum

4. **Enter Webhook URL:**
   - This is where the reel URLs will be sent
   - Example: `https://your-server.com/webhook`
   - For testing, you can use services like:
     - RequestBin: https://requestbin.com
     - Webhook.site: https://webhook.site
     - Ngrok with a local server

### Step 3: Start Scraping

1. Click "Start Scraping" button
2. The app will minimize and Instagram will open automatically
3. The accessibility service will:
   - Navigate to the search page
   - Search for your keywords
   - Navigate to the Reels tab
   - Scroll through reels
   - Copy URLs of reels matching your criteria
   - Send URLs to your webhook

4. **Monitor Progress:**
   - Return to the Rearn app to see the "Reels found" counter
   - The status will show "Running"

5. **Stop Scraping:**
   - Open the Rearn app
   - Click "Stop Scraping" button

## Viewing Logs

### Using ADB Logcat

Monitor the app's behavior in real-time:

```bash
# View all logs from the app
adb logcat -s InstagramAccessibility

# Save logs to a file
adb logcat -s InstagramAccessibility > scraper_logs.txt

# Clear existing logs before starting
adb logcat -c

# View with timestamp
adb logcat -v time -s InstagramAccessibility
```

### Using Android Studio

1. Open Logcat panel (View > Tool Windows > Logcat)
2. Select your device
3. Filter by "InstagramAccessibility" tag
4. Set log level to "Debug" to see all messages

## Setting Up a Test Webhook

### Option 1: Using webhook.site (Easiest for testing)

1. Visit https://webhook.site
2. You'll get a unique URL like: `https://webhook.site/your-unique-id`
3. Copy this URL
4. Paste it in the Rearn app's "Webhook URL" field
5. After scraping, refresh the webhook.site page to see received URLs

### Option 2: Using a Local Server with ngrok

1. **Create a simple webhook server:**
   
   ```python
   # webhook_server.py
   from flask import Flask, request
   import json
   
   app = Flask(__name__)
   
   @app.route('/webhook', methods=['POST'])
   def webhook():
       data = request.json
       print(f"Received: {json.dumps(data, indent=2)}")
       with open('reels.txt', 'a') as f:
           f.write(f"{data['reel_url']}\n")
       return {'status': 'success'}, 200
   
   if __name__ == '__main__':
       app.run(port=5000)
   ```

2. **Install requirements:**
   ```bash
   pip install flask
   ```

3. **Run the server:**
   ```bash
   python webhook_server.py
   ```

4. **Expose with ngrok:**
   ```bash
   # Install ngrok from https://ngrok.com/
   ngrok http 5000
   ```

5. **Use the ngrok URL:**
   - ngrok will provide a URL like: `https://abc123.ngrok.io`
   - Use `https://abc123.ngrok.io/webhook` in the Rearn app

## Troubleshooting

### App doesn't open Instagram

**Solution:**
- Make sure Instagram is installed
- Grant all necessary permissions
- Restart the device and try again

### Accessibility service not working

**Solution:**
- Go to Settings > Accessibility
- Disable and re-enable the Rearn service
- Restart the app
- Some devices may require additional permissions

### No reels found

**Solution:**
- Check your minimum views/likes criteria (they might be too high)
- Ensure Instagram's UI hasn't changed significantly
- Check logs with `adb logcat -s InstagramAccessibility`
- The keywords might not return reel results

### Webhook not receiving data

**Solution:**
- Test your webhook URL in a browser or with curl:
  ```bash
  curl -X POST https://your-webhook-url \
    -H "Content-Type: application/json" \
    -d '{"reel_url":"https://test.com","timestamp":1234567890}'
  ```
- Check if your server/webhook.site is accessible
- Verify the URL is correct (no typos)

### Build errors

**Solution:**
- Update Android Studio to the latest version
- File > Invalidate Caches and Restart
- Clean and rebuild:
  ```bash
  ./gradlew clean
  ./gradlew build
  ```

## Advanced Configuration

### Modifying Search Behavior

Edit `InstagramAccessibilityService.kt` to customize:

- **MAX_SCROLLS_PER_KEYWORD**: Maximum reels to check per keyword (default: 50)
- **Delay times**: Adjust `delay()` calls to make the automation slower/faster
- **Scroll distance**: Modify `scrollDown()` function for different scroll amounts

### Adding More Criteria

You can extend the `checkReelCriteria()` function to add additional filtering:

- Check for specific hashtags
- Filter by account follower count
- Check engagement rate
- Filter by post date

## Performance Tips

1. **Use realistic delays:**
   - Too fast = might miss elements loading
   - Too slow = wastes time

2. **Limit keywords:**
   - Processing too many keywords takes time
   - Start with 1-2 keywords for testing

3. **Adjust criteria:**
   - Lower minimum views/likes = more results
   - Higher criteria = more selective

4. **Monitor battery:**
   - Keep device charged during long scraping sessions
   - The app can consume significant battery

## Security and Privacy

⚠️ **Important Notes:**

1. **Instagram Terms of Service:**
   - This app automates Instagram interactions
   - Use responsibly and at your own risk
   - Instagram may detect and restrict automated behavior

2. **Webhook Security:**
   - Use HTTPS webhooks for production
   - Don't expose sensitive webhook URLs publicly
   - Implement authentication on your webhook endpoint

3. **Data Privacy:**
   - The app only collects publicly visible information
   - No Instagram credentials are stored
   - All data is sent directly to your specified webhook

## Next Steps

After successful testing:

1. **Fine-tune parameters** based on your needs
2. **Implement webhook processing** to handle received URLs
3. **Add error handling** for your specific use case
4. **Consider rate limiting** to avoid Instagram restrictions
5. **Monitor for Instagram UI changes** that may require code updates

## Support

For issues or questions:

1. Check the logs first: `adb logcat -s InstagramAccessibility`
2. Review the troubleshooting section above
3. Check Instagram's current UI for any recent changes
4. Ensure all prerequisites are met

## Building for Production

If you want to create a signed release APK:

1. **Generate a keystore:**
   ```bash
   keytool -genkey -v -keystore my-release-key.jks \
     -keyalg RSA -keysize 2048 -validity 10000 \
     -alias my-key-alias
   ```

2. **Add to `app/build.gradle`:**
   ```gradle
   android {
       ...
       signingConfigs {
           release {
               storeFile file("my-release-key.jks")
               storePassword "your-password"
               keyAlias "my-key-alias"
               keyPassword "your-password"
           }
       }
       buildTypes {
           release {
               signingConfig signingConfigs.release
               ...
           }
       }
   }
   ```

3. **Build release APK:**
   ```bash
   ./gradlew assembleRelease
   ```

The signed APK will be at:
`app/build/outputs/apk/release/app-release.apk`
