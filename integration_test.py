#!/usr/bin/env python3
"""
Integration Test for Instagram Brainrot Bot
Tests the complete workflow in dry-run mode
"""
import sys
import os
import logging

# Suppress most logging during test
logging.basicConfig(level=logging.WARNING)

def test_full_workflow():
    """Test the complete bot workflow in dry-run mode"""
    print("=" * 60)
    print("Instagram Brainrot Bot - Integration Test")
    print("=" * 60)
    print("\nTesting complete workflow in DRY RUN mode...")
    print("(No actual Instagram posting will occur)\n")
    
    try:
        from bot import InstagramBrainrotBot
        
        # Create bot in dry-run mode
        print("1. Initializing bot in dry-run mode...")
        bot = InstagramBrainrotBot(dry_run=True)
        assert bot.dry_run == True, "Dry run mode not enabled"
        print("   ✓ Bot initialized")
        
        # Setup
        print("\n2. Setting up bot components...")
        if not bot.setup():
            print("   ✗ Setup failed")
            return False
        print("   ✓ Setup completed")
        
        # Test content discovery (dry run creates mock data)
        print("\n3. Testing content discovery...")
        content_list = bot.find_content_to_post(count=10)
        if not content_list or len(content_list) == 0:
            print("   ✗ No content found")
            return False
        print(f"   ✓ Found {len(content_list)} content items")
        
        # Test processing and posting (simulated)
        print("\n4. Testing content processing (simulated)...")
        success_count = 0
        test_items = min(5, len(content_list))
        
        for i, content in enumerate(content_list[:test_items]):
            print(f"   Processing item {i+1}/{test_items}...")
            if bot.process_and_post_content(content):
                success_count += 1
            else:
                print(f"   ✗ Failed to process item {i+1}")
                
        print(f"   ✓ Successfully processed {success_count}/{test_items} items")
        
        # Cleanup
        print("\n5. Cleaning up...")
        bot.cleanup()
        print("   ✓ Cleanup completed")
        
        # Final check
        print("\n" + "=" * 60)
        if success_count >= bot.MIN_POSTS_PER_RUN:
            print(f"✓ Integration test PASSED!")
            print(f"  Successfully simulated {success_count} posts")
            print(f"  (Meets minimum requirement of {bot.MIN_POSTS_PER_RUN})")
            print("=" * 60)
            return True
        else:
            print(f"✗ Integration test FAILED!")
            print(f"  Only simulated {success_count} posts")
            print(f"  (Required minimum: {bot.MIN_POSTS_PER_RUN})")
            print("=" * 60)
            return False
            
    except Exception as e:
        print(f"\n✗ Integration test FAILED with error:")
        print(f"  {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_with_real_instagram():
    """Test with real Instagram account if credentials are available"""
    print("\n" + "=" * 60)
    print("Real Instagram Test")
    print("=" * 60)
    
    # Check if credentials exist
    if not os.path.exists('credentials.json'):
        print("\n⚠ No credentials.json found")
        print("  To test with a real Instagram account:")
        print("  1. Create credentials.json with your Instagram login")
        print("  2. Run: python integration_test.py --real")
        print("\n  See INSTAGRAM_SETUP.md for instructions")
        return None
        
    print("\nAttempting to test with real Instagram account...")
    print("WARNING: This will attempt to login and discover real content")
    print("         (but won't post anything)\n")
    
    try:
        from bot import InstagramBrainrotBot
        
        # Create bot in normal mode
        bot = InstagramBrainrotBot(dry_run=False)
        
        # Try setup (includes login)
        if not bot.setup():
            print("✗ Failed to setup with real Instagram account")
            print("  Check credentials and try again")
            return False
            
        print("✓ Successfully connected to Instagram")
        print(f"  Logged in as: {bot.credential_manager.username}")
        
        # Try to discover real content
        print("\nTesting content discovery with real Instagram...")
        content_list = bot.find_content_to_post(count=5)
        
        if content_list:
            print(f"✓ Found {len(content_list)} real content items")
            print("\nSample content:")
            for i, content in enumerate(content_list[:3]):
                print(f"  {i+1}. {content.get('caption', 'No caption')[:50]}...")
                print(f"     Views: {content.get('view_count', 0)}, Likes: {content.get('like_count', 0)}")
        else:
            print("⚠ No content found (might need to adjust hashtags)")
            
        bot.cleanup()
        return True
        
    except Exception as e:
        print(f"✗ Real Instagram test failed: {e}")
        return False

def main():
    """Run integration tests"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Integration tests for Instagram bot')
    parser.add_argument('--real', action='store_true',
                       help='Test with real Instagram account (requires credentials)')
    args = parser.parse_args()
    
    # Always run dry-run test first
    success = test_full_workflow()
    
    # Optionally test with real Instagram
    if args.real:
        real_result = test_with_real_instagram()
        if real_result is False:
            success = False
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
