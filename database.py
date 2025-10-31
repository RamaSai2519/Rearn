"""
MongoDB Database Handler for Instagram Bot
Tracks posted content to avoid duplicates
"""
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)


class MongoDBHandler:
    """Handles MongoDB operations for tracking posted content"""
    
    def __init__(self, connection_string: str):
        """
        Initialize MongoDB connection
        
        Args:
            connection_string: MongoDB connection URI
        """
        self.connection_string = connection_string
        self.client = None
        self.db = None
        self.collection = None
        
    def connect(self):
        """Establish connection to MongoDB"""
        try:
            self.client = MongoClient(self.connection_string)
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client['instagram_bot']
            self.collection = self.db['posted_content']
            logger.info("Successfully connected to MongoDB")
            return True
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            return False
            
    def is_content_posted(self, content_id: str) -> bool:
        """
        Check if content has already been posted
        
        Args:
            content_id: Unique identifier for the content
            
        Returns:
            True if content was already posted, False otherwise
        """
        if not self.collection:
            return False
            
        result = self.collection.find_one({"content_id": content_id})
        return result is not None
        
    def mark_content_posted(self, content_id: str, content_url: str, source_url: str):
        """
        Mark content as posted to avoid duplicate posts
        
        Args:
            content_id: Unique identifier for the content
            content_url: URL of the posted content
            source_url: Original source URL
        """
        if not self.collection:
            logger.error("MongoDB collection not initialized")
            return
            
        document = {
            "content_id": content_id,
            "content_url": content_url,
            "source_url": source_url,
            "posted_at": datetime.utcnow(),
            "status": "posted"
        }
        
        try:
            self.collection.insert_one(document)
            logger.info(f"Marked content {content_id} as posted")
        except Exception as e:
            logger.error(f"Failed to mark content as posted: {e}")
            
    def get_posted_count(self) -> int:
        """Get total number of posted content items"""
        if not self.collection:
            return 0
        return self.collection.count_documents({})
        
    def get_recent_posts(self, limit: int = 10) -> List[dict]:
        """
        Get most recent posted content
        
        Args:
            limit: Maximum number of posts to retrieve
            
        Returns:
            List of recent posts
        """
        if not self.collection:
            return []
            
        posts = self.collection.find().sort("posted_at", -1).limit(limit)
        return list(posts)
        
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")
