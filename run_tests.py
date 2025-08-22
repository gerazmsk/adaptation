#!/usr/bin/env python3
"""
Test runner for the Telegram GPT Bot
Runs all tests and provides a summary
"""

import subprocess
import sys
import os
from datetime import datetime

def run_command(command, description):
    """Run a command and return success status"""
    print(f"\n{'='*60}")
    print(f"🔍 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ SUCCESS")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ FAILED")
            if result.stderr:
                print(f"Error: {result.stderr}")
            if result.stdout:
                print(f"Output: {result.stdout}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    """Main test runner"""
    print("🚀 Starting Telegram GPT Bot Test Suite")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if we're in the right directory
    if not os.path.exists("bot.py"):
        print("❌ Error: bot.py not found. Please run this from the project directory.")
        sys.exit(1)
    
    # Test 1: Check Python dependencies
    print("\n📦 Checking Python dependencies...")
    try:
        import telegram
        import requests
        import dotenv
        print("✅ All required packages are available")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    # Test 2: Run unit tests
    success = run_command("python3 test_bot.py", "Running Bot Unit Tests")
    
    # Test 3: Test GPT API (if environment is set up)
    if os.path.exists(".env"):
        print("\n🔌 Testing GPT API connection...")
        api_success = run_command("python3 test_gpt_api.py", "Testing GPT API Connection")
        success = success and api_success
    else:
        print("\n⚠️  No .env file found. Skipping API tests.")
        print("   Create a .env file with GPT_API_KEY and GPT_API_URL to test API connection.")
    
    # Test 4: Check bot syntax
    syntax_success = run_command("python3 -m py_compile bot.py", "Checking Bot Code Syntax")
    success = success and syntax_success
    
    # Test 5: Check test files syntax
    test_syntax_success = run_command("python3 -m py_compile test_bot.py", "Checking Test Code Syntax")
    success = success and test_syntax_success
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    if success:
        print("🎉 ALL TESTS PASSED! Your bot is ready to run.")
        print("\nTo start the bot, run:")
        print("   python3 bot.py")
        print("\nOr use the shell script:")
        print("   ./run_bot.sh")
    else:
        print("⚠️  SOME TESTS FAILED. Please check the errors above.")
        print("\nCommon issues:")
        print("1. Missing dependencies: pip install -r requirements.txt")
        print("2. Environment variables not set in .env file")
        print("3. Bot token issues")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
