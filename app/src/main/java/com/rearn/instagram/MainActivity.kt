package com.rearn.instagram

import android.content.Intent
import android.os.Bundle
import android.provider.Settings
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.google.android.material.textfield.TextInputEditText
import android.widget.Button
import android.widget.TextView
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {
    
    private lateinit var keywordsInput: TextInputEditText
    private lateinit var minViewsInput: TextInputEditText
    private lateinit var minLikesInput: TextInputEditText
    private lateinit var webhookUrlInput: TextInputEditText
    private lateinit var startButton: Button
    private lateinit var stopButton: Button
    private lateinit var enableAccessibilityButton: Button
    private lateinit var statusText: TextView
    private lateinit var reelsCountText: TextView
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        initializeViews()
        setupListeners()
        observeServiceState()
    }
    
    private fun initializeViews() {
        keywordsInput = findViewById(R.id.keywordsInput)
        minViewsInput = findViewById(R.id.minViewsInput)
        minLikesInput = findViewById(R.id.minLikesInput)
        webhookUrlInput = findViewById(R.id.webhookUrlInput)
        startButton = findViewById(R.id.startButton)
        stopButton = findViewById(R.id.stopButton)
        enableAccessibilityButton = findViewById(R.id.enableAccessibilityButton)
        statusText = findViewById(R.id.statusText)
        reelsCountText = findViewById(R.id.reelsCountText)
    }
    
    private fun setupListeners() {
        enableAccessibilityButton.setOnClickListener {
            openAccessibilitySettings()
        }
        
        startButton.setOnClickListener {
            startScraping()
        }
        
        stopButton.setOnClickListener {
            stopScraping()
        }
    }
    
    private fun openAccessibilitySettings() {
        val intent = Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS)
        startActivity(intent)
        Toast.makeText(
            this,
            "Please enable 'Rearn - Instagram Reels Scraper' service",
            Toast.LENGTH_LONG
        ).show()
    }
    
    private fun startScraping() {
        val keywords = keywordsInput.text.toString().trim()
        val minViewsStr = minViewsInput.text.toString().trim()
        val minLikesStr = minLikesInput.text.toString().trim()
        val webhookUrl = webhookUrlInput.text.toString().trim()
        
        if (keywords.isEmpty()) {
            Toast.makeText(this, "Please enter keywords", Toast.LENGTH_SHORT).show()
            return
        }
        
        if (webhookUrl.isEmpty()) {
            Toast.makeText(this, "Please enter webhook URL", Toast.LENGTH_SHORT).show()
            return
        }
        
        val minViews = minViewsStr.toLongOrNull() ?: 0L
        val minLikes = minLikesStr.toLongOrNull() ?: 0L
        
        val config = ScrapingConfig(
            keywords = keywords.split(",").map { it.trim() }.filter { it.isNotEmpty() },
            minViews = minViews,
            minLikes = minLikes,
            webhookUrl = webhookUrl
        )
        
        if (!isAccessibilityServiceEnabled()) {
            Toast.makeText(
                this,
                "Please enable accessibility service first",
                Toast.LENGTH_LONG
            ).show()
            openAccessibilitySettings()
            return
        }
        
        InstagramAccessibilityService.startScraping(config)
        startButton.isEnabled = false
        stopButton.isEnabled = true
        statusText.text = getString(R.string.status_running)
    }
    
    private fun stopScraping() {
        InstagramAccessibilityService.stopScraping()
        startButton.isEnabled = true
        stopButton.isEnabled = false
        statusText.text = getString(R.string.status_stopped)
    }
    
    private fun isAccessibilityServiceEnabled(): Boolean {
        val service = "${packageName}/${InstagramAccessibilityService::class.java.name}"
        val enabledServices = Settings.Secure.getString(
            contentResolver,
            Settings.Secure.ENABLED_ACCESSIBILITY_SERVICES
        )
        return enabledServices?.contains(service) == true
    }
    
    private fun observeServiceState() {
        lifecycleScope.launch {
            InstagramAccessibilityService.reelsFoundFlow.collectLatest { count ->
                reelsCountText.text = getString(R.string.reels_found, count)
            }
        }
    }
}
