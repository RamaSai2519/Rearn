package com.rearn.instagram

data class ScrapingConfig(
    val keywords: List<String>,
    val minViews: Long,
    val minLikes: Long,
    val webhookUrl: String
)
