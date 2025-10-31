"""
Content Discovery Module
Finds trending and most-viewed "brainrot" content on Instagram
"""
import logging
import random
from typing import List, Dict
from instagrapi import Client
from instagrapi.types import Media

logger = logging.getLogger(__name__)


class ContentDiscovery:
    """Discovers trending brainrot content on Instagram"""
    
    # Brainrot-related hashtags and search terms
    # Note: Content should comply with Instagram's community guidelines
    BRAINROT_HASHTAGS = [
        'brainrot',
        'skibiditoilet',
        'sigma',
        'ohio',
        'griddy',
        'mewing',
        'foryou',
        'fyp',
        'viral',
        'trending',
        'comedy',
        'memes',
        'funny',
        'entertainment'
    ]
    
    def __init__(self, client: Client):
        """
        Initialize content discovery
        
        Args:
            client: Authenticated Instagram client
        """
        self.client = client
        
    def search_by_hashtag(self, hashtag: str, limit: int = 20) -> List[Media]:
        """
        Search for content by hashtag
        
        Args:
            hashtag: Hashtag to search for
            limit: Maximum number of posts to retrieve
            
        Returns:
            List of Media objects
        """
        try:
            logger.info(f"Searching for #{hashtag}")
            medias = self.client.hashtag_medias_top(hashtag, amount=limit)
            logger.info(f"Found {len(medias)} posts for #{hashtag}")
            return medias
        except Exception as e:
            logger.error(f"Failed to search hashtag #{hashtag}: {e}")
            return []
            
    def get_trending_content(self, num_posts: int = 50) -> List[Dict]:
        """
        Get trending brainrot content from Instagram
        
        Args:
            num_posts: Total number of posts to retrieve
            
        Returns:
            List of dictionaries containing content info
        """
        all_content = []
        posts_per_hashtag = max(5, num_posts // len(self.BRAINROT_HASHTAGS))
        
        # Shuffle hashtags to get variety
        hashtags = random.sample(self.BRAINROT_HASHTAGS, min(10, len(self.BRAINROT_HASHTAGS)))
        
        for hashtag in hashtags:
            try:
                medias = self.search_by_hashtag(hashtag, limit=posts_per_hashtag)
                
                for media in medias:
                    # Filter for video content (reels)
                    if media.media_type == 2 or media.product_type == "clips":  # Video or Reel
                        content_info = {
                            'id': media.id,
                            'pk': media.pk,
                            'code': media.code,
                            'video_url': media.video_url if hasattr(media, 'video_url') else None,
                            'thumbnail_url': media.thumbnail_url,
                            'caption': media.caption_text if hasattr(media, 'caption_text') else '',
                            'like_count': media.like_count,
                            'view_count': media.view_count if hasattr(media, 'view_count') else 0,
                            'comment_count': media.comment_count,
                            'hashtag': hashtag,
                            'url': f"https://www.instagram.com/p/{media.code}/"
                        }
                        all_content.append(content_info)
                        
                if len(all_content) >= num_posts:
                    break
                    
            except Exception as e:
                logger.error(f"Error processing hashtag {hashtag}: {e}")
                continue
                
        # Sort by engagement (likes + views + comments)
        all_content.sort(
            key=lambda x: (x.get('view_count', 0) + x.get('like_count', 0) * 2 + x.get('comment_count', 0) * 3),
            reverse=True
        )
        
        logger.info(f"Total content found: {len(all_content)}")
        return all_content[:num_posts]
        
    def get_explore_content(self, limit: int = 20) -> List[Dict]:
        """
        Get content from Instagram explore page
        
        Args:
            limit: Maximum number of posts to retrieve
            
        Returns:
            List of content dictionaries
        """
        try:
            logger.info("Fetching explore page content")
            medias = self.client.get_explore_medias(amount=limit)
            
            content_list = []
            for media in medias:
                if media.media_type == 2 or media.product_type == "clips":
                    content_info = {
                        'id': media.id,
                        'pk': media.pk,
                        'code': media.code,
                        'video_url': media.video_url if hasattr(media, 'video_url') else None,
                        'thumbnail_url': media.thumbnail_url,
                        'caption': media.caption_text if hasattr(media, 'caption_text') else '',
                        'like_count': media.like_count,
                        'view_count': media.view_count if hasattr(media, 'view_count') else 0,
                        'url': f"https://www.instagram.com/p/{media.code}/"
                    }
                    content_list.append(content_info)
                    
            logger.info(f"Found {len(content_list)} explore videos")
            return content_list
        except Exception as e:
            logger.error(f"Failed to get explore content: {e}")
            return []
