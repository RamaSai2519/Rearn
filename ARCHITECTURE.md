# Architecture Documentation

## Overview

The Rearn Instagram Reels Scraper is an Android application that automates the process of finding trending Instagram reels based on user-defined criteria and sending their URLs to a webhook endpoint.

## Components

### 1. MainActivity (`MainActivity.kt`)

The main user interface of the application.

**Responsibilities:**
- Display input fields for scraping parameters (keywords, min views, min likes, webhook URL)
- Handle user interactions (start/stop scraping, enable accessibility service)
- Monitor and display scraping status and progress
- Open accessibility settings

**Key Features:**
- Material Design UI with TextInputLayout
- Real-time status updates
- Reels counter updates via StateFlow

### 2. InstagramAccessibilityService (`InstagramAccessibilityService.kt`)

The core automation engine using Android's Accessibility Service API.

**Responsibilities:**
- Automate Instagram app navigation
- Search for reels using provided keywords
- Scroll through reels and evaluate criteria
- Extract reel URLs
- Send URLs to webhook

**Workflow:**
1. Open Instagram app
2. Navigate to search/explore page
3. For each keyword:
   - Enter keyword in search field
   - Navigate to Reels tab
   - Click first reel
   - Scroll through reels (up to MAX_SCROLLS_PER_KEYWORD)
   - For each reel:
     - Check views and likes against criteria
     - If criteria met, copy reel URL
     - Send URL to webhook
4. Return to search and process next keyword

**Key Functions:**
- `navigateToSearch()`: Find and interact with search icon
- `searchWithKeyword()`: Enter text in search field
- `navigateToReelsTab()`: Click on Reels tab
- `clickFirstReel()`: Open first reel in results
- `scrollAndCheckReels()`: Main loop for checking reels
- `checkReelCriteria()`: Parse and validate view/like counts
- `copyReelLink()`: Interact with share button and copy link
- `parseCount()`: Convert text like "1.2M" to numeric values

### 3. WebhookSender (`WebhookSender.kt`)

Handles HTTP communication with the webhook endpoint.

**Responsibilities:**
- Send POST requests to webhook URL
- Format data as JSON
- Handle network errors gracefully

**Data Format:**
```json
{
  "reel_url": "https://www.instagram.com/reel/...",
  "timestamp": 1234567890
}
```

### 4. ScrapingConfig (`ScrapingConfig.kt`)

Simple data class to hold scraping configuration.

**Fields:**
- `keywords`: List of search keywords
- `minViews`: Minimum view count filter
- `minLikes`: Minimum like count filter
- `webhookUrl`: Destination URL for reel data

## Data Flow

```
User Input (MainActivity)
    ↓
ScrapingConfig
    ↓
InstagramAccessibilityService
    ↓
Instagram App (via Accessibility API)
    ↓
Reel Detection & Validation
    ↓
Clipboard (Copy Link)
    ↓
WebhookSender
    ↓
Webhook Endpoint
```

## Technical Details

### Accessibility Service Configuration

The service is configured in `accessibility_service_config.xml`:

- **accessibilityEventTypes**: `typeAllMask` - Receive all accessibility events
- **accessibilityFeedbackType**: `feedbackGeneric` - Provide generic feedback
- **canRetrieveWindowContent**: `true` - Access window content for automation
- **packageNames**: `com.instagram.android` - Only monitor Instagram

### Permissions

1. **INTERNET**: Required for webhook HTTP requests
2. **BIND_ACCESSIBILITY_SERVICE**: Required to run as accessibility service
3. **QUERY_ALL_PACKAGES**: Required to detect and launch Instagram app

### UI Navigation Strategy

The service uses multiple strategies to find UI elements:

1. **Resource ID**: Most reliable but Instagram may change IDs
   ```kotlin
   findNodeByResourceId(root, "com.instagram.android:id/search_tab")
   ```

2. **Text Content**: Find elements by visible text
   ```kotlin
   findNodeByText(root, "Search")
   ```

3. **Content Description**: Find elements by accessibility description
   ```kotlin
   findNodeByContentDescription(root, "Search and Explore")
   ```

4. **Element Type**: Find by Android widget type
   ```kotlin
   findEditTextNode(root) // Finds EditText widgets
   ```

### Gesture Automation

The service performs gestures using `GestureDescription`:

- **Swipe**: Scroll through reels
- **Long Press**: Navigate to search
- **Tap**: Click elements

### Count Parsing

The app parses human-readable numbers (e.g., "1.2M views", "500K likes"):

