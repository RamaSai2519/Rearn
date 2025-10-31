"""
Content Poster Module
Handles posting/uploading content to Instagram
"""
import logging
import os
import random
from typing import Optional, List
from pathlib import Path
from instagrapi import Client
from instagrapi.types import Usertag, Location

logger = logging.getLogger(__name__)


class ContentPoster:
    """Posts content to Instagram"""
    
    # Brainrot-style captions
    CAPTION_TEMPLATES = [
        "This is peak brainrot 💀🔥 #{hashtag}",
        "POV: Your fyp rn 😭 #{hashtag}",
        "This is so sigma 💪😎 #{hashtag}",
        "Actual brainrot content 🧠🔥 #{hashtag}",
        "No way this is real 💀 #{hashtag}",
        "The algorithm brought you here 👀 #{hashtag}",
        "Your daily dose of brainrot 🧠 #{hashtag}",
        "This hits different 🔥💯 #{hashtag}",
        "Peak content fr fr 💀 #{hashtag}",
        "Bro what even is this 😭 #{hashtag}"
    ]
    
    BRAINROT_HASHTAGS = [
        '#brainrot', '#viral', '#fyp', '#foryou', '#trending',
        '#sigma', '#ohio', '#rizz', '#gyatt', '#skibidi',
        '#meme', '#funny', '#comedy', '#reels', '#explorepage'
    ]
    
    def __init__(self, client: Client):
        """
        Initialize content poster
        
        Args:
            client: Authenticated Instagram client
        """
        self.client = client
        
    def generate_caption(self, original_caption: Optional[str] = None) -> str:
        """
        Generate an engaging caption for the post
        
        Args:
            original_caption: Optional original caption to reference
            
        Returns:
            Generated caption with hashtags
        """
        # Pick random template
        template = random.choice(self.CAPTION_TEMPLATES)
        
        # Pick random hashtag for template
        main_hashtag = random.choice(['brainrot', 'viral', 'fyp', 'sigma', 'trending'])
        caption = template.format(hashtag=main_hashtag)
        
        # Add additional hashtags
        selected_hashtags = random.sample(self.BRAINROT_HASHTAGS, k=random.randint(5, 10))
        hashtag_string = ' '.join(selected_hashtags)
        
        final_caption = f"{caption}\n\n{hashtag_string}"
        
        return final_caption
        
    def post_video(self, video_path: str, caption: Optional[str] = None) -> Optional[str]:
        """
        Post a video to Instagram as a reel
        
        Args:
            video_path: Path to video file
            caption: Optional caption (will be auto-generated if not provided)
            
        Returns:
            Media ID of posted content or None if failed
        """
        if not os.path.exists(video_path):
            logger.error(f"Video file not found: {video_path}")
            return None
            
        try:
            # Generate caption if not provided
            if caption is None:
                caption = self.generate_caption()
                
            logger.info(f"Posting video: {video_path}")
            logger.info(f"Caption: {caption[:100]}...")
            
            # Upload as reel/clip
            media = self.client.clip_upload(
                video_path,
                caption=caption
            )
            
            if media and media.pk:
                logger.info(f"Successfully posted! Media ID: {media.pk}")
                return str(media.pk)
            else:
                logger.error("Failed to post video - no media returned")
                return None
                
        except Exception as e:
            logger.error(f"Failed to post video {video_path}: {e}")
            return None
            
    def post_photo(self, photo_path: str, caption: Optional[str] = None) -> Optional[str]:
        """
        Post a photo to Instagram
        
        Args:
            photo_path: Path to photo file
            caption: Optional caption
            
        Returns:
            Media ID of posted content or None if failed
        """
        if not os.path.exists(photo_path):
            logger.error(f"Photo file not found: {photo_path}")
            return None
            
        try:
            if caption is None:
                caption = self.generate_caption()
                
            logger.info(f"Posting photo: {photo_path}")
            
            media = self.client.photo_upload(
                photo_path,
                caption=caption
            )
            
            if media and media.pk:
                logger.info(f"Successfully posted photo! Media ID: {media.pk}")
                return str(media.pk)
            else:
                logger.error("Failed to post photo")
                return None
                
        except Exception as e:
            logger.error(f"Failed to post photo {photo_path}: {e}")
            return None
            
    def delete_post(self, media_id: str) -> bool:
        """
        Delete a post from Instagram
        
        Args:
            media_id: ID of the media to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            result = self.client.media_delete(media_id)
            logger.info(f"Deleted post {media_id}")
            return result
        except Exception as e:
            logger.error(f"Failed to delete post {media_id}: {e}")
            return False
