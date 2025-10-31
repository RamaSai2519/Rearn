"""
Content Downloader Module
Downloads Instagram content (reels and videos) to local storage
"""
import logging
import os
import requests
from pathlib import Path
from typing import Optional
from instagrapi import Client

logger = logging.getLogger(__name__)


class ContentDownloader:
    """Downloads Instagram media content"""
    
    def __init__(self, client: Client, download_dir: str = "downloads"):
        """
        Initialize content downloader
        
        Args:
            client: Authenticated Instagram client
            download_dir: Directory to save downloaded content
        """
        self.client = client
        self.download_dir = Path(download_dir)
        self._ensure_download_dir()
        
    def _ensure_download_dir(self):
        """Create download directory if it doesn't exist"""
        self.download_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Download directory: {self.download_dir.absolute()}")
        
    def download_video(self, media_pk: int, filename: Optional[str] = None) -> Optional[str]:
        """
        Download video from Instagram
        
        Args:
            media_pk: Primary key of the media
            filename: Optional custom filename
            
        Returns:
            Path to downloaded file or None if failed
        """
        try:
            if filename is None:
                filename = f"{media_pk}.mp4"
                
            filepath = self.download_dir / filename
            
            # Download using instagrapi
            logger.info(f"Downloading video {media_pk}")
            downloaded_path = self.client.video_download(media_pk, folder=str(self.download_dir))
            
            if downloaded_path and os.path.exists(downloaded_path):
                logger.info(f"Successfully downloaded to {downloaded_path}")
                return str(downloaded_path)
            else:
                logger.error(f"Download failed for {media_pk}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to download video {media_pk}: {e}")
            return None
            
    def download_by_url(self, url: str, filename: str) -> Optional[str]:
        """
        Download video from direct URL
        
        Args:
            url: Direct video URL
            filename: Filename to save as
            
        Returns:
            Path to downloaded file or None if failed
        """
        try:
            filepath = self.download_dir / filename
            
            logger.info(f"Downloading from URL: {url}")
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            logger.info(f"Successfully downloaded to {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Failed to download from URL {url}: {e}")
            return None
            
    def cleanup_old_files(self, keep_recent: int = 10):
        """
        Clean up old downloaded files
        
        Args:
            keep_recent: Number of recent files to keep
        """
        try:
            files = sorted(
                self.download_dir.glob("*.mp4"),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )
            
            for file in files[keep_recent:]:
                file.unlink()
                logger.info(f"Deleted old file: {file.name}")
                
        except Exception as e:
            logger.error(f"Failed to cleanup files: {e}")