```kotlin
parseCount("1.2M views") // Returns 1,200,000
parseCount("500K likes") // Returns 500,000
parseCount("100 views")  // Returns 100
```

Supports: K (thousands), M (millions), B (billions)

## Scalability Considerations

### Current Limitations

1. **Single Keyword Processing**: Keywords are processed sequentially
2. **Fixed Scroll Limit**: `MAX_SCROLLS_PER_KEYWORD = 50`
3. **No Deduplication**: Same reel may be sent multiple times
4. **No Retry Logic**: Failed webhook calls are logged but not retried
5. **Instagram UI Dependency**: Breaks when Instagram updates UI

### Potential Improvements

1. **Parallel Processing**: Process multiple keywords simultaneously
2. **URL Deduplication**: Maintain a set of seen URLs
3. **Configurable Limits**: Make scroll count user-configurable
4. **Retry Queue**: Implement exponential backoff for failed webhooks
5. **UI Fingerprinting**: More robust element detection
6. **Progress Persistence**: Save state to resume after interruption
7. **Machine Learning**: Use ML to detect reel elements more reliably

## Error Handling

### Accessibility Service Errors

- **Service Not Enabled**: User is prompted to enable in settings
- **Instagram Not Installed**: Caught and logged
- **Element Not Found**: Operation skipped, continues with next step
- **Window Content Unavailable**: Service waits and retries

### Network Errors

- **Connection Timeout**: Logged to console (30s timeout)
- **HTTP Errors**: Status code logged
- **Malformed URL**: Exception caught and logged

### Parsing Errors

- **Invalid Count Format**: Returns 0, continues processing
- **Missing Elements**: Operation skipped gracefully

## Testing Strategy

### Unit Testing

- Test `parseCount()` with various input formats
- Test `ScrapingConfig` validation
- Test JSON serialization in `WebhookSender`

### Integration Testing

- Test accessibility service element detection
- Test gesture execution
- Test clipboard operations
- Test webhook communication

### Manual Testing

- Test on multiple Android versions (7.0+)
- Test on different Instagram versions
- Test with various device screen sizes
- Test network failure scenarios
- Test accessibility permission flow

## Security Considerations

### Data Privacy

- No Instagram credentials stored or transmitted
- Only public reel data is collected
- All data sent to user-specified webhook only

### Network Security

- Supports both HTTP and HTTPS webhooks
- HTTPS recommended for production use
- No sensitive data cached locally

### Permission Risks

- Accessibility service can read all screen content
- Service is scoped to Instagram package only
- Service only runs when user explicitly starts scraping

## Maintenance

### Instagram UI Changes

Instagram frequently updates its UI. When the app stops working:

1. Use `adb logcat` to see which element detection failed
2. Inspect Instagram's current UI using Android Layout Inspector
3. Update resource IDs, text strings, or detection logic
4. Test thoroughly before deploying

### Android API Updates

- Monitor Android deprecation notices
- Test on new Android versions
- Update `targetSdk` when ready
- Check accessibility API changes

## Performance

### Battery Usage

- Continuous screen monitoring: High battery usage
- Network requests: Moderate battery usage
- Recommend keeping device charged during long sessions

### Memory Usage

- Accessibility event processing: Low memory usage
- OkHttp client: Moderate memory usage
- No large data structures maintained

### Network Usage

- Each reel URL sent: ~200 bytes
- Total usage depends on number of matching reels
- Minimal data transfer overall

## Dependencies

### Runtime Dependencies

- `androidx.core:core-ktx:1.12.0` - AndroidX core utilities
- `androidx.appcompat:appcompat:1.6.1` - AppCompat support
- `com.google.android.material:material:1.10.0` - Material Design components
- `androidx.constraintlayout:constraintlayout:2.1.4` - Layout manager
- `androidx.lifecycle:lifecycle-runtime-ktx:2.6.2` - Lifecycle components
- `com.squareup.okhttp3:okhttp:4.11.0` - HTTP client
- `org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3` - Coroutines

### Build Dependencies

- Android Gradle Plugin: 8.1.0
- Kotlin: 1.9.0
- Gradle: 8.0

## Future Enhancements

1. **Database Integration**: Store reel metadata locally
2. **Analytics Dashboard**: Show scraping statistics
3. **Scheduled Scraping**: Run at specific times
4. **Multi-Platform Support**: Support TikTok, YouTube Shorts
5. **Advanced Filtering**: Hashtags, accounts, engagement rate
6. **Batch Export**: Export all URLs to CSV/JSON
7. **Notification System**: Alert when target reels found
8. **Cloud Sync**: Sync found reels across devices
