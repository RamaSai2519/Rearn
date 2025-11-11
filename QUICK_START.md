# Quick Start Guide

Get up and running with the Instagram Reels Scraper in minutes!

## Prerequisites Checklist

- [ ] Android Studio installed
- [ ] Android device with API 24+ (Android 7.0+)
- [ ] Instagram app installed on device
- [ ] USB cable to connect device
- [ ] USB debugging enabled on device

## 5-Minute Setup

### Step 1: Clone and Open (1 min)

```bash
git clone https://github.com/RamaSai2519/Rearn.git
cd Rearn
```

Open Android Studio → Open → Select the `Rearn` directory

### Step 2: Configure SDK (1 min)

1. Copy `local.properties.template` to `local.properties`
2. Edit `local.properties` and set your Android SDK path:
   ```
   sdk.dir=/path/to/your/Android/Sdk
   ```
3. Let Android Studio sync Gradle files

### Step 3: Connect Device (1 min)

```bash
# Check device is connected
adb devices

# Should show your device
# If not, enable USB debugging in Developer Options
```

### Step 4: Build & Install (1 min)

In Android Studio:
1. Click the green "Run" button (or press Shift+F10)
2. Select your connected device
3. Wait for app to install and launch

Or via command line:
```bash
./gradlew installDebug
```

### Step 5: Configure & Test (1 min)

On your device:

1. **Enable Accessibility Service:**
   - Open the Rearn app
   - Tap "Enable Accessibility Service"
   - Toggle ON "Rearn - Instagram Reels Scraper"
   - Return to app

2. **Set Up Test Scraping:**
   - Keywords: `travel`
   - Min Views: `10000`
   - Min Likes: `100`
   - Webhook: `https://webhook.site/YOUR-UNIQUE-ID`
     (Get one from https://webhook.site)

3. **Start Scraping:**
   - Tap "Start Scraping"
   - Instagram will open automatically
   - Check webhook.site for received URLs

## Testing the Webhook (Optional)

If you want to run a local webhook server:

```bash
# Install Flask
pip install -r requirements.txt

# Run the webhook server
python webhook_server.py

# In another terminal, expose with ngrok
ngrok http 5000

# Use the ngrok HTTPS URL in the app
```

## Common Issues

### Build Fails
```bash
./gradlew clean
./gradlew build
```

### App Doesn't Start
- Check `adb logcat -s InstagramAccessibility`
- Ensure Instagram is installed
- Restart accessibility service

### No Reels Found
- Lower the minimum views/likes criteria
- Try different keywords
- Check Instagram is logged in

## Next Steps

- Read [TESTING_GUIDE.md](TESTING_GUIDE.md) for detailed testing instructions
- Read [ARCHITECTURE.md](ARCHITECTURE.md) to understand how it works
- Customize the scraping behavior in `InstagramAccessibilityService.kt`

## Project Structure

```
Rearn/
├── app/
│   ├── src/main/
│   │   ├── java/com/rearn/instagram/
│   │   │   ├── MainActivity.kt                    # UI
│   │   │   ├── InstagramAccessibilityService.kt   # Core automation
│   │   │   ├── WebhookSender.kt                   # HTTP client
│   │   │   └── ScrapingConfig.kt                  # Config model
│   │   ├── res/
│   │   │   ├── layout/activity_main.xml           # Main UI layout
│   │   │   ├── values/strings.xml                 # String resources
│   │   │   └── xml/accessibility_service_config.xml
│   │   └── AndroidManifest.xml                    # App manifest
│   └── build.gradle                                # App dependencies
├── build.gradle                                    # Project config
├── webhook_server.py                               # Test webhook server
├── README.md                                       # Project overview
├── TESTING_GUIDE.md                                # Detailed testing guide
├── ARCHITECTURE.md                                 # Technical docs
└── QUICK_START.md                                  # This file
```

## Video Tutorial (Recommended)

For a visual walkthrough, check out this flow:

1. Build and install app
2. Enable accessibility service
3. Enter search criteria
4. Start scraping
5. Watch automation in action
6. Check webhook for results

## Support

If you run into issues:

1. Check logs: `adb logcat -s InstagramAccessibility`
2. Review the [TESTING_GUIDE.md](TESTING_GUIDE.md) troubleshooting section
3. Ensure your Instagram app is up to date
4. Try restarting the accessibility service

## Safety Tips

⚠️ **Important:**

- Use responsibly - this automates Instagram interactions
- Start with small batches (1-2 keywords, low scroll count)
- Monitor for Instagram rate limiting
- Keep device charged during long sessions
- Instagram may detect and restrict automated behavior

## What You Should See

When working correctly:

1. **On App Start:**
   - Clean UI with input fields
   - Status shows "Idle"
   - Reels found: 0

2. **After Starting:**
   - Instagram opens automatically
   - Navigates to search
   - Enters keyword
   - Scrolls through reels
   - Status shows "Running"
   - Reels counter increases

3. **On Webhook:**
   - JSON with `reel_url` and `timestamp`
   - Each matching reel sent once
   - Can view in webhook.site or your server logs

## Sample Output

Webhook receives:
```json
{
  "reel_url": "https://www.instagram.com/reel/ABC123xyz/",
  "timestamp": 1699564823000
}
```

Logs show:
```
D/InstagramAccessibility: Processing keyword: travel
D/InstagramAccessibility: Sent reel to webhook: https://www.instagram.com/reel/ABC123xyz/
```

## Ready to Customize?

Edit these values in `InstagramAccessibilityService.kt`:

- `MAX_SCROLLS_PER_KEYWORD`: How many reels to check per keyword (default: 50)
- Delay values: Speed up/slow down automation
- Scroll distance: Adjust scroll amount
- Criteria checking: Add more filters

---

**You're all set!** Start scraping and happy coding! 🚀
