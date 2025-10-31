"""
Instagram Credential Manager
Handles creation and management of Instagram credentials
"""
import json
import logging
import os
import random
import string
from typing import Optional, Tuple
from instagrapi import Client
from instagrapi.exceptions import (
    LoginRequired, 
    PleaseWaitFewMinutes, 
    ChallengeRequired,
    BadPassword
)

logger = logging.getLogger(__name__)


class CredentialManager:
    """Manages Instagram account credentials"""
    
    CREDENTIALS_FILE = "credentials.json"
    SESSION_FILE = "instagram_session.json"
    
    def __init__(self):
        self.username = None
        self.password = None
        self.email = None
        
    def generate_random_username(self) -> str:
        """Generate a random username"""
        prefix = random.choice(['brainrot', 'viral', 'content', 'daily', 'trending'])
        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return f"{prefix}_{suffix}"
        
    def generate_random_email(self) -> str:
        """Generate a random email address"""
        # Using temporary email services or create pattern
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        domain = random.choice(['tempmail.com', 'guerrillamail.com', '10minutemail.com'])
        return f"{username}@{domain}"
        
    def generate_random_password(self) -> str:
        """Generate a secure random password"""
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choices(chars, k=16))
        return password
        
    def load_credentials(self) -> bool:
        """
        Load existing credentials from file
        
        Returns:
            True if credentials loaded successfully, False otherwise
        """
        if not os.path.exists(self.CREDENTIALS_FILE):
            logger.info("No credentials file found")
            return False
            
        try:
            with open(self.CREDENTIALS_FILE, 'r') as f:
                creds = json.load(f)
                self.username = creds.get('username')
                self.password = creds.get('password')
                self.email = creds.get('email')
                
            if self.username and self.password:
                logger.info(f"Loaded credentials for user: {self.username}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to load credentials: {e}")
            return False
            
    def save_credentials(self):
        """Save credentials to file"""
        creds = {
            'username': self.username,
            'password': self.password,
            'email': self.email
        }
        
        try:
            with open(self.CREDENTIALS_FILE, 'w') as f:
                json.dump(creds, f, indent=2)
            logger.info(f"Saved credentials for user: {self.username}")
        except Exception as e:
            logger.error(f"Failed to save credentials: {e}")
            
    def create_credentials(self) -> Tuple[str, str, str]:
        """
        Create new Instagram credentials
        
        Returns:
            Tuple of (username, password, email)
        """
        self.username = self.generate_random_username()
        self.password = self.generate_random_password()
        self.email = self.generate_random_email()
        
        logger.info(f"Generated new credentials:")
        logger.info(f"  Username: {self.username}")
        logger.info(f"  Email: {self.email}")
        
        self.save_credentials()
        return self.username, self.password, self.email
        
    def get_credentials(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Get credentials, creating new ones if needed
        
        Returns:
            Tuple of (username, password)
        """
        if not self.load_credentials():
            logger.info("Creating new credentials...")
            self.create_credentials()
            
        return self.username, self.password
        
    def verify_credentials(self, client: Client) -> bool:
        """
        Verify credentials work with Instagram
        
        Args:
            client: Instagram client instance
            
        Returns:
            True if credentials are valid, False otherwise
        """
        try:
            # Try to login
            username, password = self.get_credentials()
            client.login(username, password)
            logger.info(f"Successfully logged in as {username}")
            return True
        except BadPassword:
            logger.error("Invalid password, credentials may be incorrect")
            return False
        except ChallengeRequired:
            logger.warning("Challenge required - account needs verification")
            # Try to handle challenge
            return False
        except LoginRequired:
            logger.error("Login required but credentials invalid")
            return False
        except PleaseWaitFewMinutes:
            logger.warning("Rate limited - please wait a few minutes")
            return False
        except Exception as e:
            logger.error(f"Failed to verify credentials: {e}")
            return False
