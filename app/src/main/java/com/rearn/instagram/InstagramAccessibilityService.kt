package com.rearn.instagram

import android.accessibilityservice.AccessibilityService
import android.accessibilityservice.GestureDescription
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.graphics.Path
import android.graphics.Rect
import android.os.Handler
import android.os.Looper
import android.util.Log
import android.view.accessibility.AccessibilityEvent
import android.view.accessibility.AccessibilityNodeInfo
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class InstagramAccessibilityService : AccessibilityService() {

    private val serviceScope = CoroutineScope(SupervisorJob() + Dispatchers.Main)
    private val handler = Handler(Looper.getMainLooper())
    private var isRunning = false
    private var currentKeywordIndex = 0
    private var scrollCount = 0
    private var lastClipboardContent = ""
    
    companion object {
        private const val TAG = "InstagramAccessibility"
        private const val INSTAGRAM_PACKAGE = "com.instagram.android"
        private const val MAX_SCROLLS_PER_KEYWORD = 50
        
        private var currentConfig: ScrapingConfig? = null
        private val _reelsFoundFlow = MutableStateFlow(0)
        val reelsFoundFlow: StateFlow<Int> = _reelsFoundFlow
        
        fun startScraping(config: ScrapingConfig) {
            currentConfig = config
        }
        
        fun stopScraping() {
            currentConfig = null
        }
    }
    
    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        if (!isRunning && currentConfig != null) {
            startScrapingProcess()
        }
    }
    
    override fun onInterrupt() {
        Log.d(TAG, "Service interrupted")
    }
    
    override fun onServiceConnected() {
        super.onServiceConnected()
        Log.d(TAG, "Accessibility service connected")
    }
    
    private fun startScrapingProcess() {
        isRunning = true
        serviceScope.launch {
            try {
                val config = currentConfig ?: return@launch
                
                // Open Instagram
                if (!openInstagram()) {
                    Log.e(TAG, "Failed to open Instagram")
                    isRunning = false
                    return@launch
                }
                
                delay(3000) // Wait for Instagram to load
                
                // Navigate to search/explore
                if (!navigateToSearch()) {
                    Log.e(TAG, "Failed to navigate to search")
                    isRunning = false
                    return@launch
                }
                
                delay(2000)
                
                // Process each keyword
                for (keyword in config.keywords) {
                    if (currentConfig == null) break
                    
                    Log.d(TAG, "Processing keyword: $keyword")
                    currentKeywordIndex = config.keywords.indexOf(keyword)
                    
                    // Search with keyword
                    if (!searchWithKeyword(keyword)) {
                        Log.e(TAG, "Failed to search with keyword: $keyword")
                        continue
                    }
                    
                    delay(2000)
                    
                    // Navigate to Reels tab
                    if (!navigateToReelsTab()) {
                        Log.e(TAG, "Failed to navigate to Reels tab")
                        continue
                    }
                    
                    delay(2000)
                    
                    // Click first reel
                    if (!clickFirstReel()) {
                        Log.e(TAG, "Failed to click first reel")
                        continue
                    }
                    
                    delay(2000)
                    
                    // Scroll and check reels
                    scrollCount = 0
                    scrollAndCheckReels(config)
                    
                    // Go back to search
                    performGlobalAction(GLOBAL_ACTION_BACK)
                    delay(1000)
                    performGlobalAction(GLOBAL_ACTION_BACK)
                    delay(1000)
                }
                
            } catch (e: Exception) {
                Log.e(TAG, "Error in scraping process", e)
            } finally {
                isRunning = false
            }
        }
    }
    
    private fun openInstagram(): Boolean {
        try {
            val intent = packageManager.getLaunchIntentForPackage(INSTAGRAM_PACKAGE)
            if (intent != null) {
                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                startActivity(intent)
                return true
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error opening Instagram", e)
        }
        return false
    }
    
    private suspend fun navigateToSearch(): Boolean {
        delay(500)
        val rootNode = rootInActiveWindow ?: return false
        
        // Try to find search icon or explore icon
        val searchIcon = findNodeByResourceId(rootNode, "com.instagram.android:id/search_tab")
            ?: findNodeByText(rootNode, "Search")
            ?: findNodeByContentDescription(rootNode, "Search and Explore")
        
        if (searchIcon != null) {
            // Long press on search icon
            val rect = Rect()
            searchIcon.getBoundsInScreen(rect)
            performLongPress(rect.centerX().toFloat(), rect.centerY().toFloat())
            searchIcon.recycle()
            return true
        }
        
        rootNode.recycle()
        return false
    }
    
    private suspend fun searchWithKeyword(keyword: String): Boolean {
        delay(500)
        val rootNode = rootInActiveWindow ?: return false
        
        // Find search input field
        val searchField = findNodeByResourceId(rootNode, "com.instagram.android:id/action_bar_search_edit_text")
            ?: findEditTextNode(rootNode)
        
        if (searchField != null) {
            // Click on search field
            searchField.performAction(AccessibilityNodeInfo.ACTION_CLICK)
            delay(500)
            
            // Enter text
            val arguments = android.os.Bundle()
            arguments.putCharSequence(AccessibilityNodeInfo.ACTION_ARGUMENT_SET_TEXT_CHARSEQUENCE, keyword)
            searchField.performAction(AccessibilityNodeInfo.ACTION_SET_TEXT, arguments)
            delay(1000)
            
            // Press enter/search
            searchField.performAction(AccessibilityNodeInfo.ACTION_IME_ACTION)
            searchField.recycle()
            rootNode.recycle()
            return true
        }
        
        rootNode.recycle()
        return false
    }
    
    private suspend fun navigateToReelsTab(): Boolean {
        delay(500)
        val rootNode = rootInActiveWindow ?: return false
        
        // Look for Reels tab
        val reelsTab = findNodeByText(rootNode, "Reels")
            ?: findNodeByContentDescription(rootNode, "Reels")
        
        if (reelsTab != null) {
            reelsTab.performAction(AccessibilityNodeInfo.ACTION_CLICK)
            reelsTab.recycle()
            rootNode.recycle()
            return true
        }
        
        rootNode.recycle()
        return false
    }
    
    private suspend fun clickFirstReel(): Boolean {
        delay(500)
        val rootNode = rootInActiveWindow ?: return false
        
        // Find clickable video elements or image views that represent reels
        val firstReel = findClickableNode(rootNode)
        
        if (firstReel != null) {
            firstReel.performAction(AccessibilityNodeInfo.ACTION_CLICK)
            firstReel.recycle()
            rootNode.recycle()
            return true
        }
        
        rootNode.recycle()
        return false
    }
    
    private suspend fun scrollAndCheckReels(config: ScrapingConfig) {
        while (scrollCount < MAX_SCROLLS_PER_KEYWORD && currentConfig != null) {
            delay(1500)
            
            // Check if current reel meets criteria
            if (checkReelCriteria(config)) {
                // Copy link
                if (copyReelLink()) {
                    delay(1000)
                    // Get link from clipboard
                    val link = getClipboardContent()
                    if (link.isNotEmpty() && link != lastClipboardContent) {
                        lastClipboardContent = link
                        // Send to webhook
                        sendToWebhook(config.webhookUrl, link)
                        _reelsFoundFlow.value += 1
                    }
                }
            }
            
            // Scroll to next reel
            scrollDown()
            scrollCount++
            delay(500)
        }
    }
    
    private suspend fun checkReelCriteria(config: ScrapingConfig): Boolean {
        // This is a simplified check - Instagram's UI changes frequently
        // In a real implementation, you'd need to identify the exact elements
        // that show views and likes counts
        val rootNode = rootInActiveWindow ?: return false
        
        try {
            // Look for view count and like count text
            // This is approximate and may need adjustment based on Instagram's current UI
            val allTextNodes = mutableListOf<AccessibilityNodeInfo>()
            collectAllTextNodes(rootNode, allTextNodes)
            
            var hasEnoughViews = config.minViews == 0L
            var hasEnoughLikes = config.minLikes == 0L
            
            for (node in allTextNodes) {
                val text = node.text?.toString() ?: continue
                
                // Check for view count (e.g., "1.2M views" or "100K views")
                if (text.contains("views", ignoreCase = true) || 
                    text.contains("view", ignoreCase = true)) {
                    val viewCount = parseCount(text)
                    if (viewCount >= config.minViews) {
                        hasEnoughViews = true
                    }
                }
                
                // Check for like count
                if (text.contains("likes", ignoreCase = true) || 
                    text.contains("like", ignoreCase = true)) {
                    val likeCount = parseCount(text)
                    if (likeCount >= config.minLikes) {
                        hasEnoughLikes = true
                    }
                }
            }
            
            allTextNodes.forEach { it.recycle() }
            rootNode.recycle()
            
            return hasEnoughViews && hasEnoughLikes
        } catch (e: Exception) {
            Log.e(TAG, "Error checking reel criteria", e)
            rootNode.recycle()
            return false
        }
    }
    
    private suspend fun copyReelLink(): Boolean {
        val rootNode = rootInActiveWindow ?: return false
        
        try {
            // Find share button (usually a paper plane icon or "Share" text)
            val shareButton = findNodeByContentDescription(rootNode, "Share")
                ?: findNodeByResourceId(rootNode, "com.instagram.android:id/row_feed_button_share")
                ?: findNodeByText(rootNode, "Share")
            
            if (shareButton != null) {
                shareButton.performAction(AccessibilityNodeInfo.ACTION_CLICK)
                delay(1000)
                
                // Find "Copy Link" option
                val copyLinkButton = findNodeByText(rootInActiveWindow, "Copy link")
                    ?: findNodeByText(rootInActiveWindow, "Copy Link")
                
                if (copyLinkButton != null) {
                    copyLinkButton.performAction(AccessibilityNodeInfo.ACTION_CLICK)
                    delay(500)
                    
                    // Close share sheet
                    performGlobalAction(GLOBAL_ACTION_BACK)
                    delay(500)
                    
                    copyLinkButton.recycle()
                    shareButton.recycle()
                    rootNode.recycle()
                    return true
                }
                
                shareButton.recycle()
            }
            
            rootNode.recycle()
            return false
        } catch (e: Exception) {
            Log.e(TAG, "Error copying link", e)
            rootNode.recycle()
            return false
        }
    }
    
    private fun scrollDown() {
        val displayMetrics = resources.displayMetrics
        val screenHeight = displayMetrics.heightPixels
        val screenWidth = displayMetrics.widthPixels
        
        val startY = screenHeight * 0.8f
        val endY = screenHeight * 0.2f
        val x = screenWidth / 2f
        
        performSwipe(x, startY, x, endY, 300)
    }
    
    private fun performSwipe(startX: Float, startY: Float, endX: Float, endY: Float, duration: Long) {
        val path = Path()
        path.moveTo(startX, startY)
        path.lineTo(endX, endY)
        
        val gestureBuilder = GestureDescription.Builder()
        gestureBuilder.addStroke(GestureDescription.StrokeDescription(path, 0, duration))
        
        dispatchGesture(gestureBuilder.build(), null, null)
    }
    
    private fun performLongPress(x: Float, y: Float) {
        val path = Path()
        path.moveTo(x, y)
        
        val gestureBuilder = GestureDescription.Builder()
        gestureBuilder.addStroke(GestureDescription.StrokeDescription(path, 0, 1000))
        
        dispatchGesture(gestureBuilder.build(), null, null)
    }
    
    private fun getClipboardContent(): String {
        val clipboard = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
        val clip = clipboard.primaryClip
        if (clip != null && clip.itemCount > 0) {
            return clip.getItemAt(0).text?.toString() ?: ""
        }
        return ""
    }
    
    private fun sendToWebhook(webhookUrl: String, reelUrl: String) {
        serviceScope.launch(Dispatchers.IO) {
            try {
                WebhookSender.sendReel(webhookUrl, reelUrl)
                Log.d(TAG, "Sent reel to webhook: $reelUrl")
            } catch (e: Exception) {
                Log.e(TAG, "Error sending to webhook", e)
            }
        }
    }
    
    // Helper functions for finding nodes
    private fun findNodeByResourceId(root: AccessibilityNodeInfo, resourceId: String): AccessibilityNodeInfo? {
        val nodes = root.findAccessibilityNodeInfosByViewId(resourceId)
        return if (nodes.isNotEmpty()) nodes[0] else null
    }
    
    private fun findNodeByText(root: AccessibilityNodeInfo?, text: String): AccessibilityNodeInfo? {
        if (root == null) return null
        val nodes = root.findAccessibilityNodeInfosByText(text)
        return if (nodes.isNotEmpty()) nodes[0] else null
    }
    
    private fun findNodeByContentDescription(root: AccessibilityNodeInfo, description: String): AccessibilityNodeInfo? {
        if (root.contentDescription?.toString()?.contains(description, ignoreCase = true) == true) {
            return root
        }
        
        for (i in 0 until root.childCount) {
            val child = root.getChild(i) ?: continue
            val result = findNodeByContentDescription(child, description)
            if (result != null) {
                child.recycle()
                return result
            }
            child.recycle()
        }
        
        return null
    }
    
    private fun findEditTextNode(root: AccessibilityNodeInfo): AccessibilityNodeInfo? {
        if (root.className == "android.widget.EditText") {
            return root
        }
        
        for (i in 0 until root.childCount) {
            val child = root.getChild(i) ?: continue
            val result = findEditTextNode(child)
            if (result != null) {
                child.recycle()
                return result
            }
            child.recycle()
        }
        
        return null
    }
    
    private fun findClickableNode(root: AccessibilityNodeInfo): AccessibilityNodeInfo? {
        if (root.isClickable && root.isVisibleToUser) {
            return root
        }
        
        for (i in 0 until root.childCount) {
            val child = root.getChild(i) ?: continue
            if (child.isClickable && child.isVisibleToUser) {
                return child
            }
            child.recycle()
        }
        
        return null
    }
    
    private fun collectAllTextNodes(root: AccessibilityNodeInfo, nodes: MutableList<AccessibilityNodeInfo>) {
        if (root.text != null && root.text.isNotEmpty()) {
            nodes.add(root)
        }
        
        for (i in 0 until root.childCount) {
            val child = root.getChild(i) ?: continue
            collectAllTextNodes(child, nodes)
        }
    }
    
    private fun parseCount(text: String): Long {
        try {
            // Remove non-numeric characters except decimal point
            val cleaned = text.replace(Regex("[^0-9.KMB]"), "")
            
            // Check for K, M, B suffixes
            return when {
                cleaned.contains("B", ignoreCase = true) -> {
                    val num = cleaned.replace("B", "", ignoreCase = true).toFloatOrNull() ?: 0f
                    (num * 1_000_000_000).toLong()
                }
                cleaned.contains("M", ignoreCase = true) -> {
                    val num = cleaned.replace("M", "", ignoreCase = true).toFloatOrNull() ?: 0f
                    (num * 1_000_000).toLong()
                }
                cleaned.contains("K", ignoreCase = true) -> {
                    val num = cleaned.replace("K", "", ignoreCase = true).toFloatOrNull() ?: 0f
                    (num * 1_000).toLong()
                }
                else -> cleaned.toLongOrNull() ?: 0L
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error parsing count: $text", e)
            return 0L
        }
    }
}
