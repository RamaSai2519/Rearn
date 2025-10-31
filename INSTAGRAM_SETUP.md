"""
Instagram Account Setup Instructions
=====================================

This bot requires a valid Instagram account to function. Due to Instagram's security
measures, accounts MUST be created manually. Automated account creation is not possible
and violates Instagram's Terms of Service.

MANUAL ACCOUNT CREATION STEPS:
================================

1. CREATE AN EMAIL ADDRESS
   - Go to Gmail, Outlook, or ProtonMail
   - Create a new email account
   - Keep the email credentials safe
   
2. CREATE INSTAGRAM ACCOUNT
   - Go to https://www.instagram.com/accounts/emailsignup/
   - Use the email you created
   - Choose a username (brainrot themed: e.g., "viral_brainrot_daily")
   - Create a strong password
   - Complete phone verification (REQUIRED by Instagram)
   - Verify your email address
   
3. CONFIGURE THE BOT
   - Save your credentials in credentials.json:
   
   {
     "username": "your_instagram_username",
     "password": "your_instagram_password",
     "email": "your_email@example.com"
   }
   
4. FIRST LOGIN
   - Run the bot for the first time: python bot.py
   - If Instagram asks for verification:
     * Check your email for verification code
     * Enter the code when prompted
     * The bot will save the session for future use

5. ACCOUNT PREPARATION
   - Add a profile picture
   - Write a bio (e.g., "Daily viral brainrot content 🧠🔥")
   - Make the account public
   - Follow some accounts in your niche
   
IMPORTANT NOTES:
================

- Instagram REQUIRES phone verification for new accounts
- Use a real phone number (virtual numbers often don't work)
- Don't create multiple accounts from the same IP
- Wait 24-48 hours after account creation before posting
- Start with manual posts to build account trust
- The bot should only be used on accounts you own

ALTERNATIVE FOR TESTING:
========================

If you want to test the bot without a real Instagram account:
1. Use the --dry-run flag: python bot.py --dry-run
2. This will test all components except actual Instagram posting

For production use, you MUST use a legitimate, manually-created Instagram account.
