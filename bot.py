"""
Instagram Brainrot Bot - Main Orchestrator
Autonomous bot that finds, downloads, and reposts trending brainrot content
"""
import logging
import time
import sys
from typing import List, Dict
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, PleaseWaitFewMinutes

from database import MongoDBHandler
from credentials import CredentialManager
from content_discovery import ContentDiscovery
from downloader import ContentDownloader
from poster import ContentPoster

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot.log')
    ]
)

logger = logging.getLogger(__name__)


class InstagramBrainrotBot:
    """Main bot orchestrator for autonomous Instagram content reposting"""
    
    # MongoDB connection string
    MONGODB_URI = "mongodb+srv://rama:7MR9oLpef122UCdy@cluster0.fquqway.mongodb.net/?retryWrites=true&w=majority&appName=Cluster"
    
    # Minimum posts per run
    MIN_POSTS_PER_RUN = 5
    
    def __init__(self):
        """Initialize the Instagram bot"""
        self.client = Client()
        self.db_handler = MongoDBHandler(self.MONGODB_URI)
        self.credential_manager = CredentialManager()
        self.content_discovery = None
        self.downloader = None
        self.poster = None
        self.is_logged_in = False
        
    def setup(self) -> bool:
        """
        Setup bot components
        
        Returns:
            True if setup successful, False otherwise
        """
        logger.info("=" * 60)
        logger.info("Instagram Brainrot Bot Starting Up")
        logger.info("=" * 60)
        
        # Connect to MongoDB
        logger.info("Connecting to MongoDB...")
        if not self.db_handler.connect():
            logger.error("Failed to connect to MongoDB")
            return False
            
        logger.info(f"Posted content count: {self.db_handler.get_posted_count()}")
        
        # Setup Instagram credentials
        logger.info("Setting up Instagram credentials...")
        username, password = self.credential_manager.get_credentials()
        
        if not username or not password:
            logger.error("Failed to obtain credentials")
            return False
            
        # Login to Instagram
        logger.info(f"Logging in to Instagram as {username}...")
        if not self._login(username, password):
            logger.error("Failed to login to Instagram")
            return False
            
        # Initialize modules
        self.content_discovery = ContentDiscovery(self.client)
        self.downloader = ContentDownloader(self.client)
        self.poster = ContentPoster(self.client)
        
        logger.info("Bot setup completed successfully!")
        return True
        
    def _login(self, username: str, password: str) -> bool:
        """
        Login to Instagram
        
        Args:
            username: Instagram username
            password: Instagram password
            
        Returns:
            True if login successful, False otherwise
        """
        try:
            # Try to load existing session
            session_file = self.credential_manager.SESSION_FILE
            try:
                self.client.load_settings(session_file)
                self.client.login(username, password)
                logger.info("Logged in using existing session")
                self.is_logged_in = True
                return True
            except:
                pass
                
            # Fresh login
            self.client.login(username, password)
            
            # Save session
            self.client.dump_settings(session_file)
            logger.info("Successfully logged in and saved session")
            self.is_logged_in = True
            return True
            
        except LoginRequired as e:
            logger.error(f"Login required but failed: {e}")
            return False
        except PleaseWaitFewMinutes as e:
            logger.error(f"Rate limited: {e}")
            return False
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return False
            
    def find_content_to_post(self, count: int = 50) -> List[Dict]:
        """
        Find content that hasn't been posted yet
        
        Args:
            count: Number of content items to search for
            
        Returns:
            List of content items ready to post
        """
        logger.info(f"Searching for {count} trending content items...")
        
        # Get trending content
        all_content = self.content_discovery.get_trending_content(num_posts=count)
        
        # Filter out already posted content
        new_content = []
        for content in all_content:
            content_id = str(content['pk'])
            if not self.db_handler.is_content_posted(content_id):
                new_content.append(content)
            else:
                logger.debug(f"Skipping already posted content: {content_id}")
                
        logger.info(f"Found {len(new_content)} new content items to post")
        return new_content
        
    def process_and_post_content(self, content: Dict) -> bool:
        """
        Download and post a single content item
        
        Args:
            content: Content dictionary with metadata
            
        Returns:
            True if successfully posted, False otherwise
        """
        content_id = str(content['pk'])
        content_url = content['url']
        
        try:
            logger.info(f"Processing content: {content_id}")
            logger.info(f"  Source: {content_url}")
            logger.info(f"  Views: {content.get('view_count', 0)}, Likes: {content.get('like_count', 0)}")
            
            # Download the content
            logger.info("Downloading content...")
            video_path = self.downloader.download_video(content['pk'])
            
            if not video_path:
                logger.error("Failed to download content")
                return False
                
            # Wait a bit to avoid rate limiting
            time.sleep(2)
            
            # Post the content
            logger.info("Posting content to Instagram...")
            media_id = self.poster.post_video(video_path)
            
            if not media_id:
                logger.error("Failed to post content")
                return False
                
            # Mark as posted in database
            self.db_handler.mark_content_posted(
                content_id=content_id,
                content_url=f"https://www.instagram.com/p/{media_id}/",
                source_url=content_url
            )
            
            logger.info(f"✓ Successfully posted content {content_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error processing content {content_id}: {e}")
            return False
            
    def run(self):
        """Main bot execution - find and post content"""
        logger.info("\n" + "=" * 60)
        logger.info("Starting bot run...")
        logger.info("=" * 60)
        
        posted_count = 0
        attempt_count = 0
        max_attempts = 20  # Try up to 20 items to get 5 successful posts
        
        # Find content to post
        content_list = self.find_content_to_post(count=50)
        
        if not content_list:
            logger.warning("No new content found to post")
            return
            
        # Post content until we reach minimum required
        for content in content_list:
            if posted_count >= self.MIN_POSTS_PER_RUN:
                break
                
            if attempt_count >= max_attempts:
                logger.warning(f"Reached max attempts ({max_attempts}), stopping")
                break
                
            attempt_count += 1
            
            # Process and post
            if self.process_and_post_content(content):
                posted_count += 1
                logger.info(f"Progress: {posted_count}/{self.MIN_POSTS_PER_RUN} posts completed")
                
                # Wait between posts to avoid rate limiting
                if posted_count < self.MIN_POSTS_PER_RUN:
                    wait_time = 30
                    logger.info(f"Waiting {wait_time} seconds before next post...")
                    time.sleep(wait_time)
            else:
                logger.warning(f"Failed to post content, continuing to next item")
                time.sleep(5)
                
        # Summary
        logger.info("\n" + "=" * 60)
        logger.info(f"Bot run completed!")
        logger.info(f"Successfully posted: {posted_count}/{self.MIN_POSTS_PER_RUN} items")
        logger.info(f"Total attempts: {attempt_count}")
        logger.info("=" * 60)
        
        if posted_count < self.MIN_POSTS_PER_RUN:
            logger.warning(f"Warning: Only posted {posted_count} items, target was {self.MIN_POSTS_PER_RUN}")
            
    def cleanup(self):
        """Cleanup resources"""
        logger.info("Cleaning up resources...")
        
        if self.downloader:
            self.downloader.cleanup_old_files(keep_recent=5)
            
        if self.db_handler:
            self.db_handler.close()
            
        logger.info("Cleanup completed")
        
    def execute(self):
        """Execute complete bot workflow"""
        try:
            # Setup
            if not self.setup():
                logger.error("Bot setup failed, exiting")
                sys.exit(1)
                
            # Run main logic
            self.run()
            
        except KeyboardInterrupt:
            logger.info("\nBot stopped by user")
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
        finally:
            # Cleanup
            self.cleanup()


def main():
    """Entry point for the bot"""
    bot = InstagramBrainrotBot()
    bot.execute()


if __name__ == "__main__":
    main()
