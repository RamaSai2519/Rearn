#!/usr/bin/env python3
"""
Simple validation test for bot modules
Checks that all classes can be instantiated and basic methods work
"""
import sys
import logging

# Suppress logging during tests
logging.basicConfig(level=logging.CRITICAL)

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        from database import MongoDBHandler
        from credentials import CredentialManager
        from content_discovery import ContentDiscovery
        from downloader import ContentDownloader
        from poster import ContentPoster
        from bot import InstagramBrainrotBot
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_credential_manager():
    """Test CredentialManager class"""
    print("\nTesting CredentialManager...")
    try:
        from credentials import CredentialManager
        
        cm = CredentialManager()
        
        # Test username generation
        username = cm.generate_random_username()
        assert username and '_' in username, "Username generation failed"
        
        # Test email generation
        email = cm.generate_random_email()
        assert email and '@' in email, "Email generation failed"
        
        # Test password generation
        password = cm.generate_random_password()
        assert len(password) >= 16, "Password too short"
        
        print("✓ CredentialManager tests passed")
        return True
    except Exception as e:
        print(f"✗ CredentialManager test failed: {e}")
        return False

def test_database_handler():
    """Test MongoDBHandler class (without actual connection)"""
    print("\nTesting MongoDBHandler...")
    try:
        from database import MongoDBHandler
        
        # Just test instantiation
        db = MongoDBHandler("mongodb://fake-connection-string")
        assert db.connection_string == "mongodb://fake-connection-string"
        
        print("✓ MongoDBHandler instantiation passed")
        return True
    except Exception as e:
        print(f"✗ MongoDBHandler test failed: {e}")
        return False

def test_bot_class():
    """Test InstagramBrainrotBot class"""
    print("\nTesting InstagramBrainrotBot...")
    try:
        from bot import InstagramBrainrotBot
        
        bot = InstagramBrainrotBot()
        assert bot.MIN_POSTS_PER_RUN == 5, "MIN_POSTS_PER_RUN should be 5"
        assert bot.MONGODB_URI is not None, "MONGODB_URI should be set"
        
        print("✓ InstagramBrainrotBot instantiation passed")
        return True
    except Exception as e:
        print(f"✗ InstagramBrainrotBot test failed: {e}")
        return False

def test_content_poster():
    """Test ContentPoster class"""
    print("\nTesting ContentPoster...")
    try:
        from poster import ContentPoster
        from instagrapi import Client
        
        client = Client()
        poster = ContentPoster(client)
        
        # Test caption generation
        caption = poster.generate_caption()
        assert len(caption) > 0, "Caption should not be empty"
        assert '#' in caption, "Caption should contain hashtags"
        
        print("✓ ContentPoster tests passed")
        return True
    except Exception as e:
        print(f"✗ ContentPoster test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Instagram Brainrot Bot - Validation Tests")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_credential_manager,
        test_database_handler,
        test_bot_class,
        test_content_poster,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)
    
    if all(results):
        print("\n✓ All validation tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
