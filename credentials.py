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
            
    def prompt_for_credentials(self) -> Tuple[str, str, str]:
        """
        Prompt user to enter credentials manually
        
        Returns:
            Tuple of (username, password, email)
        """
        print("\n" + "="*60)
        print("Instagram Credentials Required")
        print("="*60)
        print("\nNo credentials found. Please provide your Instagram account details.")
        print("NOTE: You must create an Instagram account manually first.")
        print("See INSTAGRAM_SETUP.md for instructions.\n")
        
        try:
            username = input("Instagram username: ").strip()
            password = input("Instagram password: ").strip()
            email = input("Email address: ").strip()
            
            if not username or not password:
                raise ValueError("Username and password are required")
                
            self.username = username
            self.password = password
            self.email = email
            
            self.save_credentials()
            return username, password, email
            
        except (KeyboardInterrupt, EOFError):
            logger.error("\nCredential entry cancelled by user")
            raise
        except Exception as e:
            logger.error(f"Failed to get credentials: {e}")
            raise
        
    def get_credentials(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Get credentials, prompting user if needed
        
        Returns:
            Tuple of (username, password)
        """
        if not self.load_credentials():
            logger.info("Credentials not found. Manual entry required.")
            self.prompt_for_credentials()
            
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
            # Try to login - password is passed securely to the API
            username, password = self.get_credentials()
            # Note: Password is not logged anywhere for security
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
