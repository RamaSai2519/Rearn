package com.rearn.instagram

import android.util.Log
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.util.concurrent.TimeUnit

object WebhookSender {
    
    private const val TAG = "WebhookSender"
    
    private val client = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .build()
    
    fun sendReel(webhookUrl: String, reelUrl: String) {
        try {
            val json = JSONObject().apply {
                put("reel_url", reelUrl)
                put("timestamp", System.currentTimeMillis())
            }
            
            val mediaType = "application/json; charset=utf-8".toMediaType()
            val body = json.toString().toRequestBody(mediaType)
            
            val request = Request.Builder()
                .url(webhookUrl)
                .post(body)
                .build()
            
            client.newCall(request).execute().use { response ->
                if (response.isSuccessful) {
                    Log.d(TAG, "Successfully sent to webhook: ${response.code}")
                } else {
                    Log.e(TAG, "Failed to send to webhook: ${response.code}")
                }
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error sending to webhook", e)
            throw e
        }
    }
}
